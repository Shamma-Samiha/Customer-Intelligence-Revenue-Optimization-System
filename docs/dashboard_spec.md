# Power BI Dashboard Specification

## Premium Dashboard Title
Customer Intelligence & Revenue Forecasting System

## Page 1: Executive Overview
Purpose: Provide leadership with a high-level view of performance, profitability, and forward-looking revenue.
Visuals:
- KPI cards: Total Sales, Total Profit, Total Orders, Total Customers, Avg Order Value
- Monthly sales trend
- Monthly profit trend
- Revenue forecast line chart
- Segment revenue contribution
- Region summary bar chart
Filters:
- Order year
- Market
- Region
- Segment

## Page 2: Customer Intelligence
Purpose: Show how customers are distributed by value and engagement.
Visuals:
- RFM segment count chart
- Revenue by RFM segment
- Top customers by sales
- Top customers by profit
- Recency vs monetary scatter plot
- Customer detail table

## Page 3: Churn Risk
Purpose: Highlight customers most likely to go inactive.
Visuals:
- Churn-risk customer count
- Churn probability distribution
- At-risk customer table
- Top churn drivers
- Risk by RFM segment

## Page 4: Product & Profitability
Purpose: Expose where revenue is strong and where margin leaks occur.
Visuals:
- Sales by category
- Profit by category
- Profit by sub-category
- Loss-making products table
- Discount vs profit scatter plot

## Page 5: Geographic Performance
Purpose: Compare performance across countries, regions, and markets.
Visuals:
- Sales by country
- Profit by region
- Sales by market
- Map visual by country or state
- Geographic ranking table

## Recommended Model
Fact table:
- cleaned_orders

Dimension tables:
- dim_customer
- dim_product
- dim_geography
- dim_date
- rfm_table
- churn_predictions
- revenue_forecast

## DAX Measures
- Total Sales = SUM(cleaned_orders[sales])
- Total Profit = SUM(cleaned_orders[profit])
- Profit Margin % = DIVIDE([Total Profit], [Total Sales])
- Total Orders = DISTINCTCOUNT(cleaned_orders[order_id])
- Total Customers = DISTINCTCOUNT(cleaned_orders[customer_id])
- Avg Order Value = DIVIDE([Total Sales], [Total Orders])
- At Risk Customers = CALCULATE(DISTINCTCOUNT(churn_predictions[customer_id]), churn_predictions[predicted_churn_risk] = 1)
- VIP Revenue = CALCULATE(SUM(rfm_table[monetary]), rfm_table[rfm_segment] = "VIP Customers")

## Design Guidance
- Use a navy, teal, and emerald accent palette with plenty of white space.
- Keep KPI cards in a single top row.
- Place slicers in a clean left panel or slim top strip.
- Use consistent chart titles that read like business questions.
- Reserve dense tables for drill-through pages.

## Storytelling Guidance
Start with company performance, move into customer value, then risk, then operational detail. This creates a recruiter-friendly narrative that feels business-aware rather than chart-heavy.
