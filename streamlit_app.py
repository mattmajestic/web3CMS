import streamlit as st

def home_page():
    st.markdown("# Home page 🎈")
    st.sidebar.markdown("# Home page 🎈")

def invoice():
    st.markdown("# Invoice ❄️")
    st.sidebar.markdown("# Invoice ❄️")

page_names_to_funcs = {
    "Home Page": home_page,
    "Invoice Generator": invoice
}

selected_page = st.sidebar.selectbox("Select a page", page_names_to_funcs.keys())
page_names_to_funcs[selected_page]()
