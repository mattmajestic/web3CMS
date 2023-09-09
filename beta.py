import streamlit as st
from streamlit.components.v1 import iframe, html
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
import supabase
import os
import folium
from geopy.geocoders import Nominatim
import plotly.express as px
from streamlit import session_state
import random
import string
from streamlit_extras.switch_page_button import switch_page
import uvicorn
from fastapi import FastAPI
from pydantic import BaseModel
from urllib.parse import urlencode
import webbrowser

# Create a FastAPI app
app_fastapi = FastAPI()

# Define a data model
class Item(BaseModel):
    name: str
    description: str

# Define a route that returns JSON data
@app_fastapi.get("/api/data")
def get_data():
    data = {"name": "John Doe", "age": 30}
    return data

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


st.set_page_config(
     page_title="web3BMS",
     page_icon="🚀",
     layout="wide",
     initial_sidebar_state='expanded'
 )


# Define custom query parameters for each page
page_queries = {
    "home": "Home ✏️",
    "invoice": "Invoice 📋",
    "dev_docs": "Developer Docs 🚝",
    "backend": "CRM 📪",
    "ai_chat": "AI Chat 💻",
    "development_request": "Development Request ☎️"
}

# Get the current URL query parameters
query_params = st.experimental_get_query_params()

# Determine the selected page from the query parameters (default to "home")
selected_page = query_params.get("page", ["home"])[0]

# Create a sidebar navigation menu
selected_page = st.sidebar.radio("Navigation Panel", list(page_queries.values()), index=list(page_queries.keys()).index(selected_page))

# Set the query parameter to the selected page
selected_page_key = next(key for key, value in page_queries.items() if value == selected_page)
st.experimental_set_query_params(page=selected_page_key)

def home_page():
    page_names = ["home", "invoice", "dev_docs", "backend", "ai_chat"]
    page_labels = ["🏠 Home", "📋 Invoice", "🚝 Developer Docs", "📪 CRM", "💻 AI Chat"]
    columns = st.columns([2,2,3,2,2])
    for name, label, column in zip(page_names, page_labels, columns):
        url = f"https://web3bms.streamlit.app/?page={name}"
        button_html = f'<a href="{url}" target="_self"><button style="background-color: black; color: white;">{label}</button></a>'
        column.markdown(button_html, unsafe_allow_html=True)

    st.markdown("""
    <script src="https://cdn.jsdelivr.net/npm/mermaid/dist/mermaid.min.js"></script>
    <script>mermaid.initialize({startOnLoad:true});</script>
    """, unsafe_allow_html=True)
    st.markdown(readme_text, unsafe_allow_html=True)
    st.toast(f'Welcome to web3bms', icon='✅')

def api_endpoint():
    json_data = {
        "name": "John Doe",
        "age": 30,
        "email": "johndoe@example.com"
    }
    st.json(json_data)

def invoice():
    products_db = supabase_client.table('products').select("*").execute()
    products_df = pd.DataFrame(products_db.data)
    contacts_db = supabase_client.table('contacts').select("*").execute()
    contacts_df = pd.DataFrame(contacts_db.data)
    opportunities_db = supabase_client.table('opportunities').select("*").execute()
    opportunities_df = pd.DataFrame(opportunities_db.data)
    
    cg_html = '''
    <script src="https://widgets.coingecko.com/coingecko-coin-list-widget.js"></script><coingecko-coin-list-widget  coin-ids="bitcoin,ethereum" currency="usd" locale="en"></coingecko-coin-list-widget>
    '''

    cg_marquee = '''
    <script src="https://widgets.coingecko.com/coingecko-coin-price-marquee-widget.js"></script><coingecko-coin-price-marquee-widget  coin-ids="bitcoin,ethereum,eos,ripple,litecoin" currency="usd" background-color="#100f0f" locale="en" font-color="#fefbfb"></coingecko-coin-price-marquee-widget>
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
    coin_type = form.radio("Select Cryptocurrency Payment", ["No Crypto", "BTC", "ETH"], index=0,horizontal=True)
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

    meetings_expander = right.expander("🤝 Meetings")
    with meetings_expander:
        st.write("Calculate Meeting Costs")
        weekly_meeting_hours = st.number_input("Weekly Meeting Hours", min_value=0, value=10)
        annual_salary = st.number_input("Annual Salary ($)", min_value=0, value=50000)
        hourly_rate = annual_salary / (52 * weekly_meeting_hours) if weekly_meeting_hours > 0 else 0
        st.write(f"Hourly Rate: ${hourly_rate:.2f}")

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
    btc_expander = right.expander("💸 Donate BTC ")
    with btc_expander:
        url = "https://mainnet.demo.btcpayserver.org/api/v1/invoices?storeId=4r8DKKKMkxGPVKcW9TXB2eta7PTVzzs192TWM3KuY52e&price=100&currency=USD&defaultPaymentMethod=BTC"
        link = 'Pay with BTC [via this link](https://mainnet.demo.btcpayserver.org/api/v1/invoices?storeId=4r8DKKKMkxGPVKcW9TXB2eta7PTVzzs192TWM3KuY52e&price=100&currency=USD&defaultPaymentMethod=BTC)'
        st.markdown(link, unsafe_allow_html=True)
        components.iframe(url, width=300, height=500, scrolling=True)

    components.html(cg_marquee)
    st.toast(f'Invoice crypto!', icon='✅')

def ai_chat():
    st.title("GPT chat with your Business Data")
    st.write("Submit Prompt Below")
    prompt = st.chat_input("Chat your Business with AI")
    
    if prompt:
        st.write(f"User has sent the following prompt: {prompt}")
        response = supabase_client.table("ai-chat").insert([{"prompt": prompt, "created_at": datetime.now().isoformat()}]).execute()
        st.toast('Stored Prompt', icon='✅')
    # Show the BTC Pay Server
    prompt_expander = st.expander("📝 Show Previous Prompts")
    with prompt_expander:
        ai_chat_db = supabase_client.table('ai-chat').select("*").execute()
        ai_chat_df = pd.DataFrame(ai_chat_db.data)
        st.write("Previous Prompts:")
        st.write(ai_chat_df)
    st.toast(f'Ask Away', icon='✅')


def backend():
    # Replace with supabase fetch
    products_db = supabase_client.table('products').select("*").execute()
    products_df = pd.DataFrame(products_db.data)
    contacts_db = supabase_client.table('contacts').select("*").execute()
    contacts_df = pd.DataFrame(contacts_db.data)
    opportunities_db = supabase_client.table('opportunities').select("*").execute()
    opportunities_df = pd.DataFrame(opportunities_db.data)
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


def dev_docs():
    st.title("Development Documentation 🚝")
    st.write("")
    left, center, right = st.columns([4,4,4])
    st.write("")
    left.write("API Documentation 📪")
    left_expander = left.expander("CRM API Endpoint", expanded=False)
    with left_expander:
        st.write("📊 Description: The API allows you to manage customer relationship data.")
        st.write("🚀 Endpoint: `/api/crm`")
        st.write("📝 Method: GET")
        st.write("🔑 Parameters:")
        st.write("- `customer_id`: The ID of the customer.")
        st.write("- `name`: The name of the customer.")
        st.write("- `email`: The email address of the customer.")
        st.write("")
        st.write("")
        st.code("curl https://web3bms.io/api/crm", language="python")
        if left_expander:
            st.toast('Try it out with CURL', icon='📪')

    key_expander = left.expander("Create API Key 🔑", expanded=False)
    with key_expander:
        st.write("Enter your email address below to generate an API key:")
        email = st.text_input("Email Address")
        if st.button("Generate API Key"):
            if email:
                api_key = ''.join(random.choices(string.ascii_letters + string.digits, k=32))
                response = supabase_client.table("web3bms-api-keys").insert([{"email": email, "api_key": api_key}]).execute()
                st.write("Your API key has been generated and saved to the database.")
                st.toast('API Key Stored', icon='🔑')
                

    center.write("CLI Commands 🔍")
    cli_expander = center.expander("CRM CLI Command", expanded=False)
    with cli_expander:
        st.write("🔧 Description: The CLI command allows you to interact with customer data.")
        st.write("🛠️ Options:")
        st.write("- `--option1`: Description of option 1.")
        st.write("- `--option2`: Description of option 2.")
        st.write("")
        st.write("")
        st.code("web3bms crm list-clients", language="bash")
        st.toast('Try it out in Bash', icon='🔍')

    right.write("PyPI Package 🐍")
    pypi_expander = right.expander("CRM Python Functions", expanded=False)
    with pypi_expander:
        st.write("The web3bms package is available on PyPI and can be installed using pip:")
        st.code("pip install web3bms", language="bash")
        st.write("")
        st.write("Once installed, you can import and use the package in your Python scripts.")
        st.code("from web3bms import crm", language="python")
        st.toast('Try it out in Python', icon='🐍')

def development_request():
    st.title("Development Service Request Form 🚀")

    # User information
    user_name = st.text_input("Your Name 👤")
    user_email = st.text_input("Your Email 📧")

    # GitHub information
    github_username = st.text_input("GitHub Username 🐱")
    github_repo = st.text_input("GitHub Repository 📂")

    # Request description
    request_description = st.text_area("Describe Your Request 📝")

    # Service options
    selected_service = st.radio("Select Service 💼", ["Code Review ($100)", "Code Writing ($300)", "Full PR Request ($500)"])

    # Additional options
    include_test = st.checkbox("Include Test 🧪")
    include_documentation = st.checkbox("Include Documentation 📄")

    # Submit button
    if st.button("Submit Request 🚀"):
        # Process the user's request
        st.success("Request submitted successfully! 🎉")

        # Calculate the total price based on the selected service and options
        total_price = 0
        if "Code Review" in selected_service:
            total_price += 100
        if "Code Writing" in selected_service:
            total_price += 300
        if "Full PR Request" in selected_service:
            total_price += 500

        # Add additional costs for test and documentation
        if include_test:
            total_price += 50  # Adjust the price as needed
        if include_documentation:
            total_price += 50  # Adjust the price as needed

        # Display the total price to the user
        st.write(f"Total Price: ${total_price} 💰")

        # Store data in Supabase table
        insert_data = [
            {
                "user_name": user_name,
                "user_email": user_email,
                "github_username": github_username,
                "github_repo": github_repo,
                "request_description": request_description,
                "selected_service": selected_service,
                "include_test": include_test,
                "include_documentation": include_documentation,
                "total_price": total_price,
            }
        ]

        # Insert data into Supabase table
        response, error = supabase_client.table("service_requests").upsert(insert_data, returning="minimal")

        if error:
            st.error("Error storing data in Supabase. ❌")
        else:
            st.success("Data stored in Supabase successfully! 🎉")

    # Reset button
    if st.button("Reset Form 🔄"):
        st.text_input("Your Name 👤", value="")
        st.text_input("Your Email 📧", value="")
        st.text_input("GitHub Username 🐱", value="")
        st.text_input("GitHub Repository 📂", value="")
        st.text_area("Describe Your Request 📝", value="")
        st.checkbox("Include Test 🧪", value=False)
        st.checkbox("Include Documentation 📄", value=False)


# Map selected page to corresponding function
page_funcs = {
    "home": home_page,
    "invoice": invoice,
    "dev_docs": dev_docs,
    "backend": backend,
    "ai_chat": ai_chat,
    "development_request": development_request
}

# Execute the selected page function
page_func = page_funcs[selected_page_key]
page_func()