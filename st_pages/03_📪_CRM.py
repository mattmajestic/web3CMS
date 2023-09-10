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

    products_db = supabase_client.table('products').select("*").execute()
    products_df = pd.DataFrame(products_db.data)
    contacts_db = supabase_client.table('contacts').select("*").execute()
    contacts_df = pd.DataFrame(contacts_db.data)
    opportunities_db = supabase_client.table('opportunities').select("*").execute()
    opportunities_df = pd.DataFrame(opportunities_db.data)
    # Use geopy to get the coordinates for the center of the data points
    # geolocator = Nominatim(user_agent="myGeocoder")
    # location = geolocator.geocode(f"{contacts_df['City'].iloc[0]}, {contacts_df['State'].iloc[0]}")
    # # Create a map centered at an initial location
    # m = folium.Map(location=[location.latitude, location.longitude], zoom_start=5)

    # # Add markers for each company's location
    # for i, row in contact_df.iterrows():
    #     location = geolocator.geocode(f"{row['City']}, {row['State']}")
    #     if location:
    #         folium.Marker(
    #             location=[location.latitude, location.longitude],
    #             popup=row["Company"],
    #         ).add_to(m)

    # Set a common approximate location for all companies (e.g., the center of the USA)
    common_location = "USA"

    # Use Plotly to create a scattergeo map
    fig = px.scatter_geo(
        contacts_df,
        locations=[common_location] * len(contacts_df),  # Set the same location for all companies
        locationmode='USA-states',
        text='Company',
        scope='usa',
    )

    # Update layout settings
    fig.update_layout(
        geo=dict(
            center=dict(lat=39.8283, lon=-98.5795),  # Centered at the approximate USA coordinates
            scope='usa',
        ),
    )

    st.title("Open Sourced CRM 📪")
    tab1, tab2, tab3 = st.tabs(["📈 Clients", "🗃 Products","🎲 Opportunities"])
    tab1.file_uploader("Upload your Clients", type=['csv','xlsx'],accept_multiple_files=False,key="fileUploader")
    tab1.write("Edit Data Table")
    tab1.data_editor(contacts_df)
    # Display the map using st.plotly_chart
    # tab1.plotly_chart(fig)
    tab1.button("Save Clients Table")
    tab2.file_uploader("Upload your Products", type=['csv','xlsx'],accept_multiple_files=False,key="products_upload")
    tab2.write("Edit Data Table")
    tab2.data_editor(products_df)
    tab2.button("Save Products Table")
    tab3.file_uploader("Upload your Opportunities", type=['csv','xlsx'],accept_multiple_files=False,key="ops_upload")
    tab3.write("Edit Data Table")
    tab3.data_editor(opportunities_df)
    tab3.button("Save Ops Table")
    tab4.text("CoinGecko API")
    # cg = CoinGeckoAPI()
    # cg_category = cg.get_coins_categories()
    # jsonRaw = json.dumps(cg_category)
    # df = pd.read_json(jsonRaw)
    # tab4.dataframe(df)