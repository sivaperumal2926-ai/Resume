import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

# Load dataset
@st.cache_data
def load_data():
    return pd.read_csv("C:/Pyproject/country_wise_latest.csv")

df = load_data()

# App title
st.title("🌍 Country-wise Data Visualization Dashboard")

# Show raw dataset
if st.checkbox("Show raw data"):
    st.write(df)

# Sidebar for user input
st.sidebar.header("Visualization Settings")

# Select numeric column for histogram
numeric_cols = df.select_dtypes(include=["int64", "float64"]).columns.tolist()
col_x = st.sidebar.selectbox("Select X-axis column", numeric_cols)
col_y = st.sidebar.selectbox("Select Y-axis column", numeric_cols)

# Plot type selection
plot_type = st.sidebar.radio("Choose plot type:", ["Histogram", "Scatterplot", "Boxplot", "Correlation Heatmap"])

# Visualization
st.subheader(f"{plot_type} Visualization")

if plot_type == "Histogram":
    fig, ax = plt.subplots()
    sns.histplot(df[col_x], kde=True, ax=ax)
    ax.set_title(f"Histogram of {col_x}")
    st.pyplot(fig)

elif plot_type == "Scatterplot":
    fig, ax = plt.subplots()
    sns.scatterplot(x=df[col_x], y=df[col_y], ax=ax)
    ax.set_title(f"Scatterplot: {col_x} vs {col_y}")
    st.pyplot(fig)

elif plot_type == "Boxplot":
    fig, ax = plt.subplots()
    sns.boxplot(x=df[col_x], ax=ax)
    ax.set_title(f"Boxplot of {col_x}")
    st.pyplot(fig)

elif plot_type == "Correlation Heatmap":
    fig, ax = plt.subplots(figsize=(10, 6))
    corr = df[numeric_cols].corr()
    sns.heatmap(corr, annot=True, cmap="coolwarm", ax=ax)
    ax.set_title("Correlation Heatmap")
    st.pyplot(fig)

# Top N countries visualization
st.subheader("Top N Countries by Selected Metric")
metric = st.selectbox("Select metric:", numeric_cols)
top_n = st.slider("Select number of countries:", 5, 20, 10)

top_countries = df.nlargest(top_n, metric)[["Country/Region", metric]]

fig, ax = plt.subplots(figsize=(10, 6))
sns.barplot(data=top_countries, x=metric, y="Country/Region", ax=ax, palette="viridis")
ax.set_title(f"Top {top_n} Countries by {metric}")
st.pyplot(fig)
