# COVID-19 Global Data Visualization Dashboard

An interactive desktop dashboard built with **PyQt5, Pandas, and Matplotlib** to explore and visualize global COVID-19 data from *Our World in Data*.

This project transforms large-scale pandemic data into an intuitive, multi-page analytical interface for structured exploration and insight generation.

---

## Features

### 1 - Data Handling
- Upload raw CSV dataset
- Automated preprocessing pipeline
- ISO-based country filtering
- Missing value handling
- Derived active case estimation

### 2 - Exploratory Data Analysis (EDA)
- Top 10 countries by total cases
- Top 10 countries by total deaths
- Correlation heatmap of key numerical indicators

### 3 - Interactive Visualizations
- Global spread over time (animated choropleth)
- Global cases vs deaths trends
- Country-specific trend analysis
- Continent-wise choropleth comparisons
- Lockdowns vs case surges (Stringency index overlay)
- Global vaccination progress
- Current vaccination snapshot

### 4 - User Experience
- Full-screen dashboard interface
- Sidebar navigation with dynamic page switching
- Interactive matplotlib toolbars (zoom, pan, export)
- Clean UI design with background theming

---

##  Project Structure
```text
src/
│── main.py                  # Application entry point (launches PyQt5 app)
│── gui.py                   # Full dashboard UI architecture using QStackedLayout
│── preprocessing.py         # Data cleaning, filtering, ISO handling, feature prep
│── visualization.py         # All matplotlib-based visualization functions
│── eda.py                   # Exploratory Data Analysis plots (Top 10, Heatmap)
│
├── assets/
│   └── background.png       # Dashboard background image
│
├── data/
│   └── README.md            # Instructions to download OWID dataset (CSV not stored)
│
├── requirements.txt         # Project dependencies
└── README.md                # Project overview and documentation

```
---

## Dataset

The dataset used is the publicly available:

**Our World in Data – COVID-19 Dataset**  
https://github.com/owid/covid-19-data/blob/master/public/data/owid-covid-data.csv

Due to GitHub file size limits, the dataset is not stored in this repository.

### To run locally:
1. Download `owid-covid-data.csv`
2. Place it inside the `data/` folder
3. Launch the application

---

## Workflow Overview
**1. Data Ingestion**

The Our World in Data COVID-19 dataset is uploaded by the user and loaded into the application.

**2. Data Preprocessing**
- Convert date column to datetime format
- Remove aggregate entities (World, continents)
- Filter valid country ISO codes
- Handle missing values
- Prepare derived metrics for analysis

**3. Exploratory Data Analysis (EDA)**
- Top 10 countries by total cases
- Top 10 countries by total deaths
- Correlation heatmap of numerical indicators

**4. Interactive Visualizations**
- Global spread over time (animated choropleth)
- Country-specific trend analysis
- Global cases vs deaths comparison
- Continent-wise impact analysis
- Lockdowns vs case surges
- Global vaccination progress
- Current global vaccination snapshot

**5. User Interaction & Controls**
All visualizations support:
- Zoom
- Pan
- Axis scaling
- ResetExport as image

## Key Features
1. Modular software architecture separating UI, preprocessing, and visualization logic
2. Multi-page dashboard built using QStackedLayout
3. Data validation before rendering plots
4. Clean user-triggered workflow (Load → Preprocess → Visualize)
5. Academic-grade documentation and report

## Tools and Libraries
- Python 3.11
- PyQt5 – Desktop UI framework
- Pandas, NumPy – Data manipulation
- Matplotlib, Seaborn – Visualization
- Plotly – Choropleth maps
- Qt Framework – GUI structure

## Installation & Run
```bash
pip install -r requirements.txt
python src/main.py
```
