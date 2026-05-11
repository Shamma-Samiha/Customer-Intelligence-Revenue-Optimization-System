# Dashboard Specification

## Dashboard Title

Customer Intelligence & Revenue Forecasting System

## Dashboard Purpose

Give business users a clear view of sales performance, customer value, churn risk, and revenue outlook from a single retail dataset.

## Streamlit Website Pages

### 1. Executive Overview

Purpose: Give a fast operating snapshot of sales, profit, order volume, region performance, and segment mix.

Key elements:
- KPI cards for sales, profit, average order value, and profit margin
- Monthly sales and profit trends
- Sales by region
- Sales by customer segment
- Sidebar filters for year, market, and region

### 2. Customer Intelligence

Purpose: Show which customers and RFM segments create the most value.

Key elements:
- Total customers, average revenue, top segment, and average recency
- RFM segment distribution
- Revenue share by segment
- Recency vs revenue scatter plot
- Frequency vs revenue scatter plot
- Highest-value customer table with CSV export
- Sidebar controls for segment, minimum revenue, and number of customers shown

### 3. Churn Risk

Purpose: Help users prioritize customers who may need retention outreach.

Key elements:
- Churn rate, high-risk customer count, average risk, and average recency
- Churn probability distribution
- Customers by risk band
- Feature importance signals
- Highest-risk customer table with CSV export
- Sidebar controls for risk threshold, minimum revenue at risk, and review count

### 4. Revenue Forecast

Purpose: Compare recent revenue history with the forecast window for planning.

Key elements:
- Forecasted revenue, growth rate, horizon length, and peak forecast day
- Historical vs forecast revenue
- Forecast trend
- Weekly forecasted revenue
- Recent historical revenue
- Forecast preview table with CSV export
- Sidebar controls for forecast horizon and history window

## Power BI Model Recommendation

### Fact Tables

- `cleaned_orders`
- `revenue_forecast`

### Analytical Support Tables

- `rfm_table`
- `churn_predictions`

### Dimensions

- `dim_date`
- `dim_customer`
- `dim_product`
- `dim_geography`

## Relationship Guidance

- Use one-to-many relationships from dimensions to fact tables.
- Keep filter direction single unless a drill-through requirement needs otherwise.
- Connect customer-level analytical tables through `customer_id`.
- Connect forecast data to the date dimension through `ds`.

## Visual Design Guidance

- Use a dark navy base with teal and blue accents.
- Use rose/red only for risk, loss, or warning signals.
- Keep KPI cards at the top of each page.
- Keep charts readable, with no more than two main visuals per row.
- Use short subtitles that explain what the user should review next.
