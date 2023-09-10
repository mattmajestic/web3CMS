import streamlit as st
from streamlit.components.v1 import iframe, html
import streamlit.components.v1 as components
from streamlit_javascript import st_javascript
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
from urllib.parse import urlencode
import webbrowser
import torch
from transformers import pipeline, AutoModelForCausalLM, AutoTokenizer, set_seed
from sklearn.datasets import load_iris
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor
from sklearn.neural_network import MLPRegressor
import matplotlib.pyplot as plt
import seaborn as sns

st.set_page_config(
     page_title="web3BMS",
     page_icon="🐧",
     layout="wide",
     initial_sidebar_state='expanded'
 )

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

# Define custom query parameters for each page
page_queries = {
    "home": "Home 🐧",
    "invoice": "Invoice 📋",
    "crm": "CRM 📪",
    "ai_chat": "AI Chat 💻",
    "developer_docs": "Developer Docs 🚝",
    "developer_request": "Developer Request ☎️",
    "ml_ops": "ML Ops 👾"
}

# Get the current URL query parameters
query_params = st.experimental_get_query_params()

# Determine the selected page from the query parameters (default to "home")
selected_page = query_params.get("page", ["home"])[0]

# Create a sidebar navigation menu
selected_page = st.sidebar.radio("Navigate web3bms", list(page_queries.values()), index=list(page_queries.keys()).index(selected_page))

# Set the query parameter to the selected page
selected_page_key = next(key for key, value in page_queries.items() if value == selected_page)
st.experimental_set_query_params(page=selected_page_key)

page_names = ["home", "invoice", "developer_docs", "backend", "ai_chat", "developer_request", "ml_ops"]
page_labels = ["🏠 Home", "📋 Invoice", "🚝 Developer Docs", "📪 CRM", "💻 AI Chat", "☎️ Developer Request", "👾 ML Ops"]

# Define URLs for the pages
page_urls = {
    "🏠 Home": "https://web3bms.streamlit.app/?page=home",
    "📋 Invoice": "https://web3bms.streamlit.app/?page=invoice",
    "📪 CRM": "https://web3bms.streamlit.app/?page=crm",
    "💻 AI Chat": "https://web3bms.streamlit.app/?page=ai_chat",
    "🚝 Developer Docs": "https://web3bms.streamlit.app/?page=developer_docs",
    "☎️ Developer Request": "https://web3bms.streamlit.app/?page=developer_request",
    "👾 ML Ops": "https://web3bms.streamlit.app/?page=ml_ops"
}

button_style = 'background-color: #262730; color: white; padding: 10px 20px; border: none; border-radius: 5px; cursor: pointer; margin-right: 10px;'


def home_page():

    # columns = st.columns([2, 2, 3, 2, 2, 4, 2])

    # # Loop through page names and labels to create buttons
    # for name, label, column in zip(page_names, page_labels, columns):
    #     url = page_urls.get(label, "")
    #     if url:
    #         button_html = f'<button style="{button_style}" onclick="window.location.href=\'{url}\';">{selection}</button>'
    #         column.markdown(button_html, unsafe_allow_html=True)

    st.markdown("""
    <script src="https://cdn.jsdelivr.net/npm/mermaid/dist/mermaid.min.js"></script>
    <script>mermaid.initialize({startOnLoad:true});</script>
    """, unsafe_allow_html=True)
    st.markdown(readme_text, unsafe_allow_html=True)
    st.toast(f'Welcome to web3bms', icon='✅')

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
    with st.spinner("Generating Bot Response..."):
        if prompt:
            model_name = "gpt2"  
            model = AutoModelForCausalLM.from_pretrained(model_name)
            tokenizer = AutoTokenizer.from_pretrained(model_name)
            def generate_response(prompt):
                input_ids = tokenizer.encode(prompt, return_tensors="pt")
                response_ids = model.generate(input_ids, max_length=100, num_return_sequences=1)
                bot_response = tokenizer.decode(response_ids[0], skip_special_tokens=True)
                return bot_response
            bot_response = generate_response(prompt)
            st.write(f"User has sent the following prompt: {prompt}")
            st.write("Bot:", bot_response)
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


def crm():

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


def developer_docs():

    st.title("Software Development Documentation 🚝")
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

def developer_request():

    st.title("Software Development Request 🚀")

    # Create two columns for layout
    left_column,center_column, right_column = st.columns([6,2, 4])

    with left_column:
        st.subheader("User Information👤")
        user_email = st.text_input("Your Email 📧")
        st.subheader("GitHub Information")
        github_inputs = st.columns([5, 5])
        github_username = github_inputs[0].text_input("GitHub Username 🐱")
        github_repo = github_inputs[1].text_input("GitHub Repository 📂")
        st.subheader("Request Description")
        request_description = st.text_area("Describe Your Request 📝")

    # Right column for cost calculation and payment
    with right_column:
        st.subheader("Service Options")
        selected_service = st.radio("Select Service 💼", ["Code Review ($100)", "Code Writing ($300)", "Full PR Request ($500)"])

        include_test = st.checkbox("Include Test 🧪")
        include_documentation = st.checkbox("Include Documentation 📄")

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

        st.subheader("Total Price")
        st.write(f"${total_price} 💰")

        if st.button("Pay with Stripe Checkout"):
            st.success("Payment successful! 🎉")
        # Submit button for storing the request in Supabase
        if st.button("Submit Request"):
            response = supabase_client.table("development-request").insert([{
                "user_email": user_email,
                "github_username": github_username,
                "github_repo": github_repo,
                "request_description": request_description,
                "selected_service": selected_service,
                "include_test": include_test,
                "include_documentation": include_documentation,
                "total_price": total_price,
                "created_at": datetime.now().isoformat()
            }]).execute()
            st.toast('Request Stored Successfully', icon='✅')

def ml_ops():
    st.title("ML Ops - Model Deployment 👾")
    st.toast('GUI for Machine Learning', icon='👾')

    with st.expander("Overview of ML Ops 🍰", expanded=True):
        st.write("ML Ops (Machine Learning Operations) is a set of practices and tools designed to automate and streamline the deployment and management of machine learning models.")
        st.write("The purpose of ML Ops is to enable small and medium-sized businesses (SMBs) to leverage machine learning for various tasks, such as predicting customer behavior, optimizing operations, and making data-driven decisions.")

    with st.expander("Step 1: Select Data 📊"):
        st.subheader("Select Data Source")
        data_option = st.selectbox("Data Source", ["Iris Dataset", "Local CSV", "Database", "API"])

        if data_option == "Iris Dataset":
            st.subheader("Iris Dataset (Sample)")
            iris = load_iris()
            data = pd.DataFrame(iris.data, columns=iris.feature_names)
            st.write(data.head())

        elif data_option == "Local CSV":
            uploaded_file = st.file_uploader("Upload CSV File")
            if uploaded_file:
                # Handle the uploaded CSV file.
                st.success("CSV File Uploaded and Processed!")

        elif data_option == "Database":
            # Input fields to connect to a database.
            db_host = st.text_input("Database Host")
            db_username = st.text_input("Database Username")
            db_password = st.text_input("Database Password", type="password")

        elif data_option == "API":
            # Input fields to specify an API endpoint.
            api_url = st.text_input("API URL")

    with st.expander("Step 2: Data Options 🛠️"):
        st.subheader("Select Third-Party Datasets")

    with st.expander("Step 3: Select Model 🤖"):
        st.subheader("Select Model Type")
        model_option = st.selectbox("Model Type", ["Linear Regression", "Random Forest", "Neural Network"])
        st.toast('Select Model', icon='👾')

        if model_option == "Linear Regression":
            st.subheader("Linear Regression Options")
            learning_rate = st.slider("Learning Rate", 0.01, 1.0, 0.1)

            # Train the model on Iris data
            iris = load_iris()
            model = LinearRegression()
            model.fit(iris.data, iris.target)

            # Display model information
            st.subheader("Linear Regression Model")
            st.write("Coefficient:", model.coef_)
            st.write("Intercept:", model.intercept_)

            # Visualization: Regression Coefficients
            st.subheader("Regression Coefficients")
            fig, ax = plt.subplots(figsize=(8, 4))
            sns.barplot(x=iris.feature_names, y=model.coef_, ax=ax)
            ax.set_title("Regression Coefficients")
            ax.set_ylabel("Coefficient Value")
            ax.set_xlabel("Feature Name")
            st.pyplot(fig)

        elif model_option == "Random Forest":
            st.subheader("Random Forest Options")
            num_estimators = st.slider("Number of Estimators", 1, 100, 10)

            # Train the model on Iris data
            iris = load_iris()
            model = RandomForestRegressor(n_estimators=num_estimators)
            model.fit(iris.data, iris.target)

            # Display model information
            st.subheader("Random Forest Model")
            st.write("Feature Importance:", model.feature_importances_)

            # Visualization: Feature Importance
            st.subheader("Feature Importance")
            fig, ax = plt.subplots(figsize=(8, 4))
            sns.barplot(x=iris.feature_names, y=model.feature_importances_, ax=ax)
            ax.set_title("Feature Importance")
            ax.set_ylabel("Importance Value")
            ax.set_xlabel("Feature Name")
            st.pyplot(fig)

        elif model_option == "Neural Network":
            st.subheader("Neural Network Options")
            num_hidden_layers = st.slider("Number of Hidden Layers", 1, 5, 2)

            # Train the model on Iris data
            iris = load_iris()
            model = MLPRegressor(hidden_layer_sizes=(num_hidden_layers,))
            model.fit(iris.data, iris.target)

            # Display model information
            st.subheader("Neural Network Model")
            st.write("Number of Hidden Layers:", num_hidden_layers)

    
    with st.expander("Step 4: Save Model Parameters 💾"):
        st.toast('Save Your Model', icon='👾')
        if st.button("Save Model Parameters"):
            response = supabase_client.table("ml-ops").insert([{
                "data_option": data_option,
                "model_option": model_option,
                "created_at": datetime.now().isoformat()
            }]).execute()
            st.success("Model Parameters Saved!")

# Map selected page to corresponding function
page_funcs = {
    "home": home_page,
    "invoice": invoice,
    "crm": crm,
    "ai_chat": ai_chat,
    "developer_docs": developer_docs,
    "developer_request": developer_request,
    "ml_ops": ml_ops
}

# Execute the selected page function
page_func = page_funcs[selected_page_key]
page_func()
