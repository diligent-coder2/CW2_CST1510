# Streamlit - Multi-Domain Intelligence Platform 

## Project Overview
A unified Python and Streamlit web application designed to provide data analysis, insights, and operational capabilities for three distinct user groups: Cybersecurity Analysts, Data Scientists, and IT Administrators. 

## Addressed Problems 
Visualisatio Data Set related to the following data set: 
- **Cybersecurity:** Analyzing spikes in phishing incidents and incident response bottlenecks.
- **Data Science:** Managing large datasets, analyzing resource consumption, and recommending data governance policies.
- **IT Operations:** Identifying process inefficiencies and staff performance anomalies causing delays in ticket resolution.

## Key Technical Features
- **Secure Authentication:** Password hashing and verification using `bcrypt`.
- **Database Management:** SQL-based CRUD operations using SQLite for persistent multi-domain data storage.
- **Interactive Dashboards:** Streamlit multi-page web interface with dynamic data visualizations using Plotly/Matplotlib.
- **AI Integration:** Context-aware AI assistant powered by the OpenAI API to support analysts.

## Getting Started

1. **Create an environment using venv**
   ```bash
   # Windows
   python -m venv .venv
   # macOS and Linux
   python3 -m venv .venv
   ```

2. **Activate your environment**
   ```bash
   # Windows command prompt
   .venv\Scripts\activate.bat

   # Windows PowerShell
   .venv\Scripts\Activate.ps1

   # macOS and Linux
   source .venv/bin/activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up your environment variables:**
   - Create a .env file.
   - Add your `GROQ_API_KEY` for the AI integration to work.
   - e.g GROQ_API_KEY=your_api_key_here

5. **Run the application:**
   ```bash
   # python3 -> macOS and Linux
   python main.py
   # then, run
   streamlit run Home.py
   ```

## Author
Divine Collins – CST01510 – 2025/26