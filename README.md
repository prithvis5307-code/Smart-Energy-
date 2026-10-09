# Electricity Consumption Analysis Dashboard

An interactive, multi-page Streamlit web application for analysing campus electricity consumption data from Aug 2013 to Dec 2017.

## Dataset
- **File:** `dataset/allpower.csv`
- **Columns:** `timestamp` (Unix seconds) + 9 building power channels in Watts:
  `Academic`, `Boys_main`, `Boys_backup`, `Facilities`, `Girls_main`, `Girls_backup`, `Lecture`, `Library`, `Mess`
- **Readings:** ~2.3 million rows at 1-minute intervals

## Features

| Page | What it shows |
|------|---------------|
| **Dashboard** | KPI cards, daily energy trend with anomalies, hourly bar chart, building power bar chart |
| **Consumption Analysis** | Year filter + 4 tabs: building-wise bar + pie, hourly line + heat-map, daily line + rolling average, monthly bar + stats |
| **Anomaly Detection** | IQR-based anomaly flags, anomaly table, building comparison (normal vs anomalous), hourly profile comparison |
| **Recommendations** | 8 data-driven energy-saving recommendations with expandable details |
| **Data Quality** | Missing-data table, bar chart, coverage over time line chart, monthly missing-data heat-map |

## Setup

```bash
# Install dependencies
pip install -r requirements.txt

# Run the app
streamlit run app.py
```

Then open **http://localhost:8501** in your browser.

## Calculations
- Power readings are in **Watts (W)**
- `total_power_W = sum of all building readings` (NaN-safe, using `min_count=1`)
- `energy_kwh = total_power_W / 1000 / 60`  (one 1-minute reading = 1/60th of an hour)
- Missing readings are preserved as NaN and never treated as zero

## Project Structure
```
Code/
├── app.py               # Main Streamlit application
├── requirements.txt     # Python dependencies
├── README.md            # This file
├── dataset/
│   └── allpower.csv     # Raw electricity dataset (unchanged)
└── analysis/
    └── analysis.py      # Original analysis script
```
