from __future__ import annotations

from pathlib import Path

from data_utils import clean_superstore_data, get_project_root, load_raw_data
from rfm_utils import build_rfm_table
from churn_utils import build_customer_features, run_churn_modeling
from forecasting_utils import prepare_daily_sales, generate_revenue_forecast
from export_utils import build_executive_kpis, export_csv


def main() -> None:
    project_root = get_project_root(Path.cwd())

    raw_df = load_raw_data(project_root)
    cleaned_df = clean_superstore_data(raw_df)
    export_csv(cleaned_df, project_root / "data" / "cleaned" / "superstore_cleaned.csv")
    export_csv(cleaned_df, project_root / "data" / "processed" / "cleaned_orders.csv")
    export_csv(cleaned_df, project_root / "outputs" / "csv" / "cleaned_orders.csv")

    executive_kpis = build_executive_kpis(cleaned_df)
    export_csv(executive_kpis, project_root / "data" / "processed" / "executive_kpis.csv")
    export_csv(executive_kpis, project_root / "outputs" / "csv" / "executive_summary.csv")

    rfm_df = build_rfm_table(cleaned_df)
    export_csv(rfm_df, project_root / "outputs" / "csv" / "rfm_table.csv")
    export_csv(rfm_df, project_root / "data" / "processed" / "customer_level_features.csv")

    customer_features = build_customer_features(cleaned_df, churn_threshold_days=90)
    churn_results = run_churn_modeling(customer_features, project_root)
    export_csv(churn_results["predictions"], project_root / "outputs" / "csv" / "churn_predictions.csv")

    daily_sales = prepare_daily_sales(cleaned_df)
    forecast_df, _ = generate_revenue_forecast(daily_sales, horizon=90)
    export_csv(daily_sales, project_root / "data" / "processed" / "forecast_input_daily_sales.csv")
    export_csv(forecast_df, project_root / "outputs" / "csv" / "revenue_forecast.csv")

    print("Pipeline completed successfully.")


if __name__ == "__main__":
    main()
