import pdfkit
from jinja2 import Environment, PackageLoader, select_autoescape, FileSystemLoader
from datetime import date
import datetime
import pandas as pd
import streamlit as st
from streamlit.components.v1 import iframe
import requests

st.set_page_config(layout="centered", page_icon="🐪", page_title=" litCRM")
st.title("❄ litCRM (Streamlit Based CRM)")

left, right = st.columns(2)

env = Environment(loader=FileSystemLoader("."), autoescape=select_autoescape())
template = env.get_template("template.html")

left.write("Update the Invoice Template Below:")
products = pd.read_csv("./data/products.csv")
contacts = pd.read_csv("./data/contacts.csv")
opportunities = pd.read_csv("./data/opportunities.csv")
request = requests.get('https://w3schools.com/python/demopage.htm')
service_choices = products[["Name"]]
form = left.form("template_form")
service = form.selectbox("Invoice Service",service_choices)
coin = form.selectbox("Invoice Currency",["ETH","BTC","USDC","USD (Cash)"])
client = form.selectbox(
    "Client",
    ["CNN", "Penn State","Coca Cola Florida LLC","McAfee"],
    index=0,
)
start_period = form.date_input("Start of Invoice Time Period", datetime.date(2022, 8, 11))
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
st.text("Backend Data a User Updates")
st.text(request.status_code)
tab1, tab2, tab3 = st.tabs(["📈 Contacts", "🗃 Products","🎲 Opportunities"])
tab1.dataframe(contacts)
tab2.dataframe(products)
tab3.dataframe(opportunities)
