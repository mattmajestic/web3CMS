import streamlit as st
from streamlit_multipage import MultiPage
from multiapp import MultiApp

def my_page(st, **state):
    st.markdown("# Home page 🎈")
    st.sidebar.markdown("# Home page 🎈")

app = MultiApp()

app.add_app("Invoice", invoice.py)

app.run()
