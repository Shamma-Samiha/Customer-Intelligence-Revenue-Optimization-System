from __future__ import annotations

import pickle
from pathlib import Path

import numpy as np
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.ensemble import RandomForestClassifier
from sklearn.impute import SimpleImputer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, confusion_matrix, precision_score, recall_score, roc_auc_score
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler


FEATURE_COLUMNS = [
    "recency",
    "frequency",
    "monetary",
    "avg_discount",
    "avg_profit",
    "total_quantity",
    "avg_order_value",
    "profit_margin",
]


def build_customer_features(df: pd.DataFrame, churn_threshold_days: int = 90) -> pd.DataFrame:
    working = df.copy()
    working["order_date"] = pd.to_datetime(working["order_date"], errors="coerce")
    snapshot_date = working["order_date"].max() + pd.Timedelta(days=1)

    customer_df = (
        working.groupby(["customer_id", "customer_name"], as_index=False)
        .agg(
            recency=("order_date", lambda x: (snapshot_date - x.max()).days),
            frequency=("order_id", "nunique"),
            monetary=("sales", "sum"),
            avg_discount=("discount", "mean"),
            avg_profit=("profit", "mean"),
            total_quantity=("quantity", "sum"),
            total_profit=("profit", "sum"),
        )
    )
    customer_df["avg_order_value"] = customer_df["monetary"] / customer_df["frequency"].replace(0, np.nan)
    customer_df["profit_margin"] = np.where(customer_df["monetary"] != 0, customer_df["total_profit"] / customer_df["monetary"], 0)
    customer_df["churn_risk"] = (customer_df["recency"] > churn_threshold_days).astype(int)
    return customer_df


def _build_models():
    numeric_transformer = Pipeline(
        steps=[
            ("imputer", SimpleImputer(strategy="median")),
            ("scaler", StandardScaler()),
        ]
    )
    preprocessor = ColumnTransformer(
        transformers=[("num", numeric_transformer, FEATURE_COLUMNS)]
    )

    logistic = Pipeline(
        steps=[
            ("preprocessor", preprocessor),
            ("classifier", LogisticRegression(max_iter=1000, class_weight="balanced", random_state=42)),
        ]
    )

    forest = Pipeline(
        steps=[
            ("preprocessor", ColumnTransformer(
                transformers=[("num", SimpleImputer(strategy="median"), FEATURE_COLUMNS)]
            )),
            ("classifier", RandomForestClassifier(
                n_estimators=250,
                random_state=42,
                class_weight="balanced_subsample",
                min_samples_leaf=3,
            )),
        ]
    )
    return {"Logistic Regression": logistic, "Random Forest": forest}


def run_churn_modeling(customer_df: pd.DataFrame, project_root: Path):
    X = customer_df[FEATURE_COLUMNS].copy()
    y = customer_df["churn_risk"].copy()

    X_train, X_test, y_train, y_test, train_idx, test_idx = train_test_split(
        X,
        y,
        customer_df.index,
        test_size=0.25,
        random_state=42,
        stratify=y,
    )

    models = _build_models()
    metrics = {}
    fitted = {}

    for name, model in models.items():
        model.fit(X_train, y_train)
        proba = model.predict_proba(X_test)[:, 1]
        preds = (proba >= 0.5).astype(int)
        metrics[name] = {
            "accuracy": accuracy_score(y_test, preds),
            "precision": precision_score(y_test, preds, zero_division=0),
            "recall": recall_score(y_test, preds, zero_division=0),
            "roc_auc": roc_auc_score(y_test, proba),
        }
        fitted[name] = {"model": model, "proba": proba, "preds": preds}

    best_model_name = max(metrics, key=lambda name: (metrics[name]["recall"], metrics[name]["roc_auc"]))
    best_model = fitted[best_model_name]["model"]

    full_proba = best_model.predict_proba(X)[:, 1]
    full_preds = (full_proba >= 0.5).astype(int)
    predictions = customer_df.copy()
    predictions["predicted_churn_risk"] = full_preds
    predictions["churn_probability"] = full_proba
    predictions = predictions.sort_values("churn_probability", ascending=False).reset_index(drop=True)

    confusion = confusion_matrix(y_test, fitted[best_model_name]["preds"])

    if best_model_name == "Random Forest":
        importances = best_model.named_steps["classifier"].feature_importances_
    else:
        importances = np.abs(best_model.named_steps["classifier"].coef_[0])

    feature_importance = (
        pd.DataFrame({"feature": FEATURE_COLUMNS, "importance": importances})
        .sort_values("importance", ascending=False)
        .reset_index(drop=True)
    )

    model_path = project_root / "outputs" / "models" / "churn_model.pkl"
    model_path.parent.mkdir(parents=True, exist_ok=True)
    with open(model_path, "wb") as file:
        pickle.dump(best_model, file)

    return {
        "metrics": metrics,
        "best_model_name": best_model_name,
        "predictions": predictions,
        "confusion_matrix": confusion,
        "feature_importance": feature_importance,
    }
