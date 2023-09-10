import streamlit as st

def home_page():

    # columns = st.columns([2, 2, 3, 2, 2, 4, 2])

    # # Loop through page names and labels to create buttons
    # for name, label, column in zip(page_names, page_labels, columns):
    #     url = page_urls.get(label, "")
    #     if url:
    #         button_html = f'<button style="{button_style}" onclick="window.location.href=\'{url}\';">{selection}</button>'
    #         column.markdown(button_html, unsafe_allow_html=True)
    # Read the contents of the README.md file
    with open('README.md', 'r') as file:
        readme_text = file.read()
    st.markdown("""
    <script src="https://cdn.jsdelivr.net/npm/mermaid/dist/mermaid.min.js"></script>
    <script>mermaid.initialize({startOnLoad:true});</script>
    """, unsafe_allow_html=True)
    st.markdown(readme_text, unsafe_allow_html=True)
    st.toast(f'Welcome to web3bms', icon='✅')