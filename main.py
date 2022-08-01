from pathlib import Path

import streamlit as st
from streamlit_multipage import MultiPage

app = MultiPage()
app.st = st
app.navbar_name = "Other Apps"
app.start_button = "Start App"
app.navbar_style = "VerticalButton"

app.header = header
app.footer = footer
app.hide_navigation = True
app.hide_menu = True

app.add_app("Invoice", invoice, initial_page=True)

app.run()
