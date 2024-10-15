import mysql.connector
import pandas as pd
import streamlit as st

# Add logo in the sidebar
image_path = r"C:\Users\lejoc\OneDrive\Desktop\PROJECTS\REDBUS\redBus-Logo-Vector.svg-.png"
st.sidebar.image(image_path, caption="redBus Logo", use_column_width=True)

st.sidebar.header("Skills Learned")


st.sidebar.markdown("""
- Web Scraping using Selenium
- Data Analysis with Python
- Building Interactive Apps with Streamlit
- Database Management with SQL
""")


# Function to connect to the database and fetch data
def get_data_from_db():
    try:
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
    except Exception as e:
        st.error(f"Error connecting to the database: {e}")
        return pd.DataFrame()  # Return empty DataFrame on error

# Main app header
st.markdown("<h1 style='color:red;'>Redbus Data Scraping with Selenium & Dynamic Filtering using Streamlit</h1>", unsafe_allow_html=True)
st.markdown("---")  # This creates a horizontal line


# Fetch data from the database
data = get_data_from_db()

# Check if data is loaded
if data.empty:
    st.write("No data available from the database.")
else:
    st.write("Data loaded successfully. Here are the first few rows:")
    st.dataframe(data.head())  # Display the first few rows for verification

    # Convert RATINGS column to numeric
    data["RATINGS"] = pd.to_numeric(data["RATINGS"], errors='coerce')

    # Dropdown to select a state
    selected_state = st.selectbox("Select the desired state from the dropdown", data["STATE"].unique())
    filtered_data = data[data["STATE"] == selected_state]

    # Check state filtering
    if filtered_data.empty:
        st.write("No buses available for the selected state.")
    else:
        st.write(f"Filtered by state: {selected_state}, found {len(filtered_data)} buses.")

        # Dropdown for general bus type selection
        general_bus_type = st.selectbox("Select General Bus Type", ['AC', 'Non AC'])
        filtered_data = filtered_data[filtered_data["BUS_TYPE"].str.contains(general_bus_type)]

        # Check bus type filtering
        if filtered_data.empty:
            st.write("No buses available for the selected bus type.")
        else:
            st.write(f"Filtered by bus type: {general_bus_type}, found {len(filtered_data)} buses.")

            # Get unique detailed bus types based on the general bus type
            detailed_bus_types = filtered_data["BUS_TYPE"].unique()
            selected_detailed_bus_types = st.multiselect("Select Detailed Bus Types", detailed_bus_types)

            # Apply detailed bus type filter
            if selected_detailed_bus_types:
                filtered_data = filtered_data[filtered_data["BUS_TYPE"].isin(selected_detailed_bus_types)]
                if filtered_data.empty:
                    st.write("No buses available for the selected detailed bus types.")
                else:
                    st.write(f"Filtered by detailed bus types, found {len(filtered_data)} buses.")

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

            # Apply price range filter
            if selected_price_ranges:
                price_filter = False
                for min_price, max_price in selected_price_ranges:
                    price_filter |= (filtered_data["PRICE"].between(min_price, max_price))
                filtered_data = filtered_data[price_filter]

            # Check price filtering
            if filtered_data.empty:
                st.write("No buses available for the selected price ranges.")
            else:
                st.write(f"After price filtering, found {len(filtered_data)} buses.")

            # Sidebar for ratings selection using a slider
            st.subheader("Select Ratings")
            min_rating, max_rating = st.slider("Choose Rating Range", 0.0, 5.0, (0.0, 5.0))

            # Display selected rating values above the slider
            st.write(f"Selected Rating Range: {min_rating:.1f} to {max_rating:.1f}")

            # Apply rating filter
            filtered_data = filtered_data[(filtered_data["RATINGS"] >= min_rating) & (filtered_data["RATINGS"] <= max_rating)]

            # Display filtered bus details
            st.subheader("Filtered Bus Details")
            if not filtered_data.empty:
                st.dataframe(filtered_data[['ROUTE_NAME', 'BUS_NAME', 'BUS_TYPE', 'PRICE', 'START_TIME', 'END_TIME', 'DURATION', 'RATINGS']])
            else:
                st.write("No buses available for the selected ratings.")
