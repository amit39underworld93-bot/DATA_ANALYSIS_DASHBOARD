# Titanic Data Analysis Dashboard 🛳️📊

An interactive, end-to-end Exploratory Data Analysis (EDA) dashboard built to analyze the famous Titanic passenger dataset.
This application transforms raw CSV data into a dynamic, visual narrative, allowing users to filter demographics in real-time and uncover statistical survival patterns.

## 🚀 Key Features 

- **Real-Time Interactive Filtering:** A dynamic sidebar with multi-variable filters (Gender, Passenger Class, Age Range, Embarkation Port, and Travel Status) 
  that instantly updates all metrics and charts across the dashboard.

- **Automated Data Cleaning:** Implements real-time data preprocessing, including missing value imputation (using statistical mode for embarkation ports) and categorical mapping.

- **Dynamic KPI Tracking:** Instantly recalculates core metrics—Total Passengers, Survivor count, Survival Rate, and Average Fare—based on active user filters.

- **Advanced Visualizations:** Utilizes Plotly Express to render publication-ready, interactive charts, including:

  - Bar charts for demographic distributions (Gender, Class, SibSp/Parch).

  - Histograms and Box Plots for continuous variables (Age, Fare).
    
  - Stacked/grouped analysis correlating demographics directly to survival rates.

- **Statistical Insights & Correlation:** Automatically calculates Pearson correlation coefficients between continuous features and survival, generating a live summary of actionable insights.

## 🛠️ Tech Stack

**Language:** Python 3

**Frontend/Framework:** Streamlit (for building the interactive web interface)

**Data Manipulation:** Pandas

**Data Visualization:** Plotly Express

## 💻 How to Run (Installation & Execution)

*Follow these steps to run the dashboard on your local machine:*

1. **Clone the repository:**
   git clone https://github.com/amit39underworld93-bot/DATA_ANALYSIS_DASHBOARD.git cd DATA_ANALYSIS_DASHBOARD

2. **Install dependencies:**
   *This project requires Streamlit, Pandas, and Plotly. Ensure they are installed in your environment.*

   `pip install streamlit pandas plotly`

3. **Execute the dashboard:**
   Unlike standard Python scripts, Streamlit applications require the `streamlit run` command.

   `streamlit run titanic_dashboard.py`

## 📸 Usage Overview

*Upon running the command, a local web server will launch, and the dashboard will automatically open in your default web browser (typically at `http://localhost:8501`).*

**Navigation Sections:**

1. **Dataset Overview:** View raw data previews, missing value counts, and feature dictionaries.

2. **Interactive Filters (Sidebar):** Slice the dataset by specific passenger criteria.

3. **Passenger Profile Analysis:** Explore distributions of age, fare, and family sizes.

4. **Survival Patterns:** Analyze exactly which factors (class, gender, travel status) contributed to higher survival rates.

5. **Detailed Data & Final Insight:** View the exact filtered data table alongside a dynamically generated final conclusion.



