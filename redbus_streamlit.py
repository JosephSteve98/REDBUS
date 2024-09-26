import mysql.connector
import pandas as pd
import streamlit as st
import os


# Add an image to the sidebar
image_path = r"C:\Users\lejoc\OneDrive\Desktop\REDBUS\redBus-Logo-Vector.svg-.png"
st.sidebar.image(image_path, caption="redBus Logo", use_column_width=True)


# Function to connect to the database and fetch data
def get_data_from_db():
    connection = mysql.connector.connect(   
        host="localhost",
        database="Redbus_information",
        user="root",
        password="1234",
        port="3306"
    )
    query = "SELECT * FROM REDBUS_TABLE"
    data = pd.read_sql(query, connection)
    connection.close()
    return data

# Sidebar for skills
st.sidebar.header("Skills Learned")
skills = [
    "Web Scraping using Selenium",
    "Data Analysis with Python",
    "Building Interactive Apps with Streamlit",
    "Database Management with SQL"
]
st.sidebar.write("\n".join(skills))

# Main app header
st.header("Redbus Data Scraping with Selenium & Dynamic Filtering using Streamlit", divider="gray")
st.subheader("Red Bus Information")

# Fetch data from the database
data = get_data_from_db()

# Dropdown to select a state
selected_state = st.selectbox("Select the desired state from the dropdown", data["STATE"].unique())

# Filter the DataFrame based on the selected state
filtered_data = data[data["STATE"] == selected_state]

# Multi-select for bus types
bus_type = st.multiselect("Select Bus Types", filtered_data["BUS_TYPE"].unique())

# Checkbox options for price ranges
st.subheader("Select Price Ranges")
price_ranges = {
    "Below 500": (0, 500),
    "501 to 1000": (501, 1000),
    "1001 to 1500": (1001, 1500),
    "1501 to 2000": (1501, 2000),
    "Above 2000": (2001, float('inf'))
}

selected_price_ranges = []
for price_range, (min_price, max_price) in price_ranges.items():
    if st.checkbox(price_range):
        selected_price_ranges.append((min_price, max_price))

# Apply bus type filter
if bus_type:
    filtered_data = filtered_data[filtered_data["BUS_TYPE"].isin(bus_type)]

# Apply price range filter
if selected_price_ranges:
    price_filter = False
    for min_price, max_price in selected_price_ranges:
        price_filter |= (filtered_data["PRICE"].between(min_price, max_price))
    filtered_data = filtered_data[price_filter]

# Display filtered bus details
st.subheader("Filtered Bus Details")
if not filtered_data.empty:
    st.dataframe(filtered_data[['ROUTE_NAME', 'BUS_NAME', 'BUS_TYPE', 'PRICE', 'START_TIME', 'END_TIME', 'DURATION']])
else:
    st.write("No buses available for the selected criteria.")
