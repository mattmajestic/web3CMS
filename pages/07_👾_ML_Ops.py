import streamlit as st
from streamlit.components.v1 import iframe, html
import streamlit.components.v1 as components
from streamlit_javascript import st_javascript
import pdfkit
from jinja2 import Environment, PackageLoader, select_autoescape, FileSystemLoader
from datetime import datetime, date, time, timezone, timedelta
import pandas as pd
import requests
import yfinance as yf
from pycoingecko import CoinGeckoAPI
import json
import time
import supabase
import os
import folium
from geopy.geocoders import Nominatim
import plotly.express as px
from streamlit import session_state
import random
import string
from urllib.parse import urlencode
import webbrowser
import torch
from transformers import pipeline, AutoModelForCausalLM, AutoTokenizer, set_seed
from sklearn.datasets import load_iris
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor
from sklearn.neural_network import MLPRegressor
import matplotlib.pyplot as plt
import seaborn as sns
from web3 import Web3
# from wallet_connect import wallet_connect
# from web3 import Web3, HTTPProvider 

# Set your Supabase credentials as environment variables
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

# Initialize Supabase
supabase_client = supabase.Client(SUPABASE_URL, SUPABASE_KEY)

def ml_ops():
    st.title("ML Ops - Model Deployment 👾")
    st.toast('GUI for Machine Learning', icon='👾')

    with st.expander("Overview of ML Ops 🍰", expanded=True):
        st.write("ML Ops (Machine Learning Operations) is a set of practices and tools designed to automate and streamline the deployment and management of machine learning models.")
        st.write("The purpose of ML Ops is to enable small and medium-sized businesses (SMBs) to leverage machine learning for various tasks, such as predicting customer behavior, optimizing operations, and making data-driven decisions.")

    with st.expander("Step 1: Select Data 📊"):
        st.subheader("Select Data Source")
        data_option = st.selectbox("Data Source", ["Iris Dataset", "Local CSV", "Database", "API"])

        if data_option == "Iris Dataset":
            st.subheader("Iris Dataset (Sample)")
            iris = load_iris()
            data = pd.DataFrame(iris.data, columns=iris.feature_names)
            st.write(data.head())

        elif data_option == "Local CSV":
            uploaded_file = st.file_uploader("Upload CSV File")
            if uploaded_file:
                # Handle the uploaded CSV file.
                st.success("CSV File Uploaded and Processed!")

        elif data_option == "Database":
            # Input fields to connect to a database.
            db_host = st.text_input("Database Host")
            db_username = st.text_input("Database Username")
            db_password = st.text_input("Database Password", type="password")

        elif data_option == "API":
            # Input fields to specify an API endpoint.
            api_url = st.text_input("API URL")

    with st.expander("Step 2: Data Options 🛠️"):
        st.subheader("Select Third-Party Datasets")

    with st.expander("Step 3: Select Model 🤖"):
        st.subheader("Select Model Type")
        model_option = st.selectbox("Model Type", ["Linear Regression", "Random Forest", "Neural Network"])
        st.toast('Select Model', icon='👾')

        if model_option == "Linear Regression":
            st.subheader("Linear Regression Options")
            learning_rate = st.slider("Learning Rate", 0.01, 1.0, 0.1)

            # Train the model on Iris data
            iris = load_iris()
            model = LinearRegression()
            model.fit(iris.data, iris.target)

            # Display model information
            st.subheader("Linear Regression Model")
            st.write("Coefficient:", model.coef_)
            st.write("Intercept:", model.intercept_)

            # Visualization: Regression Coefficients
            st.subheader("Regression Coefficients")
            fig, ax = plt.subplots(figsize=(8, 4))
            sns.barplot(x=iris.feature_names, y=model.coef_, ax=ax)
            ax.set_title("Regression Coefficients")
            ax.set_ylabel("Coefficient Value")
            ax.set_xlabel("Feature Name")
            st.pyplot(fig)

        elif model_option == "Random Forest":
            st.subheader("Random Forest Options")
            num_estimators = st.slider("Number of Estimators", 1, 100, 10)

            # Train the model on Iris data
            iris = load_iris()
            model = RandomForestRegressor(n_estimators=num_estimators)
            model.fit(iris.data, iris.target)

            # Display model information
            st.subheader("Random Forest Model")
            st.write("Feature Importance:", model.feature_importances_)

            # Visualization: Feature Importance
            st.subheader("Feature Importance")
            fig, ax = plt.subplots(figsize=(8, 4))
            sns.barplot(x=iris.feature_names, y=model.feature_importances_, ax=ax)
            ax.set_title("Feature Importance")
            ax.set_ylabel("Importance Value")
            ax.set_xlabel("Feature Name")
            st.pyplot(fig)

        elif model_option == "Neural Network":
            st.subheader("Neural Network Options")
            num_hidden_layers = st.slider("Number of Hidden Layers", 1, 5, 2)

            # Train the model on Iris data
            iris = load_iris()
            model = MLPRegressor(hidden_layer_sizes=(num_hidden_layers,))
            model.fit(iris.data, iris.target)

            # Display model information
            st.subheader("Neural Network Model")
            st.write("Number of Hidden Layers:", num_hidden_layers)

    
    with st.expander("Step 4: Save Model Parameters 💾"):
        st.toast('Save Your Model', icon='👾')
        if st.button("Save Model Parameters"):
            response = supabase_client.table("ml-ops").insert([{
                "data_option": data_option,
                "model_option": model_option,
                "created_at": datetime.now().isoformat()
            }]).execute()
            st.success("Model Parameters Saved!")
