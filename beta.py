import streamlit as st
from streamlit.components.v1 import iframe
from streamlit.components.v1 import html
import streamlit.components.v1 as components
from streamlit_javascript import st_javascript
from wallet_connect import wallet_connect
import pdfkit
from jinja2 import Environment, PackageLoader, select_autoescape, FileSystemLoader
from datetime import datetime, date, time, timezone, timedelta
import pandas as pd
import requests
import yfinance as yf
from pycoingecko import CoinGeckoAPI
from web3 import Web3, HTTPProvider 
import json
import time
# from lunarcrush import LunarCrush
import supabase
import os
import folium
from geopy.geocoders import Nominatim
import plotly.express as px

# Set your Supabase credentials as environment variables
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

# Initialize Supabase
supabase_client = supabase.Client(SUPABASE_URL, SUPABASE_KEY)

# Read the contents of the README.md file
with open('README.md', 'r') as file:
    readme_text = file.read()

# Read the content of the HTML file
with open("index.html", "r") as file:
    metamask_html = file.read()

# Load and render the main.js file
    with open("metamask/main.js", "r") as js_file:
        js_code = js_file.read()

# # Define the JavaScript code to connect Metamask
# metamask_js = """
#     <script>
#         // JavaScript code to connect Metamask
#         const connectMetamask = () => {
#             if (typeof window.ethereum !== 'undefined') {
#                 startLoading();

#                 ethereum
#                     .request({ method: 'eth_requestAccounts' })
#                     .then((accounts) => {
#                         const account = accounts[0];
#                         walletID.innerHTML = `Wallet connected: <span>${account}</span>`;
#                         stopLoading();
#                     })
#                     .catch((error) => {
#                         console.log(error, error.code);
#                         alert(error.code);
#                         stopLoading();
#                     });
#             } else {
#                 if (isMobile()) {
#                     mobileDeviceWarning.classList.add('show');
#                 } else {
#                     window.open('https://metamask.io/download/', '_blank');
#                     installAlert.classList.add('show');
#                 }
#             }
#         };
#     </script>
# """

# clerk_js = st_javascript("""
#   async
#   crossorigin="anonymous"
#   data-clerk-publishable-key="pk_test_Zmxvd2luZy1oYWdmaXNoLTUuY2xlcmsuYWNjb3VudHMuZGV2JA"
#   onload="window.Clerk.load()"
#   src="https://flowing-hagfish-5.clerk.accounts.dev/npm/@clerk/clerk-js@4/dist/clerk.browser.js"
#   type="text/javascript"
# """)


st.set_page_config(
     page_title="web3BMS",
     page_icon="🚀",
     layout="wide",
     initial_sidebar_state='expanded'
 )

def home_page():
    st.markdown("""
    <script src="https://cdn.jsdelivr.net/npm/mermaid/dist/mermaid.min.js"></script>
    <script>mermaid.initialize({startOnLoad:true});</script>
    """, unsafe_allow_html=True)
    st.markdown(readme_text, unsafe_allow_html=True)

# def signin():
#     st.markdown(clerk_js, unsafe_allow_html=True)

def invoice():
    # Replace with supabase fetch
    products_db = supabase_client.table('products').select("*").execute()
    products_df = pd.DataFrame(products_db.data)
    # products = pd.read_csv("./data/products.csv")
    # Replace with supabase fetch
    contacts_db = supabase_client.table('contacts').select("*").execute()
    contacts_df = pd.DataFrame(contacts_db.data)
    # contacts = pd.read_csv("./data/contacts.csv")
    # Replace with supabase fetch
    opportunities_db = supabase_client.table('opportunities').select("*").execute()
    opportunities_df = pd.DataFrame(opportunities_db.data)
    # opportunities = pd.read_csv("./data/opportunities.csv")
    
    cg_html = '''
    <script src="https://widgets.coingecko.com/coingecko-coin-list-widget.js"></script><coingecko-coin-list-widget  coin-ids="bitcoin,ethereum" currency="usd" locale="en"></coingecko-coin-list-widget>
    '''

    st.sidebar.markdown("Crypto Invoicing")

    left, center, right = st.columns([5, 2, 5])

    env = Environment(loader=FileSystemLoader("."), autoescape=select_autoescape())
    template = env.get_template("template.html")
    left.write("Update the Invoice Template Below:")
    start = datetime.today() - timedelta(days=2)
    end = datetime.today()
    service_choices = products_df[["Name"]]
    form = left.form("template_form")
    service = form.selectbox("Invoice Service", service_choices)
    client = form.selectbox("Client", ["CNN", "Penn State", "Coca Cola Florida LLC", "McAfee"], index=0)
    start_period = form.date_input("Start of Invoice Time Period", start)
    hours = form.number_input("Hours", 1, 80, 40)
    rate = form.number_input("Hourly Rate", 1, 10000, 120, 120)
    currency_type = form.checkbox("Select Currency Type", value=False)
    if currency_type:
        crypto_type = form.selectbox("Select Cryptocurrency Type", ["BTC", "ETH", "USDC"], index=0)

submit = form.form_submit_button("Generate Invoice")
    notes = form.text_input("Add Any Additional Notes")
    submit = form.form_submit_button("Generate Invoice")
    coin_addy = right.selectbox("Invoice Send Address",
                               ["0x2170Ed0880ac9A755fd29B2688956BD959F933F8", "0x7130d2A12B9BCbFAe4f2634d864A1Ee1Ce3Ead9c",
                                "0x8AC76a51cc950d9822D68b83fE1Ad97B32Cd580d"], index=0)
    apiURL = "https://api.pancakeswap.info/api/v2/tokens/"
    response = requests.get(url=apiURL + coin_addy)
    jsonRaw = response.json()
    cg = CoinGeckoAPI()
    coin_price = cg.get_price(ids='bitcoin', vs_currencies='usd')['bitcoin']['usd']
    usd_total = hours * rate
    invoice_total = usd_total / coin_price
    coin = right.selectbox("Invoice Currency", ["ETH", "BTC", "USDC", "USD (Cash)"], index=0)
    invoice_msg = "Invoice Total " + coin
    right.text(invoice_msg)
    right.write(invoice_total)

    if submit:
        html = template.render(
            service=service,
            client=client,
            rate=rate,
            date=date.today().strftime("%B %d, %Y"),
        )
        pdf = pdfkit.from_string(html, False)
        right.balloons()
        right.title("Here you go")
        right.download_button(
            "🌀 Download Invoice",
            data=pdf,
            file_name="invoice.pdf",
            mime="application/octet-stream",
        )

    # Expander for "Meetings" section
    meetings_expander = right.expander("🤝 Meetings")
    with meetings_expander:
        st.write("Calculate Meeting Costs")

        # Numeric input for weekly meeting hours
        weekly_meeting_hours = st.number_input("Weekly Meeting Hours", min_value=0, value=10)

        # Numeric input for person's annual salary
        annual_salary = st.number_input("Annual Salary ($)", min_value=0, value=50000)

        # Calculate meeting costs based on hourly rate
        hourly_rate = annual_salary / (52 * weekly_meeting_hours) if weekly_meeting_hours > 0 else 0
        st.write(f"Hourly Rate: ${hourly_rate:.2f}")

        # You can add additional calculations or information as needed.

    # Expander for "MetaMask" section
    metamask_expander = right.expander("🔐 MetaMask")
    with metamask_expander:
        st.write("Connect Your MetaMask Wallet")

        st.markdown("To connect your MetaMask wallet, follow these steps:")
        st.markdown("1. Install the MetaMask extension in your browser if you haven't already.")
        st.markdown("2. Click on the MetaMask icon in your browser's toolbar.")
        st.markdown("3. Create a new MetaMask wallet or import an existing one if you have.")
        st.markdown("4. Click the 'Connect' button below to connect your wallet.")

        components.html(cg_html)
        connect_button = wallet_connect(label="wallet", key="wallet")
        if connect_button != "not":
            st.success('Connected', icon="✅")
            st.write(connect_button)

    # Show the BTC Pay Server
    btc_expander = st.expander("Donate BTC 💸")
    with btc_expander:
        url = "https://mainnet.demo.btcpayserver.org/api/v1/invoices?storeId=4r8DKKKMkxGPVKcW9TXB2eta7PTVzzs192TWM3KuY52e&price=100&currency=USD&defaultPaymentMethod=BTC"
        link = 'Pay with BTC [via this link](https://mainnet.demo.btcpayserver.org/api/v1/invoices?storeId=4r8DKKKMkxGPVKcW9TXB2eta7PTVzzs192TWM3KuY52e&price=100&currency=USD&defaultPaymentMethod=BTC)'
        st.markdown(link, unsafe_allow_html=True)
        components.iframe(url, width=300, height=500, scrolling=True)

def ai_chat():
    st.title("GPT chat with your Business Data")
    st.write("Submit Prompt Below")
    prompt = st.chat_input("Chat your Business with AI")
    if prompt:
        st.write(f"User has sent the following prompt: {prompt}")


def meetings():
    st.title("Time Index Calculator")
    st.write("Calculate time spent in your organization")

    # Input fields for Google credentials
    email = st.text_input("Email", "")
    password = st.text_input("Password", "", type="password")

    # Submit button for Google credentials
    if st.button("Submit Credentials"):
        if email and password:
            # You can perform actions related to Google here, e.g., fetching meeting data
            # Replace this with your own code to interact with the Google API
            st.success("Credentials submitted successfully. Fetching meeting data...")

            # Perform actions with Google API using the provided credentials
            # Example: Fetch meeting data here

        else:
            st.error("Please enter both email and password.")

    # Input field for meeting count
    meeting_count = st.number_input("Number of Meetings (approximate)", min_value=0, value=0)

    # Input field for annual salary
    annual_salary = st.number_input("Annual Salary (USD)", min_value=0, value=0)

    if st.button("Calculate"):
        if meeting_count > 0 and annual_salary > 0:
            # Calculate time index
            hours_per_week = meeting_count * (1 / 5) * 8  # Assuming 8 hours per workday and 5 workdays per week
            time_index = hours_per_week / 40
            st.write(f"Time Index: {time_index:.2f}")
        else:
            st.error("Please enter valid values for meeting count and annual salary.")


# def clients():
#     st.snow()
#     left,right = st.columns([5,5])
#     uploaded_file = left.file_uploader("Upload your Clients", type=['csv','xlsx'],accept_multiple_files=False,key="fileUploader")
#     st.sidebar.markdown("# Client Management")
#     if uploaded_file is not None:
#         contacts = pd.read_csv(uploaded_file)
#     else:
#         contacts = pd.read_csv("./data/contacts.csv")
#     right.dataframe(contacts)
#     my_bar = st.progress(0)
#     for percent_complete in range(100):
#          time.sleep(0.05)
#          my_bar.progress(percent_complete + 1)
#     my_bar.empty()

# def products():
#     left, right = st.columns([5,5])
#     uploaded_file = left.file_uploader("Upload your Products", type=['csv','xlsx'],accept_multiple_files=False,key="fileUploader")
#     st.sidebar.markdown("# Product Management")
#     if uploaded_file is not None:
#         products = pd.read_csv(uploaded_file)
#     else:
#         products = pd.read_csv("./data/products.csv")
#     right.dataframe(products)
#     my_bar = st.progress(0)
#     for percent_complete in range(100):
#          time.sleep(0.05)
#          my_bar.progress(percent_complete + 1)
#     my_bar.empty()

# def opportunities():
#     left,right = st.columns([5,5])
#     uploaded_file = left.file_uploader("Upload your Opportunities", type=['csv','xlsx'],accept_multiple_files=False,key="fileUploader")
#     st.sidebar.markdown("# Opportunities Tracker")
#     if uploaded_file is not None:
#         opportunities = pd.read_csv(uploaded_file)
#     else:
#         opportunities = pd.read_csv("./data/opportunities.csv")
#     right.dataframe(opportunities)
#     my_bar = st.progress(0)
#     for percent_complete in range(100):
#          time.sleep(0.05)
#          my_bar.progress(percent_complete + 1)
#     my_bar.empty()

def backend():
    # Replace with supabase fetch
    products_db = supabase_client.table('products').select("*").execute()
    products_df = pd.DataFrame(products_db.data)
    # products = pd.read_csv("./data/products.csv")
    # Replace with supabase fetch
    contacts_db = supabase_client.table('contacts').select("*").execute()
    contacts_df = pd.DataFrame(contacts_db.data)
    # contacts = pd.read_csv("./data/contacts.csv")
    # Replace with supabase fetch
    opportunities_db = supabase_client.table('opportunities').select("*").execute()
    opportunities_df = pd.DataFrame(opportunities_db.data)
    # opportunities = pd.read_csv("./data/opportunities.csv")
    # Use geopy to get the coordinates for the center of the data points
    # geolocator = Nominatim(user_agent="myGeocoder")
    # location = geolocator.geocode(f"{contacts_df['City'].iloc[0]}, {contacts_df['State'].iloc[0]}")
    # # Create a map centered at an initial location
    # m = folium.Map(location=[location.latitude, location.longitude], zoom_start=5)

    # # Add markers for each company's location
    # for i, row in contact_df.iterrows():
    #     location = geolocator.geocode(f"{row['City']}, {row['State']}")
    #     if location:
    #         folium.Marker(
    #             location=[location.latitude, location.longitude],
    #             popup=row["Company"],
    #         ).add_to(m)

    # Set a common approximate location for all companies (e.g., the center of the USA)
    common_location = "USA"

    # Use Plotly to create a scattergeo map
    fig = px.scatter_geo(
        contacts_df,
        locations=[common_location] * len(contacts_df),  # Set the same location for all companies
        locationmode='USA-states',
        text='Company',
        scope='usa',
    )

    # Update layout settings
    fig.update_layout(
        geo=dict(
            center=dict(lat=39.8283, lon=-98.5795),  # Centered at the approximate USA coordinates
            scope='usa',
        ),
    )

    st.text("CRM Uploads")
    tab1, tab2, tab3, tab4 = st.tabs(["📈 Clients", "🗃 Products","🎲 Opportunities","🐪 Crypto Integration"])
    tab1.file_uploader("Upload your Clients", type=['csv','xlsx'],accept_multiple_files=False,key="fileUploader")
    tab1.write("Edit Data Table")
    tab1.data_editor(contacts_df)
    # Display the map using st.plotly_chart
    # tab1.plotly_chart(fig)
    tab1.button("Save Clients Table")
    tab2.file_uploader("Upload your Products", type=['csv','xlsx'],accept_multiple_files=False,key="products_upload")
    tab2.write("Edit Data Table")
    tab2.data_editor(products_df)
    tab2.button("Save Products Table")
    tab3.file_uploader("Upload your Opportunities", type=['csv','xlsx'],accept_multiple_files=False,key="ops_upload")
    tab3.write("Edit Data Table")
    tab3.data_editor(opportunities_df)
    tab3.button("Save Ops Table")
    tab4.text("CoinGecko API")
    cg = CoinGeckoAPI()
    cg_category = cg.get_coins_categories()
    jsonRaw = json.dumps(cg_category)
    df = pd.read_json(jsonRaw)
    tab4.dataframe(df)
    
     
# def api():
#     left, center, right = st.columns([4,4,4])
#     cg = CoinGeckoAPI() 
#     btc = cg.get_price(ids='bitcoin', vs_currencies='usd', include_market_cap='true', include_24hr_vol='true', include_24hr_change='true', include_last_updated_at='true')
#     with left.container():
#         left.title("Coin Gecko API")
#         left.json(btc)
#         left.image("https://static.coingecko.com/s/coingecko-mascot-suit-b1a9df2b041094a017948f1d184f1aa263e779d4e1f22c437e835b74f0b00073.png",width=200)
#     with center.container():
#         center.title("PancakeSwap API")
#         apiURL = "https://api.pancakeswap.info/api/v2/tokens/"
#         coin_addy = center.selectbox("Invoice Currency Price",["0x2170Ed0880ac9A755fd29B2688956BD959F933F8", "0x7130d2A12B9BCbFAe4f2634d864A1Ee1Ce3Ead9c","0x8AC76a51cc950d9822D68b83fE1Ad97B32Cd580d"],index=0)
#         response = requests.get(url = apiURL + coin_addy)
#         pancake = response.json()
#         center.json(pancake)
#         center.image("https://www.pngall.com/wp-content/uploads/10/PancakeSwap-Crypto-Logo-PNG-Images.png",width=200)
#     lc = LunarCrush()
#     eth_1_year_data = lc.get_assets(symbol=['ETH'],data_points=365, interval='day')
#     with right.container():
#         right.title("LunarCrush API")
#         right.image("https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSwRhSbOtWFqO4IjI0vcb_gNsTK644-bdO3t_YkW_qq&s",width=200)
#         right.write(eth_1_year_data)

page_names_to_funcs = {
    "About ✏️": home_page,
    # "Meeting Effciency 📈":meetings,
    # "Sign In 🎲": signin,
    "Invoice 📋" : invoice,
    # "Clients": clients,
    # "Products": products,
    # "Opportunties": opportunities,
    # "API Feeds": api,
    "CRM 📪": backend,
    "AI Chat 💻": ai_chat,
    
}
selected_page = st.sidebar.radio("Navigation Panel", page_names_to_funcs.keys())
# Execute the selected page function
page_func = page_names_to_funcs[selected_page]
page_func()
