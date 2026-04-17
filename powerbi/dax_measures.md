# DAX Measures

```DAX
Total Sales = SUM(cleaned_orders[sales])
Total Profit = SUM(cleaned_orders[profit])
Profit Margin % = DIVIDE([Total Profit], [Total Sales])
Total Orders = DISTINCTCOUNT(cleaned_orders[order_id])
Total Customers = DISTINCTCOUNT(cleaned_orders[customer_id])
Avg Order Value = DIVIDE([Total Sales], [Total Orders])
Avg Sales Per Customer = DIVIDE([Total Sales], [Total Customers])
At Risk Customers = CALCULATE(DISTINCTCOUNT(churn_predictions[customer_id]), churn_predictions[predicted_churn_risk] = 1)
VIP Revenue = CALCULATE(SUM(rfm_table[monetary]), rfm_table[rfm_segment] = "VIP Customers")
Forecasted Revenue Next 90 Days = SUM(revenue_forecast[yhat])
```
