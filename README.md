# Titanic Data Analysis Dashboard 🛳️📊

An interactive, end-to-end Exploratory Data Analysis (EDA) dashboard built to analyze the famous Titanic passenger dataset.
This application transforms raw CSV data into a dynamic, visual narrative, allowing users to filter demographics in real-time and uncover statistical survival patterns.

# 🚀 Key Features 

- **Real-Time Interactive Filtering:** A dynamic sidebar with multi-variable filters (Gender, Passenger Class, Age Range, Embarkation Port, and Travel Status) 
  that instantly updates all metrics and charts across the dashboard.

- **Automated Data Cleaning:** Implements real-time data preprocessing, including missing value imputation (using statistical mode for embarkation ports) and categorical mapping.

- **Dynamic KPI Tracking:** Instantly recalculates core metrics—Total Passengers, Survivor count, Survival Rate, and Average Fare—based on active user filters.

- **Advanced Visualizations:** Utilizes Plotly Express to render publication-ready, interactive charts, including:

  - Bar charts for demographic distributions (Gender, Class, SibSp/Parch).

  - Histograms and Box Plots for continuous variables (Age, Fare).
    
  - Stacked/grouped analysis correlating demographics directly to survival rates.
