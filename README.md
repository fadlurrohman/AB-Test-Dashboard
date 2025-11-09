# Project 1 – Marketing A/B Test KPI Dashboard

This project simulates Agoda-style performance marketing data and performs:
- KPI calculation (CTR, CVR, CPC, CPA),
- A/B test evaluation between two variants,
- Interactive dashboard for channel and country breakdowns.

## Files

- `generate_marketing_data.py` – create synthetic marketing data.
- `analyze_ab_test.py` – compute KPIs and run A/B test stats.
- `streamlit_dashboard.py` – Streamlit app for interactive exploration.
- `marketing_data.csv` – generated sample dataset (after you run the generator).

## Quick start

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt

python generate_marketing_data.py
python analyze_ab_test.py   # prints summary and A/B test result
streamlit run streamlit_dashboard.py
```
