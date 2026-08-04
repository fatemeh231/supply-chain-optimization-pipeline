# -*- coding: utf-8 -*-
"""
Created on Tue Aug  4 14:47:59 2026

@author: fatemeh
"""

# src/config.py
# Supply Chain Optimization - Configuration

# ============================================
# 1. COLUMN MAPPINGS (Excel sheets → Clean names)
# ============================================

COLUMN_MAPPINGS = {
    "OrderList": {
        "Order ID": "order_id",
        "Order Date": "order_date",
        "Origin Port": "origin_port",
        "Carrier": "carrier",
        "TPT": "tpt",
        "Service Level": "service_level",
        "Ship ahead day count": "ship_ahead_days",
        "Ship Late Day count": "ship_late_days",
        "Customer": "customer",
        "Product ID": "product_id",
        "Plant Code": "plant_code",
        "Destination Port": "destination_port",
        "Unit quantity": "unit_quantity",
        "Weight": "weight"
    },
    "FreightRates": {
        "Carrier": "carrier",
        "orig_port_cd": "origin_port",
        "dest_port_cd": "destination_port",
        "minm_wgh_qty": "min_weight",
        "max_wgh_qty": "max_weight",
        "svc_cd": "service_code",
        "minimum cost": "minimum_cost",
        "rate": "rate",
        "mode_dsc": "mode_description",
        "tpt_day_cnt": "transit_days",
        "Carrier type": "carrier_type"
    },
    "WhCosts": {
        "WH": "plant_code",
        "Cost/unit": "cost_per_unit"
    },
    "WhCapacities": {
        "Plant ID": "plant_code",
        "Daily Capacity ": "daily_capacity"
    },
    "ProductsPerPlant": {
        "Plant Code": "plant_code",
        "Product ID": "product_id"
    },
    "VmiCustomers": {
        "Plant Code": "plant_code",
        "Customers": "customer"
    },
    "PlantPorts": {
        "Plant Code": "plant_code",
        "Port": "port"
    }
}

# ============================================
# 2. SHEET NAMES
# ============================================

SHEETS = [
    "OrderList",
    "FreightRates",
    "WhCosts",
    "WhCapacities",
    "ProductsPerPlant",
    "VmiCustomers",
    "PlantPorts"
]

# ============================================
# 3. FILE PATHS
# ============================================

RAW_FILE_PATH = "data/raw/supply chain logisitcs problem.xlsx"
PROCESSED_FILE_PATH = "data/processed/supply_chain_master.parquet"

# ============================================
# 4. DISCONTINUED CARRIER
# ============================================

DISCONTINUED_CARRIER = "V44_3"