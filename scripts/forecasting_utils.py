from __future__ import annotations

import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression


def prepare_daily_sales(df: pd.DataFrame) -> pd.DataFrame:
    working = df.copy()
    working["order_date"] = pd.to_datetime(working["order_date"], errors="coerce")
    daily = (
        working.groupby("order_date", as_index=False)["sales"]
        .sum()
        .sort_values("order_date")
    )
    return daily


def _prophet_forecast(daily_sales: pd.DataFrame, horizon: int):
    from prophet import Prophet

    prophet_df = daily_sales.rename(columns={"order_date": "ds", "sales": "y"})
    model = Prophet(yearly_seasonality=True, weekly_seasonality=True, daily_seasonality=False)
    model.fit(prophet_df)
    future = model.make_future_dataframe(periods=horizon)
    forecast = model.predict(future)[["ds", "yhat", "yhat_lower", "yhat_upper"]]
    return forecast, "Prophet"


def _regression_forecast(daily_sales: pd.DataFrame, horizon: int):
    data = daily_sales.copy().sort_values("order_date").reset_index(drop=True)
    data["t"] = np.arange(len(data))
    data["dow"] = data["order_date"].dt.dayofweek
    data["month"] = data["order_date"].dt.month
    data["dayofyear"] = data["order_date"].dt.dayofyear
    data["sin_year"] = np.sin(2 * np.pi * data["dayofyear"] / 365.25)
    data["cos_year"] = np.cos(2 * np.pi * data["dayofyear"] / 365.25)

    train_X = pd.get_dummies(data[["t", "dow", "month", "sin_year", "cos_year"]], columns=["dow", "month"], drop_first=False)
    model = LinearRegression()
    model.fit(train_X, data["sales"])

    future_dates = pd.date_range(data["order_date"].max() + pd.Timedelta(days=1), periods=horizon, freq="D")
    future = pd.DataFrame({"ds": future_dates})
    future["t"] = np.arange(len(data), len(data) + horizon)
    future["dow"] = future["ds"].dt.dayofweek
    future["month"] = future["ds"].dt.month
    future["dayofyear"] = future["ds"].dt.dayofyear
    future["sin_year"] = np.sin(2 * np.pi * future["dayofyear"] / 365.25)
    future["cos_year"] = np.cos(2 * np.pi * future["dayofyear"] / 365.25)
    future_X = pd.get_dummies(future[["t", "dow", "month", "sin_year", "cos_year"]], columns=["dow", "month"], drop_first=False)
    future_X = future_X.reindex(columns=train_X.columns, fill_value=0)

    preds = model.predict(future_X)
    residual_std = np.std(data["sales"] - model.predict(train_X))

    forecast = pd.DataFrame(
        {
            "ds": future["ds"],
            "yhat": preds,
            "yhat_lower": preds - 1.96 * residual_std,
            "yhat_upper": preds + 1.96 * residual_std,
        }
    )
    history = daily_sales.rename(columns={"order_date": "ds", "sales": "yhat"}).copy()
    history["yhat_lower"] = history["yhat"]
    history["yhat_upper"] = history["yhat"]
    return pd.concat([history, forecast], ignore_index=True), "Seasonal Linear Regression"


def generate_revenue_forecast(daily_sales: pd.DataFrame, horizon: int = 90):
    try:
        return _prophet_forecast(daily_sales, horizon)
    except Exception:
        return _regression_forecast(daily_sales, horizon)
