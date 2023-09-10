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


st.set_page_config(
     page_title="web3BMS",
     page_icon="💾",
     layout="wide",
     initial_sidebar_state='expanded'
 )

# # Define custom query parameters for each page
# page_queries = {
#     "home": "Home 🐧",
#     "invoice": "Invoice 📋",
#     "crm": "CRM 📪",
#     "ai_chat": "AI Chat 💻",
#     "developer_docs": "Developer Docs 🚝",
#     "developer_request": "Developer Request ☎️",
#     "ml_ops": "ML Ops 👾"
# }

# # Get the current URL query parameters
# query_params = st.experimental_get_query_params()

# # Determine the selected page from the query parameters (default to "home")
# selected_page = query_params.get("page", ["home"])[0]

# # Create a sidebar navigation menu
# selected_page = st.sidebar.radio("Navigate web3bms", list(page_queries.values()), index=list(page_queries.keys()).index(selected_page))

# # Set the query parameter to the selected page
# selected_page_key = next(key for key, value in page_queries.items() if value == selected_page)
# st.experimental_set_query_params(page=selected_page_key)

# Get a list of available page files in the 'pages' directory
page_files = [file for file in os.listdir('pages') if file.endswith('.py')]

# Create a dictionary to store page names and their respective module names
pages = {file.replace('.py', ''): file.replace('.py', '') for file in page_files}

# Sidebar navigation
st.sidebar.title("Navigation")
selected_page = st.sidebar.selectbox("Select a Page", list(pages.keys()))

# Import and run the selected page
if selected_page in pages:
    page_module = __import__('pages.' + pages[selected_page], fromlist=[selected_page])
    page_module.main()
else:
    st.error("Page not found.")
