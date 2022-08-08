import pdfkit
from jinja2 import Environment, PackageLoader, select_autoescape, FileSystemLoader
from datetime import datetime, date, time, timezone, timedelta
import pandas as pd
import streamlit as st
from streamlit.components.v1 import iframe
import requests
import yfinance as yf

#page1, page2, page3 = st.tabs(["📈 Home", "🗃 Clients","🎲 Invoice"])

def home_page():
    st.markdown("# Home page 🎈")
    st.text("Checkout the Shiny Demo")
    st.iframe("https://drive.google.com/file/d/1bpHOLX8RkjMzXAj5LtHyMrsmpZ06Gipg/preview")
    st.sidebar.markdown("# Home page 🎈")
        
def invoice():
    st.text("litCRM")
    st.title("❄ litCRM (Streamlit Based CRM)")

    left, right = st.columns(2)

    env = Environment(loader=FileSystemLoader("."), autoescape=select_autoescape())
    template = env.get_template("template.html")

    left.write("Update the Invoice Template Below:")
    products = pd.read_csv("./data/products.csv")
    contacts = pd.read_csv("./data/contacts.csv")
    opportunities = pd.read_csv("./data/opportunities.csv")
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
    st.text("Upload your Clients")
    st.file_uploader(fileUploadLabel, type=['csv','xlsx'],accept_multiple_files=False,key="fileUploader")
    st.dataframe(contacts)
    
def products():
    st.text("Upload your Products")
    st.file_uploader(fileUploadLabel, type=['csv','xlsx'],accept_multiple_files=False,key="fileUploader")
    st.dataframe(products)
    
def opportunities():
    st.text("Upload your Opportunities")
    st.file_uploader(fileUploadLabel, type=['csv','xlsx'],accept_multiple_files=False,key="fileUploader")
    st.dataframe(products)
    
def backend():
    st.text("Backend Data a User Updates")
    tab1, tab2, tab3, tab4 = st.tabs(["📈 Contacts", "🗃 Products","🎲 Opportunities","🐪 Crypto History"])
    tab1.dataframe(contacts)
    tab2.dataframe(products)
    tab3.dataframe(opportunities)
    tab4.text("Coin Currency History")
    tab4.table(coin_history)

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
