import pandas as pd
import streamlit as st
import plotly.express as px

# ==================================================================================================================================================================
# PAGE CONFIGURATION
# ==================================================================================================================================================================

st.set_page_config(
    page_title = "Titanic Data Analysis Dashboard", 
    page_icon = "🛳️",
    layout = "wide"
)

# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# SECTION 1: OVERVIEW AND DATASET INFORMATION
# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

# ==================================================================================================================================================================
# LOAD DATASET
# ==================================================================================================================================================================

df = pd.read_csv("titanic.csv")

# ==================================================================================================================================================================
# DATA CLEANING
# ==================================================================================================================================================================

df_clean = df.copy()

embarked_mode = df_clean["embarked"].mode()[0]

df_clean["embarked"] = df_clean["embarked"].fillna(embarked_mode)

embark_town_mapping = {
    "S": "Southampton",
    "C": "Cherbourg",
    "Q": "Queenstown"
}

df_clean["embark_town"] = df_clean["embark_town"].fillna(df_clean["embarked"].map(embark_town_mapping))

# ==================================================================================================================================================================
# SECTION 1: OVERVIEW
# ==================================================================================================================================================================

st.title("🛳️ Titanic Data Analysis Dashboard")

st.write(
    """
This interactive dashboard explores the Titanic passenger dataset, focusing on passenger characteristics, data quality, and survival patterns.
    """
)

st.divider()

# ==================================================================================================================================================================
# DATASET OVERVIEW
# ==================================================================================================================================================================

st.header("📊 Dataset Overview")

rows, columns = df.shape

total_missing_values = df.isnull().sum().sum()

duplicated_rows = df.duplicated().sum()

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("Total Passengers: ", rows)

with col2: 
    st.metric("Original Features: ", columns)

with col3: 
    st.metric("Total Missing Values: ", total_missing_values)

with col4:
    st.metric("Exact Duplicate Rows", duplicated_rows)

st.divider()

# ==================================================================================================================================================================
# DATASET PREVIEW
# ==================================================================================================================================================================

st.subheader("🔍 Dataset Preview")

st.dataframe(df_clean.head(), use_container_width = True)

st.divider()

# ==================================================================================================================================================================
# DATA QUALITY
# ==================================================================================================================================================================

st.subheader("🧹 Data Quality")

data_quality = pd.DataFrame({
    "Column": df.columns,
    "Data Type": df.dtypes.astype(str).values,
    "Missing Values": df.isnull().sum().values, 
    "Missing Percentage" : (df.isnull().sum().values/len(df)*100).round(2)
})

st.dataframe(data_quality, use_container_width = True, hide_index = True)

st.divider()

# ==================================================================================================================================================================
# FEATURE INFORMATION
# ==================================================================================================================================================================

st.subheader("📋 Dataset Features")

feature_description = (
    {
            "Feature": [
                "survived",
                "pclass",
                "sex",
                "age",
                "sibsp",
                "parch",
                "fare",
                "embarked",
                "class",
                "who",
                "adult_male",
                "deck",
                "embarked_town",
                "alive",
                "alone"
    ],
            
            
            "Description": [
                "Survival status: 0 = No, 1 = Yes",
                "Passenger class: 1, 2, or 3",
                "Passenger gender",
                "Passenger age",
                "Number of siblings or spouses aboard",
                "Number of parents or children aboard",
                "Passenger fare",
                "Port of embarkation: C, Q, S",
                "Passenger class as text",
                "Passenger category: man, woman, child",
                "Whether the passenger is an adult male",
                "Passenger deck",
                "Full name of embarkation town",
                "Survival status as yes/no",
                "Whether the passenger was travelling alone"
    ]
    }
)

df_features = pd.DataFrame(feature_description)
st.dataframe(df_features, use_container_width = True, hide_index = True)

# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# SECTION 2: INTERACTIVE FILTERS + KPI METRICS
# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

st.header("🎛️ Interactive Filters")

st.write(
    """
Use the filters below to explore different groups of the Titanic passengers and observe how the key statistics change dynamically.
    """
)

# ==================================================================================================================================================================
# SIDEBAR FILTERS
# ==================================================================================================================================================================

st.sidebar.header("🔎 Passenger Filters")

selected_options = ["All"] + sorted(df_clean["sex"].dropna().unique().tolist())

selected_gender = st.sidebar.selectbox("Gender", selected_options)

# ==================================================================================================================================================================
# PASSENGER CLASS FILTERS
# ==================================================================================================================================================================

class_options = ["All"] + sorted(df_clean["pclass"].dropna().unique().tolist())

selected_class = st.sidebar.selectbox("Passenger Class", class_options)

# ==================================================================================================================================================================
# EMBARKATION FILTERS
# ==================================================================================================================================================================

embarked_options = ["All"] + sorted(df_clean["embark_town"].dropna().unique().tolist())

selected_embarkation = st.sidebar.selectbox("Embarkation Ports", embarked_options)

# ==================================================================================================================================================================
# AGE FILTERS
# ==================================================================================================================================================================

age_min = int(df_clean["age"].min())
age_max = int(df_clean["age"].max())

selected_age_range = st.sidebar.slider("Age Range", min_value = age_min, max_value = age_max, value = (age_min, age_max))

# ==================================================================================================================================================================
# TRAVEL STATUS FILTERS
# ==================================================================================================================================================================

travel_options = ["All", "Travelling Alone", "Travelling With Family"]

selected_travel_status = st.sidebar.selectbox("Travel Status", travel_options)

# ==================================================================================================================================================================
# APPLY FILTERS 
# ==================================================================================================================================================================

filtered_df = df_clean.copy()

# Gender Filter
if selected_gender != "All":
    filtered_df = filtered_df[filtered_df["sex"] == selected_gender]

# Passenger Class Filter
if selected_class != "All":
    filtered_df = filtered_df[filtered_df["pclass"] == selected_class]

# Embarkation Filter
if selected_embarkation != "All":
    filtered_df = filtered_df[filtered_df["embark_town"] == selected_embarkation]

# Age Filter
filtered_df = filtered_df[filtered_df["age"].between(selected_age_range[0], selected_age_range[1])]

# Travel Status Filter 
if selected_travel_status == "Travelling Alone":
    filtered_df = filtered_df[filtered_df["alone"] == True]

elif selected_travel_status == "Travelling With Family":
    filtered_df = filtered_df[filtered_df["alone"] == False]

st.divider()

# ==================================================================================================================================================================
# KPI METRICS
# ==================================================================================================================================================================

st.subheader("📊 Key Passenger Metrics")

total_passengers = len(filtered_df)

total_survivors = filtered_df["survived"].sum()

survival_rates = (
    (total_survivors/total_passengers)*100
    if total_passengers > 0
    else 0
)

average_fare = (
    filtered_df["fare"].mean()
    if total_passengers > 0
    else 0
)

average_fare_display = (f"{average_fare:.2f} units" if pd.notna(average_fare) else "N/A")

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("Passengers", f"{total_passengers:,}")

with col2:
    st.metric("Survivors", f"{int(total_survivors):,}")

with col3: 
    st.metric("Survival Rate", f"{survival_rates:.2f}%")

with col4: 
    st.metric("Average Fare", f"{average_fare:.2f} units")

st.divider()

# ==================================================================================================================================================================
# FILTERED DATA SUMMARY
# ==================================================================================================================================================================

st.subheader("🔍 Filtered Passenger Data")

st.write(f"Showing **{len(filtered_df):,} passengers** based on the selected filters.")

st.dataframe(
    filtered_df, 
    use_container_width = True, 
    hide_index = True
)

if filtered_df.empty:
    st.warning(
        "No passengers match the selected filters. "
        "Please broaden the filters to continue the analysis."
    )
    st.stop()

# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# SECTION 3: PASSENGER PROFILE ANALYSIS
# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

st.header("📈 Passenger Profile Analysis")

st.write("""
This section provides an interactive overview of the characteristics of the selected Titanic Passengers using demographic and travel related features.
""")

# ==================================================================================================================================================================
# GENDER DISTRIBUTION
# ==================================================================================================================================================================

st.subheader("👥 Gender Distribution")

gender_distribution = (filtered_df["sex"].value_counts().reset_index())

gender_distribution.columns = ["Gender", "Passengers"]

fig_gender = px.bar(gender_distribution, x = "Gender", y = "Passengers", title = "Passenger Distribution By Gender", text = "Passengers")

fig_gender.update_traces(textposition = "outside")

max_gender_distribution = gender_distribution["Passengers"].max()

fig_gender.update_layout(xaxis_title = "Gender", 
                        yaxis_title = "Number Of Passengers", 
                        yaxis=dict(dtick=1 if max_gender_distribution < 10 else None))

st.plotly_chart(fig_gender, use_container_width = True)

# ==================================================================================================================================================================
# PASSENGER CLASS DISTRIBUTION
# ==================================================================================================================================================================

st.subheader("🎫 Passenger Class Distribution")

class_distribution = (filtered_df["pclass"].value_counts().sort_index().reset_index())

class_distribution.columns = ["Passenger Class", "Passengers"]

fig_class = px.bar(class_distribution, x = "Passenger Class", y = "Passengers", title = "Passenger Distribution by Class", text = "Passengers")

fig_class.update_traces(textposition = "outside")

max_class_distribution = class_distribution["Passengers"].max()

fig_class.update_layout(
    xaxis_title = "Passenger Class", 
    yaxis_title = "Number Of Passengers", 
    xaxis = dict(tickmode = "array", 
                tickvals = [1, 2, 3], 
                ticktext = ["1st Class", "2nd Class", "3rd Class"]
    ), 
    yaxis=dict(dtick=1 if max_class_distribution < 10 else None))

st.plotly_chart(fig_class, use_container_width = True)

# ==================================================================================================================================================================
# AGE DISTRIBUTION
# ==================================================================================================================================================================

age_data = filtered_df.dropna(subset=["age"])

fig_age = px.histogram(
    age_data, 
    x = "age", 
    nbins = 30, 
    title = "Passenger Age Distribution", 
    labels = {"age" : "Age"}
)

fig_age.update_layout(xaxis_title = "Age", 
                    yaxis_title = "Number Of Passengers", 
                    yaxis = dict(dtick = 1 if len(age_data) < 10 else None))

st.plotly_chart(fig_age, use_container_width = True)

# ==================================================================================================================================================================
# FARE DISTRIBUTION
# ==================================================================================================================================================================

st.subheader("💰 Fare Distribution")

fare_data = filtered_df.dropna(subset=["fare"])

fig_fare = px.histogram(
    fare_data, 
    x = "fare", 
    nbins = 30, 
    title = "Passenger Fare Distribution", 
    labels = {"fare" : "Fare"}
)

fig_fare.update_layout(xaxis_title = "Fare", 
                    yaxis_title = "Number Of Passengers", 
                    yaxis = dict(dtick = 1 if len(fare_data) < 10 else None))

st.plotly_chart(fig_fare, use_container_width = True)

# ==================================================================================================================================================================
# EMBARKATION DISTRIBUTION
# ==================================================================================================================================================================


st.subheader("⚓ Embarkation Port Distribution")

embarkation_distribution = (filtered_df["embark_town"].value_counts().reset_index())

embarkation_distribution.columns = ["Embarkation Port", "Passengers"]

fig_embarkation = px.bar(
    embarkation_distribution,
    x="Embarkation Port",
    y="Passengers",
    title="Passenger Distribution by Embarkation Port",
    text="Passengers"
)

max_embarked_passengers = embarkation_distribution["Passengers"].max()

fig_embarkation.update_traces(textposition="outside")

fig_embarkation.update_layout(xaxis_title="Embarkation Port", 
                            yaxis_title="Number of Passengers", 
                            yaxis=dict(dtick=1 if max_embarked_passengers < 10 else None))

st.plotly_chart(fig_embarkation, use_container_width=True)

# ==================================================================================================================================================================
# SIBSP DISTRIBUTION
# ==================================================================================================================================================================

st.subheader("👨‍👩‍👧‍👦 Siblings/Spouses Aboard")

sibsp_distribution = (filtered_df["sibsp"].value_counts().sort_index().reset_index())

sibsp_distribution.columns = ["Sibsp", "Passengers"]

fig_sibsp = px.bar(
    sibsp_distribution,
    x="Sibsp",
    y="Passengers",
    title="Distribution of Siblings/Spouses Aboard",
    text="Passengers"
)

max_sibsp_passengers = sibsp_distribution["Passengers"].max()

fig_sibsp.update_traces(textposition="outside")

fig_sibsp.update_layout(xaxis_title="Number of Siblings/Spouses", 
                        yaxis_title="Number of Passengers",
                        xaxis=dict(type="category"), 
                        yaxis=dict(dtick=1 if max_sibsp_passengers < 10 else None))

st.plotly_chart(fig_sibsp, use_container_width=True)

# ==================================================================================================================================================================
# PARCH DISTRIBUTION
# ==================================================================================================================================================================

st.subheader("👪 Parents/Children Aboard")

parch_distribution = (filtered_df["parch"].value_counts().sort_index().reset_index())

parch_distribution.columns = ["Parch", "Passengers"]

fig_parch = px.bar(
    parch_distribution,
    x="Parch",
    y="Passengers",
    title="Distribution of Parents/Children Aboard",
    text="Passengers"
)

max_parch_passengers = parch_distribution["Passengers"].max()

fig_parch.update_traces(textposition="outside")

fig_parch.update_layout(xaxis_title="Number of Parents/Children", 
                        yaxis_title="Number of Passengers", 
                        xaxis=dict(type="category"), 
                        yaxis=dict(dtick=1 if max_parch_passengers < 10 else None))

st.plotly_chart(fig_parch, use_container_width=True)

# ==================================================================================================================================================================
# TRAVEL STATUS
# ==================================================================================================================================================================

st.subheader("🧳 Travel Status")

travel_distribution = (
    filtered_df["alone"].dropna().map({True : "Travelling Alone", False : "Travelling With Family"})
    .value_counts().reindex(
        ["Travelling Alone", "Travelling With Family"], fill_value = 0
    ).rename_axis("Travel Status").reset_index(name = "Passengers")
)

travel_distribution.columns = ["Travel Status", "Passengers"]

fig_travel = px.bar(
    travel_distribution,
    x="Travel Status",
    y="Passengers",
    title="Passengers Travelling Alone vs With Family",
    text="Passengers",
    category_orders={
        "Travel Status": [
            "Travelling Alone",
            "Travelling With Family"
        ]
    }
)

max_travel_passengers = travel_distribution["Passengers"].max()

fig_travel.update_traces(textposition="outside")

fig_travel.update_layout(xaxis_title="Travel Status", 
                        yaxis_title="Number of Passengers", 
                        yaxis=dict(dtick=1 if max_travel_passengers < 10 else None))

st.plotly_chart(fig_travel, use_container_width=True)

# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# SECTION 4: SURVIVAL PATTERNS AND FEATURE RELATIONSHIP
# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

st.header("❤️ Survival Patterns And Feature Analysis")

st.write(
    """This section analyzes how different passenger characteristics and travel related features were associated with the survival of the Titanic."""
)

# ==================================================================================================================================================================
# GENDER VS SURVIVAL
# ==================================================================================================================================================================

st.subheader("👩 Gender vs Survival")

gender_survival = (filtered_df.groupby("sex")["survived"].mean().mul(100).reset_index())

gender_survival.columns = ["Gender", "Survival Rate"]

fig_gender_survival = px.bar(
    gender_survival, x = "Gender", y = "Survival Rate", 
    title = "Survival Rate by Gender", 
    text = "Survival Rate"
)

fig_gender_survival.update_traces(
    texttemplate="%{text:.2f}%",
    textposition = "outside"
)

fig_gender_survival.update_layout(
    xaxis_title = "Gender", 
    yaxis_title = "Survival Rate(%)", 
    yaxis = dict(range = [0, 100])
)

st.plotly_chart(fig_gender_survival, use_container_width = True)

# ==================================================================================================================================================================
# PCLASS VS SURVIVAL
# ==================================================================================================================================================================

st.subheader("🎫 Passenger Class vs Survival")

class_survival = (filtered_df.groupby("pclass")["survived"].mean().mul(100).reset_index())

class_survival.columns = ["Pclass", "Survival Rate"]

class_survival = class_survival.sort_values("Pclass")

fig_class_survival = px.bar(
    class_survival, x = "Pclass", y = "Survival Rate", 
    title = "Survival Rate by Passenger Class", 
    text = "Survival Rate"
)

fig_class_survival.update_traces(
    texttemplate="%{text:.2f}%",
    textposition = "outside"
)

fig_class_survival.update_layout(
    xaxis_title = "Pclass", 
    yaxis_title = "Survival Rate(%)", 
    yaxis = dict(range = [0, 100]), 
    xaxis = dict(tickmode = "array", 
                tickvals = [1, 2, 3], 
                ticktext = ["1st Class", "2nd Class", "3rd Class"])
)

st.plotly_chart(fig_class_survival, use_container_width = True)

# ==================================================================================================================================================================
# EMBARKATION PORT VS SURVIVAL
# ==================================================================================================================================================================

st.subheader("⚓ Embarkation Port vs Survival")

embarkation_survival = (filtered_df.groupby("embark_town")["survived"].mean().mul(100).reset_index())

embarkation_survival.columns = ["Embarkation Port", "Survival Rate"]

fig_embarkation_survival = px.bar(
    embarkation_survival, x = "Embarkation Port", y = "Survival Rate", 
    title = "Survival Rate by Embarkation Port", 
    text = "Survival Rate"
)

fig_embarkation_survival.update_traces(
    texttemplate="%{text:.2f}%",
    textposition = "outside"
)

fig_embarkation_survival.update_layout(
    xaxis_title = "Embarkation Port", 
    yaxis_title = "Survival Rate(%)", 
    yaxis = dict(range = [0, 100])
)

st.plotly_chart(fig_embarkation_survival, use_container_width = True)

# ==================================================================================================================================================================
# AGE VS SURVIVAL
# ==================================================================================================================================================================

st.subheader("🎂 Age vs Survival")

age_survival_data = filtered_df.dropna(subset=["age"])

fig_age_survival = px.histogram(
    age_survival_data, 
    x = "age", 
    color = "survived", 
    nbins = 30, 
    barmode = "group", 
    opacity = 0.65, 
    title = "Age Distribution by Survival Status", 
    labels = {"age" : "Age", "survived" : "Survival Status"}
)

fig_age_survival.update_layout(
    xaxis_title = "Age", 
    yaxis_title = "Number of Passengers", 
    legend_title = "Survival Status"
)

fig_age_survival.for_each_trace(
    lambda trace : trace.update(
        name = "Did Not Survive" if trace.name == "0" else "Survived"
    )
)

st.plotly_chart(fig_age_survival, use_container_width = True)

# ==================================================================================================================================================================
# FARE VS SURVIVAL
# ==================================================================================================================================================================

st.subheader("💰 Fare vs Survival")

fare_survival_data = filtered_df.dropna(subset=["fare", "survived"]).copy()

fare_survival_data["Survival Status"] = filtered_df["survived"].map(
    {
        0 : "Did Not Survive", 
        1 : "Survived"
    }
)

fig_fare_survival = px.box(
    fare_survival_data, x = "Survival Status", y = "fare", 
    title = "Fare Distribution by Survival Status", 
    labels = {
        "fare" : "Fare", 
        "Survival Status": "Survival Status"
    }, points = False
)

fig_fare_survival.update_layout(
    yaxis = dict(rangemode = "tozero")
)

st.plotly_chart(fig_fare_survival, use_container_width = True)

# ==================================================================================================================================================================
# SIBSP VS SURVIVAL
# ==================================================================================================================================================================
st.subheader("👨‍👩‍👧‍👦 SibSp vs Survival")

sibsp_survival = (filtered_df.groupby("sibsp")["survived"].mean().mul(100).reset_index())

sibsp_survival.columns = ["SibSp", "Survival Rate"]

sibsp_survival = sibsp_survival.sort_values("SibSp")

fig_sibsp_survival = px.bar(
    sibsp_survival,
    x = "SibSp",
    y = "Survival Rate",
    title = "Survival Rate by Number of Siblings / Spouses",
    text = "Survival Rate"
)

fig_sibsp_survival.update_traces(
    texttemplate="%{text:.2f}%",
    textposition="outside"
)

fig_sibsp_survival.update_layout(
    xaxis_title="Number of Siblings / Spouses",
    yaxis_title="Survival Rate (%)",
    yaxis=dict(range=[0, 100]), 
    xaxis=dict(type="category")
)

st.plotly_chart(
    fig_sibsp_survival,
    use_container_width=True
)

# ==================================================================================================================================================================
# PARCH VS SURVIVAL
# ==================================================================================================================================================================

st.subheader("👪 Parch vs Survival")

parch_survival = (filtered_df.groupby("parch")["survived"].mean().mul(100).reset_index())

parch_survival.columns = ["Parch", "Survival Rate"]

parch_survival = parch_survival.sort_values("Parch")

fig_parch_survival = px.bar(
    parch_survival,
    x = "Parch",
    y = "Survival Rate",
    title = "Survival Rate by Number of Parents / Children",
    text = "Survival Rate"
)

fig_parch_survival.update_traces(
    texttemplate="%{text:.2f}%",
    textposition="outside"
)

fig_parch_survival.update_layout(
    xaxis_title="Number of Parents / Children",
    yaxis_title="Survival Rate (%)",
    yaxis=dict(range = [0, 100]), 
    xaxis=dict(type="category")
)

st.plotly_chart(fig_parch_survival, use_container_width=True)

# ==================================================================================================================================================================
# TRAVEL STATUS VS SURVIVAL
# ==================================================================================================================================================================

st.subheader("🧳 Travel Status vs Survival")

travel_survival = (filtered_df.groupby("alone")["survived"].mean().mul(100).reset_index())

travel_survival.columns = ["alone", "Survival Rate"]

travel_survival["Travel Status"] = travel_survival["alone"].map(
    {
        True : "Travelling Alone", 
        False : "Travelling With Family"
    }
)

fig_travel_survival = px.bar(
    travel_survival,
    x = "Travel Status",
    y = "Survival Rate",
    title = "Survival Rate by Travel Status",
    text = "Survival Rate", 
    category_orders = {
        "Travel Status": ["Travelling Alone", "Travelling With Family"]
    }
)

fig_travel_survival.update_traces(
    texttemplate="%{text:.2f}%",
    textposition="outside"
)

fig_travel_survival.update_layout(
    xaxis_title="Travel Status",
    yaxis_title="Survival Rate (%)",
    yaxis = dict(range = [0, 100])
)

st.plotly_chart(fig_travel_survival, use_container_width=True)

# ==================================================================================================================================================================
# GENDER + PASSENGER CLASS VS SURVIVAL
# ==================================================================================================================================================================

st.subheader("👥 Gender + Passenger Class vs Survival")

gender_class_survival = (filtered_df.groupby(["sex", "pclass"])["survived"].mean().mul(100).reset_index())

gender_class_survival.columns = ["Gender", "Passenger Class", "Survival Rate"]

fig_gender_class = px.bar(
    gender_class_survival,
    x="Passenger Class",
    y="Survival Rate",
    color="Gender",
    barmode="group",
    title="Survival Rate by Gender and Passenger Class",
    text="Survival Rate"
)

fig_gender_class.update_traces(
    texttemplate="%{text:.2f}%",
    textposition="outside"
)

fig_gender_class.update_layout(
    xaxis_title="Passenger Class",
    yaxis_title="Survival Rate (%)",
    yaxis=dict(range=[0, 100]),
    xaxis=dict(
        tickmode="array",
        tickvals=[1, 2, 3],
        ticktext=["1st Class", "2nd Class", "3rd Class"]
    )
)

st.plotly_chart(fig_gender_class,use_container_width = True)

# ==================================================================================================================================================================
# AGE GROUP VS SURVIVAL
# ==================================================================================================================================================================

st.subheader("🎯 Age Group vs Survival")

age_group_df = filtered_df.copy()

age_group_df["Age Group"] = pd.cut(
    age_group_df["age"], bins = [0, 12, 18, 30, 50, 65, float("inf")], 
    labels = [
        "Child", 
        "Teenager", 
        "Young Adult", 
        "Adult", 
        "Middle Age", 
        "Senior"
    ], include_lowest = True
)

age_group_df = age_group_df.dropna(subset=["Age Group"])

age_group_survival = (age_group_df.groupby("Age Group", observed = False)["survived"].mean().mul(100).reset_index())

age_group_survival.columns = ["Age Group", "Survival Rate"]

fig_age_group_survival = px.bar(
    age_group_survival,
    x="Age Group",
    y="Survival Rate",
    title="Survival Rate by Age Group",
    text="Survival Rate"
)

fig_age_group_survival.update_traces(
    texttemplate="%{text:.2f}%",
    textposition="outside"
)

fig_age_group_survival.update_layout(
    xaxis_title="Age Group",
    yaxis_title="Survival Rate (%)",
    yaxis=dict(range=[0, 100]),
)

st.plotly_chart(fig_age_group_survival,use_container_width = True)

# ==================================================================================================================================================================
# CORRELATION WITH SURVIVAL                 
# ==================================================================================================================================================================

st.subheader("📊 Numerical Feature Correlation With Survival")

correlation_columns = [
    "survived",
    "pclass",
    "age",
    "sibsp",
    "parch",
    "fare"
]

survival_correlation = (
    filtered_df[correlation_columns]
    .corr()["survived"]
    .drop("survived").dropna()
    .sort_values(ascending = False)
    .reset_index()
)

survival_correlation.columns = ["Feature", "Correlation With Survival"]

if not survival_correlation.empty:
    fig_correlation = px.bar(
        survival_correlation, 
        x = "Feature", 
        y = "Correlation With Survival",
        title="Numerical Feature Correlation with Survival",
        text="Correlation With Survival"
    )

    fig_correlation.update_traces(
        texttemplate="%{text:.2f}",
        textposition="outside"
    )

    fig_correlation.update_layout(
        xaxis_title = "Feature",
        yaxis_title = "Correlation With Survival",
        yaxis=dict(range=[-1, 1]),
    )

    st.plotly_chart(fig_correlation, use_container_width = True)

else:
    st.info("Correlation cannot be calculated from the currently selected data.")

# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# SECTION 5: DETAILED DATA AND FINAL INSIGHT 
# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

st.header("📋 Detailed Data And Final Insight")

st.write(
    """This final section provides a final view of the selected passengers,
    summary statistics, key survival insights, and the overall conclusion from the Titanic analysis."""
)

# ==================================================================================================================================================================
# FILTERED DATASET
# ==================================================================================================================================================================

st.subheader("🔎 Detailed Passenger Data")

st.write(
    f"""The table shows the complete information for the **{len(filtered_df):,} passengers** selected through the sidebar filters."""
)

st.dataframe(filtered_df, use_container_width = True, hide_index = True)

# ==================================================================================================================================================================
# SUMMARY STATISTICS
# ==================================================================================================================================================================

st.subheader("📊 Summary Statistics")

summary_columns = [
    "age", 
    "fare", 
    "sibsp", 
    "parch"
]

summary_statistics = (filtered_df[summary_columns].describe().T.round(2))

summary_statistics = summary_statistics.rename(
    columns = {
        "count" : "Count", 
        "mean" : "Mean", 
        "std" : "Std. Deviation", 
        "min" : "Minimum", 
        "25%" : "25th Percentile", 
        "50%" : "50th Percentile", 
        "75%" : "75th Percentile", 
        "max" : "Maximum"
    }
)

st.dataframe(summary_statistics, use_container_width = True)

# ==================================================================================================================================================================
# SURVIVAL SUMMARY
# ==================================================================================================================================================================

st.subheader("❤️ Survival Summary")

if len(filtered_df) > 0:

    survival_counts = (filtered_df["survived"].value_counts().sort_index())

    survived_counts = survival_counts.get(1, 0)
    not_survival_counts = survival_counts.get(0, 0)

    survival_rate = (survived_counts/len(filtered_df))*100

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("Survived", f"{int(survived_counts):,}")

    with col2: 
        st.metric("Did Not Survive", f"{int(not_survival_counts):,}")

    with col3:
        st.metric("Survival Rate", f"{survival_rate:.2f}%")

else:
    st.warning("No passengers match the selected filters.")

# ==================================================================================================================================================================
# TOP SURVIVAL INSIGHTS
# ==================================================================================================================================================================

st.subheader("💡 Key Survival Insights")

if len(filtered_df) > 0:

    insight_col1, insight_col2 = st.columns(2)

    # ==============================================================================================================================================================
    # GENDER INSIGHTS
    # ==============================================================================================================================================================

    with insight_col1: 

        gender_insight = (filtered_df.groupby("sex")["survived"].mean().mul(100))

        if len(gender_insight) > 0:

            highest_gender = gender_insight.idxmax()
            highest_gender_rate = gender_insight.max()

            st.markdown(
                f"""
**Gender:** ***{highest_gender.title()} passengers had the highest
survival rate among the selected passengers, at***
**{highest_gender_rate:.2f}%**.
"""
            )

    # ==============================================================================================================================================================
    # CLASS INSIGHTS
    # ==============================================================================================================================================================

    with insight_col2:

        class_insight = (filtered_df.groupby("pclass")["survived"].mean().mul(100))

        if len(class_insight) > 0:

            highest_class = class_insight.idxmax()
            highest_class_rate = class_insight.max()

            st.markdown(
                f"""
**Passenger Class:** ***Class {highest_class} had the highest
survival rate among the selected passengers, at***
**{highest_class_rate:.2f}%**.
"""
            )

    st.divider()

    # ==============================================================================================================================================================
    # FARE INSIGHTS
    # ==============================================================================================================================================================

    average_fare = filtered_df["fare"].mean()

    st.markdown(
        f"""
**Fare** : ***The average fare among the selected passengers was*** **{average_fare:.2f} units**.
"""
    )

    # ==============================================================================================================================================================
    #  AGE INSIGHTS
    # ==============================================================================================================================================================

    average_age = filtered_df["age"].mean()

    if pd.notna(average_age):
        st.markdown(
            f"""
    **Age** : ***The average age among the selected passengers was*** **{average_age:.2f}**.
    """
        )

    # ==============================================================================================================================================================
    # TRAVEL STATUS INSIGHTS
    # ==============================================================================================================================================================

    travel_insight = (filtered_df.groupby("alone")["survived"].mean().mul(100))

    if len(travel_insight) > 0:

        highest_travel_status = travel_insight.idxmax()
        highest_travel_rate = travel_insight.max()

        travel_label = (
            "Travelling Alone" if highest_travel_status else "Travelling With Family"
        )

        st.markdown(
    f"""
**Travel Status:** ***{travel_label.title()} passengers had the highest
survival rate among the selected passengers, at***
**{highest_travel_rate:.2f}%**.
"""
)

else:
    st.info("Insights will appear when passengers are available after applying the filters.")

# ==================================================================================================================================================================
# FINAL CONCLUSION
# ==================================================================================================================================================================

st.subheader("📝 Final Conclusion")

if len(filtered_df) > 0:

    st.write(
        f"""
The Titanic analysis dashboard examined **{len(filtered_df):,} selected passengers**
based on the applied filters. The analysis explored passenger demographics,
travel characteristics, survival patterns, and relationships between numerical
features and survival.

The results show that survival was not evenly distributed across all passenger
groups. Factors such as **gender, passenger class, age, fare, family-related
features, and travel status** showed different patterns in relation to survival.

The dashboard combines data exploration with interactive filtering, allowing
users to investigate how survival patterns change across different passenger
groups.
"""
    )

else:

    st.warning(
        "No final conclusion can be generated because no passengers match the selected filters."
    )


# ==================================================================================================================================================================
# DASHBOARD END 
# ==================================================================================================================================================================

st.divider()

st.success("***🎉 Titanic Data Analysis Dashboard completed successfully!***")
