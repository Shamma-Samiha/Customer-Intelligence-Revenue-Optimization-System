# Customer Intelligence & Revenue Forecasting System

An end-to-end analytics portfolio project that transforms retail transaction data into executive KPIs, exploratory insights, RFM customer segmentation, churn-risk scoring, revenue forecasting, dashboard-ready outputs, a Power BI specification, and a polished web app.

## Business Problem
Retail teams need more than historical reporting. They need a system that explains performance, identifies valuable and at-risk customers, highlights profit leakage, and supports forward-looking planning.

## Project Objectives
- Load and validate raw retail data
- Clean and standardize the transactional dataset
- Perform recruiter-ready exploratory analysis
- Segment customers using RFM logic
- Build a proxy churn-risk model
- Forecast revenue for the next 90 days
- Deliver dashboard-ready exports for Power BI and Streamlit

## Tools Used
- Python
- pandas
- seaborn
- matplotlib
- scikit-learn
- Streamlit
- Plotly
- Power BI design specification

## Repository Structure
```text
data/          raw, cleaned, and processed datasets
notebooks/     end-to-end analysis notebooks
scripts/       reusable analytics modules and pipeline runner
outputs/       exported CSVs and model artifacts
powerbi/       DAX measures, theme, and dashboard spec support
webapp/        portfolio-ready Streamlit app
docs/          planning, insight, and dashboard documentation
```

## Notebook Workflow
1. `01_data_loading.ipynb`
2. `02_data_cleaning.ipynb`
3. `03_eda.ipynb`
4. `04_rfm_segmentation.ipynb`
5. `05_churn_analysis.ipynb`
6. `06_revenue_forecasting.ipynb`

## Key Outputs
- `data/cleaned/superstore_cleaned.csv`
- `outputs/csv/rfm_table.csv`
- `outputs/csv/churn_predictions.csv`
- `outputs/csv/revenue_forecast.csv`
- `data/processed/executive_kpis.csv`

## How to Run
```bash
pip install -r requirements.txt
python scripts/run_pipeline.py
streamlit run webapp/app.py
```

## Power BI Dashboard
The `docs/dashboard_spec.md` and `powerbi/dax_measures.md` files define a recruiter-ready multi-page Power BI dashboard covering executive performance, customer intelligence, churn risk, product profitability, and geographic performance.

## Website App
The Streamlit app presents this project as a polished analytics product with executive metrics, customer intelligence views, churn-risk monitoring, and revenue forecasting.

## Key Insights
- Revenue scale is meaningful, but quality varies across products, geographies, and customer groups.
- Customer behavior can be turned into clear value segments through RFM scoring.
- Inactivity-based churn signals help prioritize retention outreach before revenue decays further.
- Forecasting gives the project a forward-looking layer that strengthens business relevance.

## Resume-Ready Summary
Built an end-to-end retail analytics system using Python, machine learning, forecasting, dashboard design, and web app delivery to generate customer intelligence, churn-risk insights, and 90-day revenue forecasts from transactional sales data.
