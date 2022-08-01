import pdfkit
from jinja2 import Environment, PackageLoader, select_autoescape, FileSystemLoader
from datetime import date
import streamlit as st
from streamlit.components.v1 import iframe

st.set_page_config(layout="centered", page_icon="❄️", page_title="streamlitCRM Invoice Generator")
st.title("❄️ streamlitCRM Invoice Generator")

st.write(
    "This app shows you how you can use Streamlit to make a invoice in your business!"
)

left, right = st.columns(2)

right.write("Here is the Invoice Template:")

env = Environment(loader=FileSystemLoader("."), autoescape=select_autoescape())
template = env.get_template("template.html")


left.write("Who was the client:")
form = left.form("template_form")
service = form.text_input("Invoice Service")
client = form.selectbox(
    "Client",
    ["CNN", "Penn State","Coca Cola Florida LLC","McAfee"],
    index=0,
)
rate = form.number_input("Hourly Rate", 1, 10000, 90)
submit = form.form_submit_button("Generate Invoice")

if submit:
    html = template.render(
        service=service,
        client=client,
        rate=rate,
        date=date.today().strftime("%B %d, %Y"),
    )
    pdf = pdfkit.from_string(html, False)
    st.balloons()
    right.download_button(
        "⬇️ Download PDF",
        data=pdf,
        file_name="invoice.pdf",
        mime="application/octet-stream",
    )
