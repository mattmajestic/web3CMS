import pdfkit
from jinja2 import Environment, PackageLoader, select_autoescape, FileSystemLoader
from datetime import date
import streamlit as st
from streamlit.components.v1 import iframe

st.set_page_config(layout="centered", page_icon="🎓", page_title="Diploma Generator")
st.title("🎓 Diploma PDF Generator")

st.write(
    "This app shows you how you can use Streamlit to make a PDF generator app in just a few lines of code!"
)

left, right = st.columns(2)

right.write("Here is the Invoice Template:")

right.image("template.png", width=300)

env = Environment(loader=FileSystemLoader("."), autoescape=select_autoescape())
template = env.get_template("template.html")


left.write("Who was the client:")
form = left.form("template_form")
service = form.text_input("Invoice Service")
client = form.selectbox(
    "Client",
    ["Moralis", "Infura"],
    index=0,
)
rate = form.slider("Hourly Rate", 1, 10000, 90)
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

    right.success("🎉 Your invoice was generated!")
    right.download_button(
        "⬇️ Download PDF",
        data=pdf,
        file_name="invoice.pdf",
        mime="application/octet-stream",
    )
