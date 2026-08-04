# -*- coding: utf-8 -*-
"""
Created on Tue Aug  4 14:52:54 2026

@author: fatemeh
"""
import sys
import os
import pandas as pd

# Add the project root to Python's path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from src.loader import SupplyChainLoader

if __name__ == "__main__":
    print("="*60)
    print("🚀 SUPPLY CHAIN OPTIMIZATION PIPELINE")
    print("="*60)
    print()
    
    # Initialize the loader
    loader = SupplyChainLoader()
    
    # Run the pipeline
    master_df = loader.run_pipeline()
    
    # Show summary
    print("\n" + "="*60)
    print("📊 FINAL DATASET SUMMARY")
    print("="*60)
    print(f"   Total Rows: {len(master_df)}")
    print(f"   Total Columns: {len(master_df.columns)}")
    
    # Active carriers
    if 'carrier_status' in master_df.columns:
        active = master_df[master_df['carrier_status'] == 'Active']['carrier'].nunique()
        discontinued = master_df[master_df['carrier_status'] == 'Discontinued']['carrier'].nunique()
        print(f"   Active Carriers: {active}")
        print(f"   Discontinued Carriers: {discontinued}")
    
    # Cost summary
    if 'total_cost' in master_df.columns:
        print(f"\n   💰 Cost Summary:")
        print(f"      Average Total Cost: ${master_df['total_cost'].mean():.2f}")
        print(f"      Max Total Cost: ${master_df['total_cost'].max():.2f}")
        print(f"      Min Total Cost: ${master_df['total_cost'].min():.2f}")
    
    # Orders with cost
    if 'total_cost' in master_df.columns:
        with_cost = master_df['total_cost'].notna().sum()
        total = len(master_df)
        print(f"\n   📦 Orders with cost calculated: {with_cost} out of {total} ({with_cost/total*100:.2f}%)")
    
    # Sample of V44_3 orders
    if 'carrier_status' in master_df.columns:
        v44_3_orders = master_df[master_df['carrier_status'] == 'Discontinued']
        if len(v44_3_orders) > 0:
            print(f"\n   🚫 V44_3 Discontinued Carrier Orders: {len(v44_3_orders)}")
            print(f"      (These orders have no freight cost - flagged for review)")
    
    print("\n" + "="*60)
    print("📌 NEXT STEPS")
    print("="*60)
    print("  1. Open Power BI and connect to:")
    print(f"     -> {loader.processed_path}")
    print("  2. Build your Supply Chain Optimization dashboard")
    print("  3. Show cost savings opportunities")
    print("  4. Analyze carrier performance by cost")
    print("  5. Identify optimization opportunities")
    print("\n" + "="*60)
    print("🎉 Pipeline Complete!")
    print("="*60)