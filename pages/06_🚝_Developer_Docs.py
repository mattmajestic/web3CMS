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

def developer_docs():

    st.title("Software Development Documentation 🚝")
    st.write("")
    left, center, right = st.columns([4,4,4])
    st.write("")
    left.write("API Documentation 📪")
    left_expander = left.expander("CRM API Endpoint", expanded=False)
    with left_expander:
        st.write("📊 Description: The API allows you to manage customer relationship data.")
        st.write("🚀 Endpoint: `/api/crm`")
        st.write("📝 Method: GET")
        st.write("🔑 Parameters:")
        st.write("- `customer_id`: The ID of the customer.")
        st.write("- `name`: The name of the customer.")
        st.write("- `email`: The email address of the customer.")
        st.write("")
        st.write("")
        st.code("curl https://web3bms.io/api/crm", language="python")
        if left_expander:
            st.toast('Try it out with CURL', icon='📪')

    key_expander = left.expander("Create API Key 🔑", expanded=False)
    with key_expander:
        st.write("Enter your email address below to generate an API key:")
        email = st.text_input("Email Address")
        if st.button("Generate API Key"):
            if email:
                api_key = ''.join(random.choices(string.ascii_letters + string.digits, k=32))
                response = supabase_client.table("web3bms-api-keys").insert([{"email": email, "api_key": api_key}]).execute()
                st.write("Your API key has been generated and saved to the database.")
                st.toast('API Key Stored', icon='🔑')
                

    center.write("CLI Commands 🔍")
    cli_expander = center.expander("CRM CLI Command", expanded=False)
    with cli_expander:
        st.write("🔧 Description: The CLI command allows you to interact with customer data.")
        st.write("🛠️ Options:")
        st.write("- `--option1`: Description of option 1.")
        st.write("- `--option2`: Description of option 2.")
        st.write("")
        st.write("")
        st.code("web3bms crm list-clients", language="bash")
        st.toast('Try it out in Bash', icon='🔍')

    right.write("PyPI Package 🐍")
    pypi_expander = right.expander("CRM Python Functions", expanded=False)
    with pypi_expander:
        st.write("The web3bms package is available on PyPI and can be installed using pip:")
        st.code("pip install web3bms", language="bash")
        st.write("")
        st.write("Once installed, you can import and use the package in your Python scripts.")
        st.code("from web3bms import crm", language="python")
        st.toast('Try it out in Python', icon='🐍')