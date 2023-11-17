# Real-Time Malawi Stock Market Data Dashboard

This Python script provides a real-time dashboard for monitoring [Malawi Stock Market](https://mse.co.mw/market/mainboard) data using the Streamlit library. The dashboard automatically fetches and updates stock market data every 5 minutes, displaying a table and a time series plot for the selected stock symbol.

## Function to Fetch and Update Data
The fetch_and_update_data function is responsible for fetching the HTML content from the Malawi Stock Exchange (MSE) website, parsing it, and extracting relevant data from the specified table. The extracted data is then stored in a Pandas DataFrame, and the function updates an existing CSV file with the new data. The function returns the combined DataFrame, including both the existing and newly collected data.

## Streamlit App
The Streamlit app is configured to have a wide layout and a title indicating that it's a real-time dashboard for Malawi Stock Market data. The main functionality is within a while loop that continuously fetches and updates data every 5 minutes.

## Displaying Data in Streamlit
The data is displayed in Streamlit using columns and widgets. The left column shows a filtered table based on the selected stock symbol, and the right column displays a time series plot for the selected symbol.
