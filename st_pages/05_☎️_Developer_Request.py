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


def main():

    st.title("Software Development Request 🚀")

    # Create two columns for layout
    left_column,center_column, right_column = st.columns([6,2, 4])

    with left_column:
        st.subheader("User Information👤")
        user_email = st.text_input("Your Email 📧")
        st.subheader("GitHub Information")
        github_inputs = st.columns([5, 5])
        github_username = github_inputs[0].text_input("GitHub Username 🐱")
        github_repo = github_inputs[1].text_input("GitHub Repository 📂")
        st.subheader("Request Description")
        request_description = st.text_area("Describe Your Request 📝")

    # Right column for cost calculation and payment
    with right_column:
        st.subheader("Service Options")
        selected_service = st.radio("Select Service 💼", ["Code Review ($100)", "Code Writing ($300)", "Full PR Request ($500)"])

        include_test = st.checkbox("Include Test 🧪")
        include_documentation = st.checkbox("Include Documentation 📄")

        # Calculate the total price based on the selected service and options
        total_price = 0
        if "Code Review" in selected_service:
            total_price += 100
        if "Code Writing" in selected_service:
            total_price += 300
        if "Full PR Request" in selected_service:
            total_price += 500

        # Add additional costs for test and documentation
        if include_test:
            total_price += 50  # Adjust the price as needed
        if include_documentation:
            total_price += 50  # Adjust the price as needed

        st.subheader("Total Price")
        st.write(f"${total_price} 💰")

        if st.button("Pay with Stripe Checkout"):
            st.success("Payment successful! 🎉")
        # Submit button for storing the request in Supabase
        if st.button("Submit Request"):
            response = supabase_client.table("development-request").insert([{
                "user_email": user_email,
                "github_username": github_username,
                "github_repo": github_repo,
                "request_description": request_description,
                "selected_service": selected_service,
                "include_test": include_test,
                "include_documentation": include_documentation,
                "total_price": total_price,
                "created_at": datetime.now().isoformat()
            }]).execute()
            st.toast('Request Stored Successfully', icon='✅')