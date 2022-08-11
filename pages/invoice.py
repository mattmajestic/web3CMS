import pdfkit
from jinja2 import Environment, PackageLoader, select_autoescape, FileSystemLoader
from datetime import datetime, date, time, timezone, timedelta
import pandas as pd
import streamlit as st
from streamlit.components.v1 import iframe
import streamlit.components.v1 as components
import requests
import yfinance as yf
import web3
from web3 import Web3, HTTPProvider 
import json

def home_page():
    st.markdown("# Check out the Project ReadMe 🚀")
    st.write("litCRM Readme https://github.com/mattmajestic/litCRM/blob/main/README.md")
    st.markdown("Checkout the Shiny Demo")
    components.iframe("https://drive.google.com/file/d/1bpHOLX8RkjMzXAj5LtHyMrsmpZ06Gipg/preview",640,480)
    st.sidebar.markdown("# Check out the Project Materials")
        
def invoice():
    products = pd.read_csv("./data/products.csv")
    contacts = pd.read_csv("./data/contacts.csv")
    opportunities = pd.read_csv("./data/opportunities.csv")
    st.title("❄ litCRM (Streamlit Based CRM)")
    st.sidebar.markdown("Crypto Invoicing")

    left, right = st.columns([5, 5])

    env = Environment(loader=FileSystemLoader("."), autoescape=select_autoescape())
    template = env.get_template("template.html")

    left.write("Update the Invoice Template Below:")
    start = datetime.today() - timedelta(days=2)
    end = datetime.today()
    service_choices = products[["Name"]]
    form = left.form("template_form")
    service = form.selectbox("Invoice Service",service_choices)
    coin = form.selectbox("Invoice Currency",["ETH","BTC","USDC","USD (Cash)"])
    coin_history = yf.download(tickers=coin, start=start.date(), end=end.date(), interval="1d")
    client = form.selectbox(
    "Client",
    ["CNN", "Penn State","Coca Cola Florida LLC","McAfee"],
    index=0,
    )
    start_period = form.date_input("Start of Invoice Time Period", start)
    hours = form.number_input("Hours", 1, 80, 40)
    rate = form.number_input("Hourly Rate", 1, 10000, 120,120)
    notes = form.text_input("Add Any Additional Notes")
    submit = form.form_submit_button("Generate Invoice")
    coin_addy = right.selectbox("Invoice Currency Price",["0x2170Ed0880ac9A755fd29B2688956BD959F933F8", "0x7130d2A12B9BCbFAe4f2634d864A1Ee1Ce3Ead9c","0x8AC76a51cc950d9822D68b83fE1Ad97B32Cd580d"],index=0)
    apiURL = "https://api.pancakeswap.info/api/v2/tokens/"
    response = requests.get(url = apiURL + coin_addy)
    jsonRaw = response.json()
    right.json(jsonRaw)
    coin_price = float(jsonRaw['data']['price']
    right.text("Invoice Total " + coin_price + " " + coin)

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
    uploaded_file = st.file_uploader("Upload your Clients", type=['csv','xlsx'],accept_multiple_files=False,key="fileUploader")
    st.sidebar.markdown("# Client Management")
    if uploaded_file is not None:
        contacts = pd.read_csv(uploaded_file)
    else:
        contacts = pd.read_csv("./data/contacts.csv")
    st.dataframe(contacts)
    
def products():
    uploaded_file = st.file_uploader("Upload your Products", type=['csv','xlsx'],accept_multiple_files=False,key="fileUploader")
    st.sidebar.markdown("# Product Management")
    if uploaded_file is not None:
        products = pd.read_csv(uploaded_file)
    else:
        products = pd.read_csv("./data/products.csv")
    st.dataframe(products)
    
def opportunities():
    uploaded_file = st.file_uploader("Upload your Opportunities", type=['csv','xlsx'],accept_multiple_files=False,key="fileUploader")
    st.sidebar.markdown("# Opportunities Tracker")
    if uploaded_file is not None:
        opportunities = pd.read_csv(uploaded_file)
    else:
        opportunities = pd.read_csv("./data/opportunities.csv")
    st.dataframe(opportunities)
    
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

page_names_to_funcs = {
    "Home Page": home_page,
    "Invoice": invoice,
    "Clients": clients,
    "Products": products,
    "Opportunties": opportunities,
    "Backend": backend,
    
}
selected_page = st.sidebar.selectbox("Select a page", page_names_to_funcs.keys())
page_names_to_funcs[selected_page]()
