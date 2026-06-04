# Retail-Sales-Dashboards

A retail sales dashboard built with Streamlit, featuring a 3D animated hero section and Plotly visualizations.

## Features
- 3D animated hero visual using custom CSS/HTML
- Interactive Streamlit dashboard for sales metrics
- Plotly `line` and `scatter_3d` charts for revenue tracking
- Transaction entry form with live session state
- Inventory alerts and AI-style insights

## Run locally
1. Create a Python virtual environment:
   ```bash
   python -m venv .venv
   source .venv/bin/activate
   ```
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Start the app:
   ```bash
   streamlit run app.py
   ```

## Deploy on Streamlit Community Cloud
1. Push this repository to GitHub.
2. Sign in to [Streamlit Community Cloud](https://share.streamlit.io).
3. Click "New app", select your GitHub repo, choose `main` branch, and set `app.py` as the entry point.
4. Streamlit will deploy the app automatically.

## Notes
- The dashboard is already connected to GitHub at `https://github.com/Phantom-dcode/Retail-Sales-Dashboards`.
- `requirements.txt` is included so Streamlit Cloud can install the right dependencies.
