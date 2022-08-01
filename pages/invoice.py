import pdfkit
from jinja2 import Environment, PackageLoader, select_autoescape, FileSystemLoader
from datetime import date
import pandas as pd
import streamlit as st
from streamlit.components.v1 import iframe

st.set_page_config(layout="centered", page_icon="🐪", page_title=" litCRM")
st.title("❄ litCRM (Streamlit Based CRM)")

left, right = st.columns(2)

env = Environment(loader=FileSystemLoader("."), autoescape=select_autoescape())
template = env.get_template("template.html")

left.write("Update the Invoice Template Below:")
products = pd.read_csv("./data/products.csv")
contacts = pd.read_csv("./data/contacts.csv")
service_choices = products[["Name"]]
dates = st.date_input(
     "Invoice Time Period",
     datetime.today().strftime('%Y-%m-%d'))
st.write('Invoice Time Period', d)
form = left.form("template_form")
service = form.selectbox("Invoice Service",service_choices)
client = form.selectbox(
    "Client",
    ["CNN", "Penn State","Coca Cola Florida LLC","McAfee"],
    index=0,
)
hours = form.number_input("Hours", 1, 80, 40)
rate = form.number_input("Hourly Rate", 1, 10000, 120,120)
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
    right.title("Here's your invoice")
    right.download_button(
        "🌀 Download PDF",
        data=pdf,
        file_name="invoice.pdf",
        mime="application/octet-stream",
    )
st.text("Backend Data")
tab1, tab2 = st.tabs(["📈 Contacts", "🗃 Products"])
tab1.dataframe(contacts)
tab2.dataframe(products)
