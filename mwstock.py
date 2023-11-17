import streamlit as st
import requests
from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime, timedelta
import plotly.express as px
import time

# Function to fetch and update data
def fetch_and_update_data():
    url = "https://mse.co.mw/market/mainboard"

    # Fetch the HTML content from the URL
    response = requests.get(url)
    html = response.text

    # Parse the HTML content
    soup = BeautifulSoup(html, 'html.parser')

    # Find the table with the specified class
    table = soup.find('table', class_='table')

    # Check if the table was found
    if table:
        # Extract data from the table
        data = []
        for row in table.find_all('tr')[1:-1]:  # Exclude the header and footer rows
            columns = row.find_all(['td', 'th'])
            symbol = columns[0].find('a').text.strip()
            open_price = columns[1].text.strip()
            close_price = columns[2].text.strip()
            percent_change = columns[3].text.strip()
            volume = columns[4].text.strip().replace(',', '')
            turnover = columns[5].text.strip().replace(',', '')

            data.append({
                'Symbol': symbol,
                'Open Price': open_price,
                'Close Price': close_price,
                'Percent Change': percent_change,
                'Volume': volume,
                'Turnover': turnover,
            })

        # Create a DataFrame
        new_data_df = pd.DataFrame(data)

        # Add a column for the collection date
        new_data_df['Date Collected'] = datetime.now()

        # Load existing DataFrame if it exists
        try:
            existing_df = pd.read_csv('existing_data.csv')
        except FileNotFoundError:
            existing_df = pd.DataFrame()

        # Append new data to existing DataFrame
        combined_df = pd.concat([existing_df, new_data_df], ignore_index=True)

        # Save the updated DataFrame to a CSV file
        combined_df.to_csv('existing_data.csv', index=False)

        return combined_df
    else:
        st.error("Table not found.")
        return None

# Streamlit app
st.set_page_config(
    page_title="Real-Time Malawi Stock Market Data Dashboard",
    page_icon="✅",
    layout="wide",
)

st.title("Malawi Stock Market Live Dashboard")

# Create a placeholder for the data
data_placeholder = st.empty()

# Automatically update and display the data every 5 minutes
while True:
    data_df = fetch_and_update_data()

    # Display the updated data in Streamlit
    if data_df is not None:
        # Convert 'Symbol' column to string to avoid TypeError during sorting
        data_df['Symbol'] = data_df['Symbol'].astype(str)

        # Get unique symbols for filtering
        unique_symbols = sorted(data_df['Symbol'].unique())

        # Create a new selectbox with a unique key in each iteration
        selected_symbol = st.selectbox("Select Symbol to Filter:", unique_symbols, key=f"symbol_selectbox_{time.time()}")

        # Use st.columns to create a layout with two columns
        col1, col2 = st.columns(2)

        # Filter data based on selected symbol and display in the left column
        with col1:
            filtered_data = data_df[data_df['Symbol'] == selected_symbol]
            st.dataframe(filtered_data.style.set_table_styles([{'selector': 'th', 'props': [('max-width', '100px')]}]))

        # Create a time series plot for the selected symbol in the right column
        with col2:
            fig = px.line(filtered_data, x='Date Collected', y='Open Price', title=f'Time Series Plot for {selected_symbol}')
            st.plotly_chart(fig)

    # Wait for 5 minutes before fetching data again
    time.sleep(300)  # 300 seconds = 5 minutes
