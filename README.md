# 📦 Supply Chain Optimization Pipeline

> *"From messy Excel chaos to actionable supply chain insights"*

![Python](https://img.shields.io/badge/Python-3.10-blue)
![Pandas](https://img.shields.io/badge/Pandas-2.0+-green)
![Power BI](https://img.shields.io/badge/Power%20BI-Ready-yellow)
![License](https://img.shields.io/badge/License-MIT-lightgrey)

---

## 📌 Overview

Supply chain managers deal with **complex, multi-table data** every day. Orders, freight rates, warehouse costs, plant capacities, and product mappings are scattered across different sheets—each with different formats and relationships.

**This project solves that problem.**

It provides an automated **ETL pipeline** that:
1. Reads a messy Excel file with **7 interconnected sheets**
2. Performs complex joins across all tables
3. Handles **discontinued carriers** (V44_3) and missing data
4. Calculates **freight costs, warehouse costs, and total costs**
5. Exports a production-ready Parquet file
6. Visualizes everything in an interactive Power BI dashboard

---

## 🧠 The Challenge

This dataset was **not a simple CSV**. It was one Excel file with **7 sheets**, each with different schemas:

| Sheet | Purpose | Key Columns |
| :--- | :--- | :--- |
| OrderList | Main orders | Order ID, Carrier, Plant Code, Weight |
| FreightRates | Shipping costs | Carrier, Origin/Destination Ports, Rate |
| WhCosts | Storage costs | Plant, Cost/unit |
| WhCapacities | Daily capacity | Plant, Daily Capacity |
| ProductsPerPlant | Product availability | Plant Code, Product ID |
| VmiCustomers | VMI restrictions | Plant Code, Customers |
| PlantPorts | Plant-port mapping | Plant Code, Port |

**The Real Mess:**
- One Excel file, 7 sheets → required multiple reads and joins
- 9,215 orders → expanded to **209,402 rows** after matching weight brackets
- 854 orders with **V44_3** (discontinued carrier) → no freight rates → full nulls for cost columns
- Complex business logic: matching order weight to correct freight rate bracket
- Multiple joins required: OrderList → FreightRates → PlantPorts → WhCosts → WhCapacities → ProductsPerPlant → VmiCustomers

---

## 🚀 The Pipeline

```
Raw Excel (7 Sheets)
    ↓
Load All Sheets (Python)
    ↓
Clean Column Names
    ↓
Flag Discontinued Carriers (V44_3)
    ↓
Complex Joins:
- OrderList → FreightRates (Carrier, Origin, Destination, Weight Bracket)
- → PlantPorts
- → WhCosts
- → WhCapacities
- → ProductsPerPlant
- → VmiCustomers
    ↓
Calculate Costs:
- Freight Cost = Weight × Rate
- Warehouse Cost = Unit Quantity × Cost/unit
- Total Cost = Freight + Warehouse
    ↓
Fix Data Types (Power Query)
    ↓
Export as Parquet
    ↓
Power BI Dashboard
```

---


## 🛠️ Technologies Used

| Tool | Purpose |
| :--- | :--- |
| **Python 3.10** | Core programming language |
| **Pandas** | Data manipulation & cleaning |
| **NumPy** | Numerical operations |
| **PyArrow** | Parquet file support |
| **OpenPyXL** | Excel file support |
| **Power BI** | Dashboard & visualization |

---

## 📊 Dashboard Features

### Page 1: Executive Summary
- 4 KPI Cards (Total Orders, Total Cost, Avg Cost Per Order, Discontinued %)
- Total Cost by Carrier (Bar Chart)
- Total Cost by Plant (Bar Chart)
- Orders by Carrier Status (Donut Chart)
- Carrier Performance Summary (Table)

### Page 2: Cost Analysis
- Freight vs Warehouse Cost by Carrier (Stacked Bar Chart)
- Cost by Weight Range (Bar Chart)
- Weight vs Freight Cost (Scatter Chart)
- Orders Without Freight Cost (Card)

### Page 3: Carrier & Plant Performance
- Plant Capacity Utilization (Bar Chart)
- Plant Performance Summary (Table)
- Discontinued Carrier Orders (Table)
- Orders Over Time (Line Chart)

---

## 📊 Key Results

| Metric | Value |
| :--- | :--- |
| **Total Orders** | 9,215 |
| **Active Orders** | 8,361 |
| **Discontinued Orders (V44_3)** | 854 |
| **Discontinued %** | 9.27% |
| **Active Carriers** | 8 |
| **Discontinued Carriers** | 1 |
| **Master Dataset Rows** | 209,402 |
| **Master Dataset Columns** | 33 |

---

## 🧠 Business Insights

| Insight | Action |
| :--- | :--- |
| **854 orders use discontinued carrier V44_3** | Review these orders and assign new carriers |
| **Freight costs vary significantly by carrier** | Renegotiate contracts with high-cost carriers |
| **Plant utilization varies** | Optimize plant allocation |
| **Weight range impacts freight cost** | Consider consolidating shipments |

---

## 🏃 How to Run

### 1. Clone the Repository
```bash
git clone https://github.com/fatemeh231/supply-chain-optimization-pipeline.git
cd supply-chain-optimization-pipeline
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Place Your Raw File
Place `supply chain logisitcs problem.xlsx` in `data/raw/`

### 4. Run the Pipeline
```bash
python main.py
```

### 5. Open the Dashboard
- Open `output/supply_chain_dashboard.pbix` in Power BI Desktop
- The data is already connected to the Parquet file

---

## 🔧 Data Cleaning Highlights

| Challenge | Solution |
| :--- | :--- |
| **7 interconnected sheets** | Loaded all sheets, performed complex joins |
| **V44_3 discontinued carrier** | Flagged with `carrier_status` = "Discontinued" |
| **854 orders with null freight cost** | Kept nulls to preserve data integrity |
| **Weight bracket matching** | Merged OrderList with FreightRates on min/max weight |
| **Data type issues in Power BI** | Fixed in Power Query with explicit data types |
| **209,402 rows from 9,215 orders** | Each order matched multiple weight brackets |

---

## 📸 Dashboard Screenshots

### Page 1: Executive Summary
![Executive Summary](screenshots/executive_summary.png)

### Page 2: Cost Analysis
![Cost Analysis](screenshots/cost_analysis.png)

### Page 3: Carrier & Plant Performance
![Carrier Performance](screenshots/carrier_performance.png)

---

## 🚀 Future Improvements

- [ ] Add cost optimization algorithm to recommend cheapest carrier
- [ ] Add route optimization based on origin/destination ports
- [ ] Integrate with live data feeds
- [ ] Dockerize the pipeline
- [ ] Add unit tests

---

## 📬 Contact

- **LinkedIn**:https://www.linkedin.com/in/seyedeh-fatemeh-hosseininasab-7320bb322/

---

## 📄 License

This project is licensed under the **MIT License** — feel free to use it for your own portfolio or commercial projects.

---

**Built with ❤️ by Fatemeh**

---

*"Any kind of messy data can be handled—you just need the right pipeline."*
