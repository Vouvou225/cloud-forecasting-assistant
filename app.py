import streamlit as st
import google.generativeai as genai
import pandas as pd
from google.cloud import bigquery

# --- CONFIGURATION ---
GOOGLE_API_KEY = "fff"  # Replace with os.getenv("GOOGLE_API_KEY") for security
MODEL_NAME = "models/gemini-1.5-pro-latest"
genai.configure(api_key=GOOGLE_API_KEY)
model = genai.GenerativeModel(MODEL_NAME)
chat = model.start_chat()

# --- SYSTEM PROMPT ---
SYSTEM_PROMPT = """
You are a cloud FinOps assistant that analyzes cloud cost forecast data. You are given time series data for future dates. Answer user questions analytically and clearly, and identify any trends, spikes, or savings opportunities.
"""

# --- INITIAL STATE ---
if "data_loaded" not in st.session_state:
    st.session_state.data_loaded = False
if "df" not in st.session_state:
    st.session_state.df = None
if "forecast_data" not in st.session_state:
    st.session_state.forecast_data = ""

# --- UI ---
st.title("💸 Cloud Forecasting Q&A (FinOps Assistant)")

st.markdown("### 📊 Load forecast data from BigQuery")
if st.button("Load forecast data") or st.session_state.data_loaded:
    if not st.session_state.data_loaded:
        try:
            client = bigquery.Client()
            query = "SELECT * FROM `omes-datascience-sbx.GCP_Billing.AzureCostdata`"
            query_job = client.query(query)
            df = query_job.to_dataframe()
            st.session_state.df = df
            st.session_state.data_loaded = True
        except Exception as e:
            st.error(f"Error loading data from BigQuery: {e}")
            st.stop()

    df = st.session_state.df
    st.success("✅ Forecast data loaded.")
    st.dataframe(df)

    # --- Column Selection ---
    st.markdown("### 🔧 Select Forecast Columns")

    datetime_cols = [col for col in df.columns if pd.api.types.is_datetime64_any_dtype(df[col]) or 'date' in col.lower()]
    numeric_cols = [col for col in df.columns if pd.api.types.is_numeric_dtype(df[col])]

    if not datetime_cols or not numeric_cols:
        st.error("❌ Need at least one date/time column and one numeric column.")
        st.stop()

    col1 = st.selectbox("📅 X-axis (Date)", datetime_cols)
    col2 = st.selectbox("💰 Y-axis (Cost or Value)", numeric_cols)

    # Convert col1 to datetime if not already
    try:
        df[col1] = pd.to_datetime(df[col1])
    except:
        pass

    # --- Date Filtering ---
    st.markdown("### 📅 Filter by Date Range")
    min_date, max_date = df[col1].min(), df[col1].max()
    date_range = st.date_input("Select range", value=(min_date, max_date), min_value=min_date, max_value=max_date)
    if len(date_range) == 2:
        df = df[(df[col1] >= pd.to_datetime(date_range[0])) & (df[col1] <= pd.to_datetime(date_range[1]))]

    # --- Export CSV ---
    st.download_button("⬇️ Download filtered data", df.to_csv(index=False), file_name="filtered_forecast.csv")

    # --- Chart ---
    st.markdown("### 📈 Forecast Trend")
    st.line_chart(df[[col1, col2]].set_index(col1).sort_index())

    # --- Row limit for Gemini ---
    st.markdown("### ⚙️ Gemini Input Settings")
    row_limit = st.slider("How many rows to send to Gemini (for context)?", min_value=10, max_value=500, value=100, step=10)
    trimmed_df = df[[col1, col2]].dropna().head(row_limit)
    forecast_data = "\n".join([f"{row[col1]}    {row[col2]}" for _, row in trimmed_df.iterrows()])
    st.session_state.forecast_data = forecast_data

    # --- Q&A Interface ---
    st.markdown("### 🤖 Ask a question about the forecast")
    st.markdown("*Example questions:*")
    st.markdown("- What is the overall trend in the forecasted costs?\n- Are there any spikes or anomalies?\n- What are the top 5 most expensive forecasted dates?\n- How can we reduce forecasted spending?")

    user_question = st.text_input("Your question")
    if user_question:
        prompt = f"{SYSTEM_PROMPT}\n\nForecast data:\n{forecast_data}\n\nUser question:\n{user_question}"
        with st.spinner("Thinking..."):
            response = chat.send_message(prompt)
        st.success("Gemini response:")
        st.markdown(response.text)

        if st.checkbox("📩 Save this response"):
            result_row = pd.DataFrame([[user_question, response.text]], columns=["question", "answer"])
            result_row.to_csv("responses.csv", mode='a', header=False, index=False)
            st.info("Saved to responses.csv")

else:
    st.info("Click the button to load forecast data from BigQuery.")
