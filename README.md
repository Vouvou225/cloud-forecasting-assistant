# 💸 Cloud Forecasting Q&A Assistant

An interactive [Streamlit](https://streamlit.io) app for analyzing and exploring cloud cost forecast data using BigQuery and Google Gemini AI.

This assistant helps you visualize trends, detect anomalies, ask natural-language questions, and discover savings opportunities in your cloud spend.

---

## 🚀 Features

✅ Load forecast data directly from **BigQuery**  
✅ Select **date** and **cost** columns dynamically  
✅ Filter by **date range**  
✅ Visualize trends using interactive **line charts**  
✅ Ask Gemini AI custom questions based on forecast data  
✅ Adjust **row limit** to control data sent to AI  
✅ **Export** filtered data to CSV  
✅ Save AI **Q&A history** for future reference  

---

## 🖼️ App Preview

![Cloud Forecasting App Demo](https://user-images.githubusercontent.com/yourusername/demo-screenshot.png)

---

## 🛠️ Setup & Usage

### 1. Clone the Repository
```bash
git clone https://github.com/YOUR_USERNAME/cloud-forecasting-assistant.git
cd cloud-forecasting-assistant



2. Install Dependencies
pip install -r requirements.txt

3. Set Your Google Gemini API Key
export GOOGLE_API_KEY="your-api-key-here"

4. Run the App
streamlit run app.py



🤖 Example Questions to Ask Gemini
"What is the overall trend in the forecasted cloud costs?"

"Are there any spikes or unusual drops?"

"What are the top 5 most expensive forecasted dates?"

"Where are the best cost-saving opportunities?"


📂 Project Structure
cloud-forecasting-assistant/
├── app.py                # Main Streamlit app
├── requirements.txt      # Python dependencies
├── responses.csv         # Optional: stores saved Q&A
├── README.md             # Project documentation


🌐 Technologies Used
Streamlit – interactive data apps

Google BigQuery – cloud billing data source

Google Gemini – AI Q&A model

Pandas – data transformation

Matplotlib / Streamlit charting – visualization

🧾 License
This project is open-source and free to use. MIT License.

