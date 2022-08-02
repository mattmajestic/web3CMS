import streamlit as st
from multiapp import MultiApp
from apps import home, data_stats # import your app modules here

app = MultiApp()

app.add_app("Invoice", invoice.app)

app.run()
