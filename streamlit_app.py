import streamlit as st
from multiapp import MultiApp

app = MultiApp()

st.markdown("# Home page 🎈")
st.sidebar.markdown("# Home page 🎈")
app.add_app("Invoice", invoice.py)

app.run()
