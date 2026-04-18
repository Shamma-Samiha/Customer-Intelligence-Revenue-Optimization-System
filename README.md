# Customer Intelligence & Revenue Forecasting System

An end-to-end retail analytics portfolio project that combines data engineering, business analysis, customer intelligence, machine learning, forecasting, Power BI design, and a deployable Streamlit dashboard into one recruiter-ready system.

## Project Overview

Retail organizations often have rich transaction history but limited visibility into which customers matter most, where profit is leaking, who is likely to churn, and how revenue is expected to move next. This project turns retail order data into a practical decision-support system built for both business storytelling and technical credibility.

## Problem Statement

Leadership teams need more than static sales reports. They need:

- a trusted cleaned dataset
- clear KPI reporting
- customer segmentation that supports targeting
- churn-risk signals for retention planning
- a forward-looking revenue forecast
- dashboards that communicate insights cleanly

## Solution Approach

This project follows a realistic analytics lifecycle:

1. Load and inspect raw retail transaction data
2. Clean and standardize the dataset for reuse
3. Perform broad exploratory data analysis
4. Build RFM-based customer segmentation
5. Create a proxy churn-risk model from transaction behavior
6. Forecast the next 90 days of revenue
7. Export dashboard-ready datasets
8. Deliver insights through Power BI design and a deployed Streamlit app

## Tools and Technologies

- Python
- pandas
- NumPy
- matplotlib
- seaborn
- scikit-learn
- Plotly
- Streamlit
- Power BI

## Key Deliverables

- Six structured analytics notebooks
- Modular Python pipeline scripts
- Dashboard-ready CSV outputs
- Recruiter-ready Streamlit web app
- Power BI dashboard layout and DAX pack
- Documentation for project planning, business insights, and dashboard design

## Repository Structure

```text
data/
  raw/            source dataset
  cleaned/        cleaned canonical dataset
  processed/      app-ready and dashboard-ready intermediate exports

notebooks/        analysis workflow from loading to forecasting
scripts/          reusable ETL, RFM, churn, forecasting, and export logic
outputs/          final csv outputs, model files, and visual assets
powerbi/          DAX measures, theme, and dashboard design assets
webapp/           deployable multi-page Streamlit app
docs/             project plan, dashboard specification, and business insights
```

## Analytics Workflow

### 1. Data Loading
- raw CSV ingestion with encoding fallback
- schema inspection
- missing value and duplicate checks

### 2. Data Cleaning
- standardized column names
- date conversion
- corrupt or utility column removal
- time feature engineering
- profit margin creation

### 3. Exploratory Analysis
- executive KPIs
- time trends and seasonality
- geographic performance
- product and profitability analysis
- customer concentration analysis

### 4. RFM Segmentation
- customer recency, frequency, and monetary scoring
- segment creation for VIP, loyal, regular, new, and at-risk customers
- segment-level value analysis

### 5. Churn-Risk Analysis
- inactivity-based churn definition
- customer feature engineering
- baseline classification models
- churn probability scoring

### 6. Revenue Forecasting
- daily sales aggregation
- 90-day forecast generation
- forecast output for planning dashboards

## Dashboard Layer

### Streamlit Web App
The app presents the project as a polished business analytics product with:

- executive overview
- customer intelligence page
- churn-risk page
- revenue forecast page
- methodology page

Entry point:

```bash
streamlit run webapp/app.py
```

### Power BI Dashboard
The Power BI design pack includes:

- multi-page dashboard specification
- recommended table relationships
- DAX measures
- visual storytelling guidance

See:

- [docs/dashboard_spec.md](docs/dashboard_spec.md)
- [powerbi/dax_measures.md](powerbi/dax_measures.md)

## Key Output Files

- `data/cleaned/superstore_cleaned.csv`
- `data/processed/cleaned_orders.csv`
- `data/processed/executive_kpis.csv`
- `outputs/csv/rfm_table.csv`
- `outputs/csv/churn_predictions.csv`
- `outputs/csv/revenue_forecast.csv`

## Screenshots

Add screenshots here after deployment:

- `docs/screenshots/streamlit_home.png`
- `docs/screenshots/customer_intelligence.png`
- `docs/screenshots/churn_dashboard.png`
- `docs/screenshots/powerbi_executive_overview.png`

## How to Run Locally

```bash
pip install -r requirements.txt
python scripts/run_pipeline.py
streamlit run webapp/app.py
```

## Deployment

This project is structured for Streamlit Community Cloud deployment using `webapp/app.py` as the entry point. The app uses repository-relative paths and cached CSV loading to stay deployment-safe.

## Business Impact

This project helps decision-makers:

- understand where sales and profit come from
- identify high-value and at-risk customers
- prioritize retention and reactivation activity
- spot profit leakage by category and geography
- plan ahead using forecasted revenue

## Recruiter Summary

Built a full analytics product around retail transaction data using Python, scikit-learn, Streamlit, and Power BI design principles to deliver customer segmentation, churn-risk monitoring, revenue forecasting, and executive-ready dashboards.
