# Deployment Guide

## Streamlit Community Cloud

### 1. Push the Project to GitHub

Run these commands from the repository root:

```bash
git add .
git commit -m "Finalize analytics project for deployment"
git push origin main
```

### 2. Prepare the Repository

Before deploying, make sure these files exist in the repo:

- `webapp/app.py`
- `requirements.txt`
- `.streamlit/config.toml`
- `outputs/csv/cleaned_orders.csv`
- `outputs/csv/rfm_table.csv`
- `outputs/csv/churn_predictions.csv`
- `outputs/csv/revenue_forecast.csv`
- `outputs/csv/executive_summary.csv`

If any output files are missing, run:

```bash
python scripts/run_pipeline.py
```

### 3. Deploy on Streamlit Community Cloud

1. Go to `https://share.streamlit.io`
2. Sign in with GitHub
3. Click `New app`
4. Select your repository
5. Choose the branch, usually `main`
6. Set the main file path to `webapp/app.py`
7. Click `Deploy`

### 4. Common Deployment Errors

#### ModuleNotFoundError
Cause:
- missing package in `requirements.txt`
- broken import path

Fix:
- update `requirements.txt`
- keep `webapp/__init__.py`, `webapp/components/__init__.py`, and `webapp/utils/__init__.py`
- redeploy after pushing changes

#### FileNotFoundError
Cause:
- required CSV outputs not committed
- app expects generated files that were not built

Fix:
- run `python scripts/run_pipeline.py`
- commit the generated files in `outputs/csv/`
- push again

#### App Loads but Pages Fail
Cause:
- one page depends on a missing dataset

Fix:
- confirm all required files exist under `outputs/csv/`
- open the app homepage and check the missing file warning

### 5. Debugging Failed Deployments

- open the Streamlit deployment logs
- read the first Python exception, not just the last line
- verify the failing import or dataset path locally
- rerun:

```bash
python -m compileall webapp scripts
python scripts/run_pipeline.py
streamlit run webapp/app.py
```

## Optional Advanced Deployment

### Custom Domain

Streamlit Community Cloud custom domain support depends on current platform settings. If available:

1. open the app settings
2. add your custom domain
3. configure the DNS record with your domain provider
4. wait for SSL provisioning

### Render

You can also deploy this as a web service on Render:

1. create a new Web Service
2. connect the GitHub repo
3. set the build command:

```bash
pip install -r requirements.txt
```

4. set the start command:

```bash
streamlit run webapp/app.py --server.port $PORT --server.address 0.0.0.0
```

### Hugging Face Spaces

Choose a Streamlit Space and point it at the same repo layout. Keep the generated CSV outputs committed so the app can load immediately on startup.

## Performance Tips

- keep dashboard inputs as precomputed CSV outputs
- use `@st.cache_data` for loaders
- avoid loading notebooks or raw files in the web app
- prefer aggregated outputs over expensive live recomputation
