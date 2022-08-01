import streamlit as st
from streamlit_multipage import MultiPage

def my_page(st, **state):
    st.markdown("# Home page 🎈")
    st.sidebar.markdown("# Home page 🎈")

app = MultiApp()
app.st = st

app.add_app("Home", my_page)
app.add_app("Invoice", invoice.py)

app.run()
