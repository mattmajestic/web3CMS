import streamlit as st
from streamlit.components.v1 import iframe, html
import streamlit.components.v1 as components
from streamlit_javascript import st_javascript
from wallet_connect import wallet_connect
import pdfkit
from jinja2 import Environment, PackageLoader, select_autoescape, FileSystemLoader
from datetime import datetime, date, time, timezone, timedelta
import pandas as pd
import requests
import yfinance as yf
from pycoingecko import CoinGeckoAPI
from web3 import Web3, HTTPProvider 
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
from streamlit_extras.switch_page_button import switch_page

# Read the contents of the README.md file
with open('README.md', 'r') as file:
    readme_text = file.read()

def home_page():
    st.markdown("""
    <script src="https://cdn.jsdelivr.net/npm/mermaid/dist/mermaid.min.js"></script>
    <script>mermaid.initialize({startOnLoad:true});</script>
    """, unsafe_allow_html=True)
    st.markdown(readme_text, unsafe_allow_html=True)