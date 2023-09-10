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

def main():

    # columns = st.columns([2, 2, 3, 2, 2, 4, 2])

    # # Loop through page names and labels to create buttons
    # for name, label, column in zip(page_names, page_labels, columns):
    #     url = page_urls.get(label, "")
    #     if url:
    #         button_html = f'<button style="{button_style}" onclick="window.location.href=\'{url}\';">{selection}</button>'
    #         column.markdown(button_html, unsafe_allow_html=True)
    # Read the contents of the README.md file
    with open('README.md', 'r') as file:
        readme_text = file.read()
    st.markdown("""
    <script src="https://cdn.jsdelivr.net/npm/mermaid/dist/mermaid.min.js"></script>
    <script>mermaid.initialize({startOnLoad:true});</script>
    """, unsafe_allow_html=True)
    st.markdown(readme_text, unsafe_allow_html=True)
    st.toast(f'Welcome to web3bms', icon='✅')