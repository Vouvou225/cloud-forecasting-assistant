# Cloud Forecasting Q&A App

This Streamlit application connects to BigQuery to analyze and visualize cloud cost forecast data.
It uses Google's Gemini AI to answer user questions about trends, anomalies, and optimization.

## Features

- Load data from BigQuery
- Select X (date) and Y (cost) columns
- Filter by date range
- Line chart visualization
- Control how many rows are sent to Gemini
- Ask natural-language questions
- Save Q&A responses
- Export filtered forecast to CSV

## To Run

1. Install requirements:

```bash
pip install -r requirements.txt
```

2. Set your Gemini API key:

```bash
export GOOGLE_API_KEY=your_api_key_here
```

3. Run the app:

```bash
streamlit run app.py
```
