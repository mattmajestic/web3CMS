import streamlit as st
from multiapp import MultiApp

app = MultiApp()

app.add_app("Home", home.py)
app.add_app("Invoice", invoice.py)

app.run()
