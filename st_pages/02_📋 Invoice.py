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

    cg_html = '''
    <script src="https://widgets.coingecko.com/coingecko-coin-list-widget.js"></script><coingecko-coin-list-widget  coin-ids="bitcoin,ethereum" currency="usd" locale="en"></coingecko-coin-list-widget>
    '''

    cg_marquee = '''
    <script src="https://widgets.coingecko.com/coingecko-coin-price-marquee-widget.js"></script><coingecko-coin-price-marquee-widget  coin-ids="bitcoin,ethereum,eos,ripple,litecoin" currency="usd" background-color="#100f0f" locale="en" font-color="#fefbfb"></coingecko-coin-price-marquee-widget>
    '''

    left, center, right = st.columns([5, 2, 5])

    env = Environment(loader=FileSystemLoader("."), autoescape=select_autoescape())
    template = env.get_template("template.html")
    left.write("Update the Invoice Template Below:")
    start = datetime.today() - timedelta(days=2)
    end = datetime.today()
    service_choices = products_df[["Name"]]
    form = left.form("template_form")
    service = form.selectbox("Invoice Service", service_choices)
    client = form.selectbox("Client", ["CNN", "Penn State", "Coca Cola Florida LLC", "McAfee"], index=0)
    start_period = form.date_input("Start of Invoice Time Period", start)
    hours = form.number_input("Hours", 1, 80, 40)
    rate = form.number_input("Hourly Rate", 1, 10000, 120, 120)
    coin_type = form.radio("Select Cryptocurrency Payment", ["No Crypto", "BTC", "ETH"], index=1, horizontal=True)  # Set BTC as the default
    notes = form.text_input("Add Any Additional Notes")
    submit = form.form_submit_button("Generate Invoice")
    coin_ids = {"BTC": "bitcoin", "ETH": "ethereum"}
    selected_coin_id = coin_ids[coin_type]
    cg = CoinGeckoAPI()
    coin_price = cg.get_price(ids=selected_coin_id, vs_currencies='usd')[selected_coin_id]['usd']

    if coin_type:
        crypto_expander = right.expander("🤝 Crypto Accounts", expanded=True)
        with crypto_expander:
            crypto_percentage = st.number_input("Percentage of Invoice to be Paid with Crypto", min_value=5, max_value=50, step=5, value=5)
            coin_addy = st.selectbox("Stored Crypto Address",
                                ["0x2170Ed0880ac9A755fd29B2688956BD959F933F8", "0x7130d2A12B9BCbFAe4f2634d864A1Ee1Ce3Ead9c"], index=0)
            invoice_usd = hours * rate                   
            invoice_crypto_value = (invoice_usd * crypto_percentage) / 100
            invoice_msg = f"Invoice Total ({coin_type}): {invoice_crypto_value:.4f} {coin_type}"
            st.text(invoice_msg)

    if submit:
        html = template.render(
            service=service,
            client=client,
            rate=rate,
            date=date.today().strftime("%B %d, %Y"),
        )
        pdf = pdfkit.from_string(html, False)
        right.balloons()
        right.title("Here you go")
        right.download_button(
            "🌀 Download Invoice",
            data=pdf,
            file_name="invoice.pdf",
            mime="application/octet-stream",
        )

    # meetings_expander = right.expander("🤝 Meetings")
    # with meetings_expander:
    #     st.write("Calculate Meeting Costs")
    #     weekly_meeting_hours = st.number_input("Weekly Meeting Hours", min_value=0, value=10)
    #     annual_salary = st.number_input("Annual Salary ($)", min_value=0, value=50000)
    #     hourly_rate = annual_salary / (52 * weekly_meeting_hours) if weekly_meeting_hours > 0 else 0
    #     st.write(f"Hourly Rate: ${hourly_rate:.2f}")

    # metamask_expander = right.expander("🔐 MetaMask")
    # with metamask_expander:
    #     st.write("Connect Your MetaMask Wallet")
    #     st.markdown("To connect your MetaMask wallet, follow these steps:")
    #     st.markdown("1. Install the MetaMask extension in your browser if you haven't already.")
    #     st.markdown("2. Click on the MetaMask icon in your browser's toolbar.")
    #     st.markdown("3. Create a new MetaMask wallet or import an existing one if you have.")
    #     st.markdown("4. Click the 'Connect' button below to connect your wallet.")
    #     components.html(cg_html)
    #     connect_button = wallet_connect(label="wallet", key="wallet")
    #     if connect_button != "not":
    #         st.success('Connected', icon="✅")
    #         st.write(connect_button)

    # Show the BTC Pay Server
    # btc_expander = right.expander("💸 Donate BTC ")
    # with btc_expander:
    #     url = "https://mainnet.demo.btcpayserver.org/api/v1/invoices?storeId=4r8DKKKMkxGPVKcW9TXB2eta7PTVzzs192TWM3KuY52e&price=100&currency=USD&defaultPaymentMethod=BTC"
    #     link = 'Pay with BTC [via this link](https://mainnet.demo.btcpayserver.org/api/v1/invoices?storeId=4r8DKKKMkxGPVKcW9TXB2eta7PTVzzs192TWM3KuY52e&price=100&currency=USD&defaultPaymentMethod=BTC)'
    #     st.markdown(link, unsafe_allow_html=True)
    #     components.iframe(url, width=300, height=500, scrolling=True)

    components.html(cg_marquee)
    st.toast(f'Invoice crypto!', icon='✅')
