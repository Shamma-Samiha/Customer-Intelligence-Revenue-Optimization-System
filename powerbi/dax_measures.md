# DAX Measures

## Core Financial Measures

```DAX
Total Sales = SUM(cleaned_orders[sales])

Total Profit = SUM(cleaned_orders[profit])

Profit Margin % = DIVIDE([Total Profit], [Total Sales])

Total Orders = DISTINCTCOUNT(cleaned_orders[order_id])

Total Customers = DISTINCTCOUNT(cleaned_orders[customer_id])

Avg Order Value = DIVIDE([Total Sales], [Total Orders])

Avg Sales Per Customer = DIVIDE([Total Sales], [Total Customers])
```

## Customer Intelligence Measures

```DAX
VIP Customers =
CALCULATE(
    DISTINCTCOUNT(rfm_table[customer_id]),
    rfm_table[rfm_segment] = "VIP Customers"
)

VIP Revenue =
CALCULATE(
    SUM(rfm_table[monetary]),
    rfm_table[rfm_segment] = "VIP Customers"
)

At Risk Segment Customers =
CALCULATE(
    DISTINCTCOUNT(rfm_table[customer_id]),
    rfm_table[rfm_segment] = "At Risk Customers"
)

Avg Customer Recency =
AVERAGE(rfm_table[recency])
```

## Churn Measures

```DAX
Predicted At Risk Customers =
CALCULATE(
    DISTINCTCOUNT(churn_predictions[customer_id]),
    churn_predictions[predicted_churn_risk] = 1
)

Average Churn Probability =
AVERAGE(churn_predictions[churn_probability])

High Risk Customers Over 80% =
CALCULATE(
    DISTINCTCOUNT(churn_predictions[customer_id]),
    churn_predictions[churn_probability] >= 0.8
)
```

## Forecast Measures

```DAX
Forecast Revenue Next 90 Days =
SUM(revenue_forecast[yhat])

Average Daily Forecast =
AVERAGE(revenue_forecast[yhat])

Forecast Upper Band =
SUM(revenue_forecast[yhat_upper])

Forecast Lower Band =
SUM(revenue_forecast[yhat_lower])
```

## Recommended Relationships

- `cleaned_orders[customer_id]` -> `rfm_table[customer_id]`
- `cleaned_orders[customer_id]` -> `churn_predictions[customer_id]`
- `cleaned_orders[order_date]` -> `dim_date[date]`
- `revenue_forecast[ds]` -> `dim_date[date]`

Use single-direction filtering from dimensions into fact tables and keep `rfm_table`, `churn_predictions`, and `revenue_forecast` as dashboard support tables rather than raw transaction replacements.
