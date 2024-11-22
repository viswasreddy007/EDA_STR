import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import warnings
import os

# Suppress warnings
warnings.filterwarnings("ignore")

# Page configuration
st.set_page_config(
    page_title="EDA Dashboard",
    page_icon="📊",
    layout="wide"
)

# CSS Styling
st.markdown("""
    <style>
        /* Full-page gradient background */
        .stApp {
            background-color:#ff6d83 ;
            background-attachment: fixed;
            color: #333333;
        }

        /* Title and Header styling */
        h1, h3, h2 {
            text-align: center;
            color: #FFFFFF;
            text-shadow: 2px 2px 5px rgba(0, 0, 0, 0.8);
        }

        /* Sidebar styling */
         .stSidebar{
            background-color: RoyalBlue !important;  /* Green background */
            color: white !important;  /* White text color */
            border-radius: 10px;
            padding: 15px;
        }

        /* File uploader */
        .stFileUploader {
            color: #FFFFFF !important;
             background-color: white !important;
            border-radius: 10px;
            padding: 15px;
        }

        /* Buttons */
        .stButton>button {
            background-color: white !important;
            color: RoyalBlue !important;
            border-radius: 10px !important;
            box-shadow: 0px 4px 6px rgba(0, 0, 0, 0.2);
        }
            .stButton>button:hover {
            background-color: RoyalBlue !important;
            color: #FFEB99 !important;
            border-radius: 10px !important;
            box-shadow: 0px 4px 6px rgba(0, 0, 1, 0.5);
            
        }
    </style>
""", unsafe_allow_html=True)

# Title section
st.markdown(
    "<h1>Exploratory Data Analysis (EDA)</h1>",
    unsafe_allow_html=True
)
st.markdown(
    "<p style='text-align: center;'>Analyze your data effortlessly with a variety of plots and visualizations.</p>",
    unsafe_allow_html=True
)

# Sidebar setup
st.sidebar.header("Navigation")
st.sidebar.markdown("### Select a plot type and upload your dataset")

# Session state setup
if 'df' not in st.session_state:
    st.session_state.df = pd.DataFrame()
if 'default_loaded' not in st.session_state:
    st.session_state.default_loaded = False

# File uploader
file = st.file_uploader("Upload a CSV or Excel file:", type=["csv", "xlsx"])
df = st.session_state.df

# Helper functions
def outli(se_co):
    va = df[se_co].values
    m = df[se_co].median()
    q1 = np.percentile(df[se_co], 25)
    q3 = np.percentile(df[se_co], 75)
    iqr = q3 - q1
    lb = q1 - (1.5 * iqr)
    ub = q3 + (1.5 * iqr)
    f = df[se_co]
    con = (va < lb) | (va > ub)
    l = np.where(con, m, f)
    return l

def chart(pl, se_co):
    if pl == 'bar':
        v = df[se_co].value_counts()
        if len(v) <= 12:
            sns.countplot(data=df, x=se_co, palette='Set2')
            plt.title(se_co, fontsize=16)
            st.pyplot(plt)
            plt.clf()
    elif pl == 'pie':
        data = df[se_co].value_counts()
        if len(data) <= 12:
            ke = data.keys()
            va = data.values
            plt.pie(va, labels=ke, autopct='%0.2f%%', radius=1, colors=sns.color_palette("pastel"))
            plt.title(se_co, fontsize=16)
            st.pyplot(plt)
            plt.clf()
    elif pl == 'hist':
        df['bal'] = outli(se_co)
        plt.figure(figsize=(10, 4))
        plt.subplot(1, 2, 1)
        plt.hist(df[se_co], color='skyblue', edgecolor='black')
        plt.title(f"{se_co} (Before Outliers)", fontsize=14)
        plt.subplot(1, 2, 2)
        plt.hist(df['bal'], color='salmon', edgecolor='black')
        plt.title(f"{se_co} (After Outliers)", fontsize=14)
        st.pyplot(plt)
        plt.clf()
        df.drop("bal", axis=1, inplace=True)
    elif pl == 'dist':
        df['bal'] = outli(se_co)
        plt.figure(figsize=(10, 4))
        plt.subplot(1, 2, 1)
        sns.histplot(df[se_co], kde=True, color='skyblue')
        plt.title(f"{se_co} (Before Outliers)", fontsize=14)
        plt.subplot(1, 2, 2)
        sns.histplot(df['bal'], kde=True, color='salmon')
        plt.title(f"{se_co} (After Outliers)", fontsize=14)
        st.pyplot(plt)
        plt.clf()
        df.drop('bal', axis=1, inplace=True)
    elif pl == 'boxplot':
        df['bal'] = outli(se_co)
        plt.figure(figsize=(10, 4))
        plt.subplot(1, 2, 1)
        plt.boxplot(df[se_co])
        plt.title(f"{se_co} (Before Outliers)", fontsize=14)
        plt.subplot(1, 2, 2)
        plt.boxplot(df['bal'])
        plt.title(f"{se_co} (After Outliers)", fontsize=14)
        st.pyplot(plt)
        plt.clf()
        df.drop('bal', axis=1, inplace=True)

def heat():
    cor = df.corr(numeric_only=True)
    plt.figure(figsize=(10, 6))
    sns.heatmap(cor, annot=True, cmap='coolwarm', fmt=".2f")
    st.pyplot(plt)
    plt.clf()  

def cro(se_col1, se_col2):
    df1 = pd.crosstab(df[se_col1], df[se_col2])
    df1.plot(kind='bar', figsize=(8, 4), color=['skyblue', 'salmon'])
    plt.title(f"Cross Tabulation: {se_col1} vs {se_col2}", fontsize=16)
    st.pyplot(plt)
    plt.clf()

# File reading and display
if file is not None:
    file_extension = os.path.splitext(file.name)[-1].lower()
    try:
        if file_extension == '.csv':
            sep = st.text_input("Enter the separator for the CSV file", ',')
            df = pd.read_csv(file, sep=sep)
            st.session_state.df = df
            st.write(df.head())
        elif file_extension == '.xlsx':
            df = pd.read_excel(file)
            st.session_state.df = df
            st.write(df.head())
    except Exception as e:
        st.error(f"Error reading the file: {str(e)}")

defau = st.sidebar.button("Use Default Dataset")

if defau and not st.session_state.default_loaded:
    df = pd.read_csv("bank.csv",sep=';')
    st.session_state.df = df
    st.session_state.default_loaded = True
    st.write("Default dataset loaded:")
    st.write(df.head())

catcol = df.select_dtypes(include='object').columns
numcol = df.select_dtypes(exclude='object').columns

se_op = st.sidebar.selectbox("Choose Plot Type:", ["bar", "pie", "hist", "dist", "boxplot", "heatmap", "crosstab"])

if se_op in ['crosstab']:
    se_col1 = st.sidebar.selectbox("Select Column 1:", catcol)
    se_col2 = st.sidebar.selectbox("Select Column 2:", catcol)
elif se_op in ['bar', 'pie']:
    se_co = st.sidebar.selectbox("Select Categorical Column:", catcol)
elif se_op in ['hist', 'dist', 'boxplot']:
    se_co = st.sidebar.selectbox("Select Numerical Column:", numcol)

submit = st.sidebar.button("Generate Plot")

if submit:
    if df.empty:
        st.error("Please upload a dataset or use the default dataset.")
    else:
        if se_op == 'crosstab':
            cro(se_col1, se_col2)
        elif se_op == 'heatmap':
            heat()
        else:
            chart(se_op, se_co)