# Power BI Dashboard Specification

## Dashboard Title
Customer Intelligence & Revenue Forecasting System

## Subtitle
From retail transactions to customer strategy, churn-risk monitoring, and revenue planning

## Recommended Data Model

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

## Relationships

- `cleaned_orders[order_date]` many-to-one -> `dim_date[date]`
- `revenue_forecast[ds]` many-to-one -> `dim_date[date]`
- `cleaned_orders[customer_id]` many-to-one -> `dim_customer[customer_id]`
- `rfm_table[customer_id]` many-to-one -> `dim_customer[customer_id]`
- `churn_predictions[customer_id]` many-to-one -> `dim_customer[customer_id]`
- `cleaned_orders[product_id]` many-to-one -> `dim_product[product_id]`
- `cleaned_orders[region/state/country]` many-to-one -> `dim_geography`

Keep relationship direction single from dimensions to facts. Avoid bidirectional filtering unless a drill-through use case truly requires it.

## Page 1: Executive Overview
Purpose: Give leadership a fast read on performance, margin quality, and forward-looking revenue.

Visuals:
- KPI cards: Total Sales, Total Profit, Profit Margin %, Total Orders, Total Customers, Avg Order Value
- Monthly sales trend line
- Monthly profit trend line
- Revenue forecast chart with upper/lower band
- Sales by region bar chart
- Revenue by segment stacked bar

Slicers:
- Order Year
- Market
- Region
- Customer Segment

## Page 2: Customer Intelligence
Purpose: Show how customer value is distributed and where retention effort should concentrate.

Visuals:
- Customer count by RFM segment
- Revenue contribution by RFM segment
- Recency vs monetary scatter plot
- Top customers by revenue
- Top customers by profit
- Customer detail table with recency, frequency, monetary, churn probability

Drill-through:
- Customer profile page by `customer_id`

## Page 3: Churn Risk
Purpose: Surface the customers most likely to go inactive and explain the size of the risk pool.

Visuals:
- Predicted at-risk customer KPI
- Average churn probability KPI
- Churn probability histogram
- High-risk customer table
- Churn risk by region
- Churn risk by RFM segment

## Page 4: Product & Profitability
Purpose: Reveal which products and categories create profitable scale and which destroy margin.

Visuals:
- Sales by category
- Profit by category
- Profit by sub-category
- Top products by sales
- Loss-making products table
- Discount vs profit scatter plot

## Page 5: Geographic Performance
Purpose: Compare country, region, and market performance to identify leaders and laggards.

Visuals:
- Sales by country map
- Profit by region column chart
- Sales by market chart
- Geographic ranking matrix
- Filtered product/category performance by region

## Visual Design Recommendations

- Use a navy base with teal and emerald accents for KPIs and positive results.
- Use rose/red sparingly for churn and loss signals.
- Keep KPI cards in the top band with generous padding.
- Place slicers in a left rail or top strip with consistent ordering.
- Use no more than 5-6 visuals per page to maintain readability.
- Add short page subtitles so the dashboard feels like a guided business story.

## Recruiter-Focused Storytelling Flow

1. Start with company performance and revenue trend.
2. Move into customer value through RFM.
3. Transition into churn risk and retention urgency.
4. Show operational detail through product and profitability.
5. Finish with geographic scale and market opportunity.

This structure makes the dashboard feel strategic rather than purely descriptive.
