import streamlit as st
from streamlit.components.v1 import iframe
from streamlit.components.v1 import html
import streamlit.components.v1 as components
from streamlit_javascript import st_javascript
import pdfkit
from jinja2 import Environment, PackageLoader, select_autoescape, FileSystemLoader
from datetime import datetime, date, time, timezone, timedelta
import pandas as pd
import requests
import yfinance as yf
from pycoingecko import CoinGeckoAPI
import web3
from web3 import Web3, HTTPProvider 
import json
import time
from lunarcrush import LunarCrush

# Read the contents of the README.md file
    with open('README.md', 'r') as file:
        readme_text = file.read()

st.set_page_config(
     page_title="web3BMS",
     page_icon="🚀",
     layout="wide",
     initial_sidebar_state="expanded"
 )

def home_page():
    st.title("❄ web3BMS (Web3 Enabled Business Management Solution)")
    st.markdown(readme_text)

def invoice():
    products = pd.read_csv("./data/products.csv")
    contacts = pd.read_csv("./data/contacts.csv")
    opportunities = pd.read_csv("./data/opportunities.csv")
    
    cg_html = '''
    <script src="https://widgets.coingecko.com/coingecko-coin-list-widget.js"></script><coingecko-coin-list-widget  coin-ids="bitcoin,ethereum" currency="usd" locale="en"></coingecko-coin-list-widget>
    '''
    st.title("❄ litBMS (Streamlit Based Crypto Business Management Solutions)")
    st.sidebar.markdown("Crypto Invoicing")

    left,center, right = st.columns([5,2,5])

    env = Environment(loader=FileSystemLoader("."), autoescape=select_autoescape())
    template = env.get_template("template.html")
    left.write("Update the Invoice Template Below:")
    start = datetime.today() - timedelta(days=2)
    end = datetime.today()
    service_choices = products[["Name"]]
    form = left.form("template_form")
    service = form.selectbox("Invoice Service",service_choices)
    client = form.selectbox("Client",["CNN", "Penn State","Coca Cola Florida LLC","McAfee"],index=0)
    start_period = form.date_input("Start of Invoice Time Period", start)
    hours = form.number_input("Hours", 1, 80, 40)
    rate = form.number_input("Hourly Rate", 1, 10000, 120,120)
    notes = form.text_input("Add Any Additional Notes")
    submit = form.form_submit_button("Generate Invoice")
    coin_addy = right.selectbox("Invoice Currency Price",["0x2170Ed0880ac9A755fd29B2688956BD959F933F8", "0x7130d2A12B9BCbFAe4f2634d864A1Ee1Ce3Ead9c","0x8AC76a51cc950d9822D68b83fE1Ad97B32Cd580d"],index=0)
    apiURL = "https://api.pancakeswap.info/api/v2/tokens/"
    response = requests.get(url = apiURL + coin_addy)
    jsonRaw = response.json()
    coin_price = float(jsonRaw['data']['price'])
    usd_total = hours * rate
    invoice_total = usd_total/coin_price
    coin = right.selectbox("Invoice Currency",["ETH","BTC","USDC","USD (Cash)"],index=0)
    invoice_msg = "Invoice Total " + coin
    right.text(invoice_msg)
    right.write(invoice_total)
    with right:
         components.html(cg_html)

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

def clients():
    st.snow()
    left,right = st.columns([5,5])
    uploaded_file = left.file_uploader("Upload your Clients", type=['csv','xlsx'],accept_multiple_files=False,key="fileUploader")
    st.sidebar.markdown("# Client Management")
    if uploaded_file is not None:
        contacts = pd.read_csv(uploaded_file)
    else:
        contacts = pd.read_csv("./data/contacts.csv")
    right.dataframe(contacts)
    my_bar = st.progress(0)
    for percent_complete in range(100):
         time.sleep(0.05)
         my_bar.progress(percent_complete + 1)
    my_bar.empty()

def products():
    left, right = st.columns([5,5])
    uploaded_file = left.file_uploader("Upload your Products", type=['csv','xlsx'],accept_multiple_files=False,key="fileUploader")
    st.sidebar.markdown("# Product Management")
    if uploaded_file is not None:
        products = pd.read_csv(uploaded_file)
    else:
        products = pd.read_csv("./data/products.csv")
    right.dataframe(products)
    my_bar = st.progress(0)
    for percent_complete in range(100):
         time.sleep(0.05)
         my_bar.progress(percent_complete + 1)
    my_bar.empty()

def opportunities():
    left,right = st.columns([5,5])
    uploaded_file = left.file_uploader("Upload your Opportunities", type=['csv','xlsx'],accept_multiple_files=False,key="fileUploader")
    st.sidebar.markdown("# Opportunities Tracker")
    if uploaded_file is not None:
        opportunities = pd.read_csv(uploaded_file)
    else:
        opportunities = pd.read_csv("./data/opportunities.csv")
    right.dataframe(opportunities)
    my_bar = st.progress(0)
    for percent_complete in range(100):
         time.sleep(0.05)
         my_bar.progress(percent_complete + 1)
    my_bar.empty()

def backend():
    products = pd.read_csv("./data/products.csv")
    contacts = pd.read_csv("./data/contacts.csv")
    opportunities = pd.read_csv("./data/opportunities.csv")
    st.text("Backend Data a User Updates")
    tab1, tab2, tab3, tab4 = st.tabs(["📈 Contacts", "🗃 Products","🎲 Opportunities","🐪 Crypto History"])
    tab1.dataframe(contacts)
    tab2.dataframe(products)
    tab3.dataframe(opportunities)
    tab4.text("Coin Currency History")
    coin_addy = tab4.selectbox("Coin Adrress",["0x2170Ed0880ac9A755fd29B2688956BD959F933F8", "0x7130d2A12B9BCbFAe4f2634d864A1Ee1Ce3Ead9c"],index=0)
    apiURL = "https://api.pancakeswap.info/api/v2/tokens/"
    response = requests.get(url = apiURL + coin_addy)
    jsonRaw = response.json()
    tab4.json(jsonRaw)
     
def api():
    left, center, right = st.columns([4,4,4])
    cg = CoinGeckoAPI() 
    btc = cg.get_price(ids='bitcoin', vs_currencies='usd', include_market_cap='true', include_24hr_vol='true', include_24hr_change='true', include_last_updated_at='true')
    with left.container():
        left.title("Coin Gecko API")
        left.json(btc)
        left.image("https://static.coingecko.com/s/coingecko-mascot-suit-b1a9df2b041094a017948f1d184f1aa263e779d4e1f22c437e835b74f0b00073.png",width=200)
    with center.container():
        center.title("PancakeSwap API")
        apiURL = "https://api.pancakeswap.info/api/v2/tokens/"
        coin_addy = center.selectbox("Invoice Currency Price",["0x2170Ed0880ac9A755fd29B2688956BD959F933F8", "0x7130d2A12B9BCbFAe4f2634d864A1Ee1Ce3Ead9c","0x8AC76a51cc950d9822D68b83fE1Ad97B32Cd580d"],index=0)
        response = requests.get(url = apiURL + coin_addy)
        pancake = response.json()
        center.json(pancake)
        center.image("https://www.pngall.com/wp-content/uploads/10/PancakeSwap-Crypto-Logo-PNG-Images.png",width=200)
    lc = LunarCrush()
    eth_1_year_data = lc.get_assets(symbol=['ETH'],data_points=365, interval='day')
    with right.container():
        right.title("LunarCrush API")
        right.image("https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSwRhSbOtWFqO4IjI0vcb_gNsTK644-bdO3t_YkW_qq&s",width=200)
        right.write(eth_1_year_data)

page_names_to_funcs = {
    "Home Page": home_page,
    "Invoice": invoice,
    "Clients": clients,
    "Products": products,
    "Opportunties": opportunities,
    "API Feeds": api,
    "Backend": backend,
    
}
selected_page = st.sidebar.selectbox("Select a page", page_names_to_funcs.keys())
page_names_to_funcs[selected_page]()
