# -*- coding: utf-8 -*-
"""
Created on Tue Aug  4 14:48:29 2026

@author: fatemeh
"""
import pandas as pd
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from src.config import (
    COLUMN_MAPPINGS,
    SHEETS,
    RAW_FILE_PATH,
    PROCESSED_FILE_PATH,
    DISCONTINUED_CARRIER
)

class SupplyChainLoader:
    """
    Loads and processes the Supply Chain Logistics Problem dataset.
    Handles 7 interconnected tables and creates a master dataset.
    """
    
    def __init__(self, raw_path: str = None, processed_path: str = None):
        """
        Initialize the loader with file paths.
        
        Args:
            raw_path: Path to the raw Excel file
            processed_path: Path where the processed Parquet file will be saved
        """
        self.raw_path = raw_path or RAW_FILE_PATH
        self.processed_path = processed_path or PROCESSED_FILE_PATH
        self.data = {}
        self.master_df = None
        
    def load_all_sheets(self) -> dict:
        """
        Load all 7 sheets from the Excel file.
        
        Returns:
            dict: Dictionary with sheet names as keys and DataFrames as values
        """
        print("📂 Loading all sheets...")
        
        for sheet in SHEETS:
            try:
                df = pd.read_excel(self.raw_path, sheet_name=sheet)
                self.data[sheet] = df
                print(f"   ✅ {sheet}: {len(df)} rows, {len(df.columns)} columns")
            except Exception as e:
                print(f"   ❌ Error loading {sheet}: {e}")
                
        return self.data
    
    def clean_column_names(self, df: pd.DataFrame, sheet_name: str) -> pd.DataFrame:
        """
        Rename columns using the mapping dictionary.
        
        Args:
            df: DataFrame to clean
            sheet_name: Name of the sheet (to find the right mapping)
            
        Returns:
            pd.DataFrame: DataFrame with renamed columns
        """
        mapping = COLUMN_MAPPINGS.get(sheet_name, {})
        
        # Only rename columns that exist
        columns_to_rename = {k: v for k, v in mapping.items() if k in df.columns}
        
        if columns_to_rename:
            df.rename(columns=columns_to_rename, inplace=True)
            print(f"   ✅ Renamed {len(columns_to_rename)} columns in {sheet_name}")
            
        return df
    
    def add_carrier_status(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Add a column to flag discontinued carriers.
        
        Args:
            df: OrderList DataFrame
            
        Returns:
            pd.DataFrame: DataFrame with carrier_status column
        """
        df['carrier_status'] = df['carrier'].apply(
            lambda x: 'Discontinued' if x == DISCONTINUED_CARRIER else 'Active'
        )
        print(f"   ✅ Added carrier_status column")
        print(f"      Active: {len(df[df['carrier_status'] == 'Active'])}")
        print(f"      Discontinued: {len(df[df['carrier_status'] == 'Discontinued'])}")
        
        return df
    
    def merge_freight_rates(self, order_df: pd.DataFrame) -> pd.DataFrame:
        """
        Merge OrderList with FreightRates on carrier, origin, and destination ports.
        
        Args:
            order_df: OrderList DataFrame
            
        Returns:
            pd.DataFrame: Merged DataFrame
        """
        freight_rates = self.data['FreightRates']
        
        # Clean column names for FreightRates
        freight_rates = self.clean_column_names(freight_rates, "FreightRates")
        
        # Merge on carrier, origin port, destination port
        merged = order_df.merge(
            freight_rates,
            left_on=['carrier', 'origin_port', 'destination_port'],
            right_on=['carrier', 'origin_port', 'destination_port'],
            how='left'
        )
        
        matched = merged['rate'].notna().sum()
        total = len(merged)
        print(f"   ✅ Merged with FreightRates: {matched} matched out of {total} ({matched/total*100:.2f}%)")
        
        return merged
    
    def merge_plant_tables(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Merge with PlantPorts, WhCosts, WhCapacities, ProductsPerPlant, and VmiCustomers.
        
        Args:
            df: DataFrame to enrich
            
        Returns:
            pd.DataFrame: Enriched DataFrame
        """
        # 1. PlantPorts
        plant_ports = self.clean_column_names(self.data['PlantPorts'], "PlantPorts")
        df = df.merge(plant_ports, left_on=['plant_code'], right_on=['plant_code'], how='left')
        print(f"   ✅ Merged PlantPorts")
        
        # 2. WhCosts
        wh_costs = self.clean_column_names(self.data['WhCosts'], "WhCosts")
        df = df.merge(wh_costs, left_on=['plant_code'], right_on=['plant_code'], how='left')
        print(f"   ✅ Merged WhCosts")
        
        # 3. WhCapacities
        wh_capacities = self.clean_column_names(self.data['WhCapacities'], "WhCapacities")
        df = df.merge(wh_capacities, left_on=['plant_code'], right_on=['plant_code'], how='left')
        print(f"   ✅ Merged WhCapacities")
        
        # 4. ProductsPerPlant
        products_per_plant = self.clean_column_names(self.data['ProductsPerPlant'], "ProductsPerPlant")
        df = df.merge(
            products_per_plant,
            left_on=['plant_code', 'product_id'],
            right_on=['plant_code', 'product_id'],
            how='left'
        )
        print(f"   ✅ Merged ProductsPerPlant")
        
        # 5. VmiCustomers
        vmi_customers = self.clean_column_names(self.data['VmiCustomers'], "VmiCustomers")
        df = df.merge(vmi_customers, left_on=['plant_code'], right_on=['plant_code'], how='left')
        print(f"   ✅ Merged VmiCustomers")
        
        return df
    
    def calculate_costs(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Calculate freight cost and total cost.
        
        Args:
            df: DataFrame with rate and cost_per_unit columns
            
        Returns:
            pd.DataFrame: DataFrame with cost columns added
        """
        # Freight cost = Weight × Rate (only for active carriers)
        df['freight_cost'] = df.apply(
            lambda row: row['weight'] * row['rate'] 
            if pd.notna(row['rate']) and row['carrier_status'] == 'Active' 
            else None,
            axis=1
        )
        
        # Warehouse cost = Unit quantity × Cost per unit
        df['warehouse_cost'] = df.apply(
            lambda row: row['unit_quantity'] * row['cost_per_unit'] 
            if pd.notna(row['cost_per_unit']) 
            else None,
            axis=1
        )
        
        # Total cost = Freight cost + Warehouse cost
        df['total_cost'] = df['freight_cost'] + df['warehouse_cost']
        
        # Count orders with cost
        total = len(df)
        with_cost = df['total_cost'].notna().sum()
        print(f"   ✅ Calculated costs: {with_cost} out of {total} rows have total cost ({with_cost/total*100:.2f}%)")
        
        return df
    
    def run_pipeline(self) -> pd.DataFrame:
        """
        Run the complete ETL pipeline.
        
        Returns:
            pd.DataFrame: Master dataset
        """
        print("="*60)
        print("📊 SUPPLY CHAIN OPTIMIZATION - ETL PIPELINE")
        print("="*60)
        
        # Step 1: Load all sheets
        print("\n🔄 STEP 1: Loading all sheets...")
        self.load_all_sheets()
        
        # Step 2: Clean OrderList
        print("\n🔄 STEP 2: Cleaning OrderList...")
        order_df = self.data['OrderList']
        order_df = self.clean_column_names(order_df, "OrderList")
        
        # Step 3: Add carrier status
        print("\n🔄 STEP 3: Adding carrier status...")
        order_df = self.add_carrier_status(order_df)
        
        # Step 4: Merge with FreightRates
        print("\n🔄 STEP 4: Merging with FreightRates...")
        master_df = self.merge_freight_rates(order_df)
        
        # Step 5: Merge with plant tables
        print("\n🔄 STEP 5: Merging with plant tables...")
        master_df = self.merge_plant_tables(master_df)
        
        # Step 6: Calculate costs
        print("\n🔄 STEP 6: Calculating costs...")
        master_df = self.calculate_costs(master_df)
        
        # Step 7: Save to Parquet
        print("\n🔄 STEP 7: Saving to Parquet...")
        os.makedirs(os.path.dirname(self.processed_path), exist_ok=True)
        master_df.to_parquet(self.processed_path, index=False)
        print(f"   ✅ Saved to: {self.processed_path}")
        print(f"   Shape: {master_df.shape[0]} rows, {master_df.shape[1]} columns")
        
        self.master_df = master_df
        
        print("\n" + "="*60)
        print("🎉 Pipeline Completed Successfully!")
        print("="*60)
        
        return master_df