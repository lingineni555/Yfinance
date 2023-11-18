
# Code to retrive data from Yfinance API

import yfinance as yf
import pandas as pd

# Define a list of stock symbols
stock_symbols = ["AAPL", "MSFT", "GOOGL", "TSLA","NIO","BABA","AMZN","ADBE","NVDA","JPM"]  # Add more stock symbols as needed

# Create an empty DataFrame to store the data
data = pd.DataFrame(columns=["Current Date","Stock Name", "Current Value", "Six Months Back Close","six_months_back_date",
                             "One Month Back Close","one_month_back_date",
                             "% of Stocks Held by Insiders", "% of Stocks Held by Institutions","No of institutions holding shares"])

# Loop through each stock symbol
for symbol in stock_symbols:
    try:
        # Create a Ticker object for the stock
        stock = yf.Ticker(symbol)

        # Get historical data
        historical_data = stock.history(period="12mo")  # Adjust the period as needed
        historical_data = historical_data.reset_index()

        # Calculate the required values
        current_value = historical_data.iloc[-1]["Close"]
        current_date = historical_data.iloc[-1]["Date"]
        six_months_back_close = historical_data.iloc[0]["Close"]
        six_months_back_date = historical_data.iloc[0]["Date"]
        one_month_back_close = historical_data.iloc[-20]["Close"]  # Approx. 1 month data
        one_month_back_date = historical_data.iloc[-20]["Date"]
        # Add logic to calculate short %, % of insiders, and % of institutions if available

        # Get holders data
        holders = stock.major_holders
        holders = holders.reset_index(drop=True)
        new_df = pd.DataFrame(columns=holders[1])
        new_df.loc[0] = holders[0].values
        new_df = new_df.reset_index(drop=True)
        insider = new_df["% of Shares Held by All Insider"].iloc[0]
        institutions = new_df["% of Shares Held by Institutions"].iloc[0]
        num_of_inst = new_df["Number of Institutions Holding Shares"].iloc[0]



        # Add the data to the DataFrame
        data = data.append({
            "Current Date": current_date,
            "Stock Name": symbol,
            "Current Value": current_value,
            "Six Months Back Close": six_months_back_close,
            "six_months_back_date": six_months_back_date,
            "One Month Back Close": one_month_back_close,
            "one_month_back_date": one_month_back_date,
            "% of Stocks Held by Insiders": insider ,
            "% of Stocks Held by Institutions": institutions,
            "No of institutions holding shares": num_of_inst
        }, ignore_index=True)

    except Exception as e:
        print(f"Error fetching data for {symbol}: {str(e)}")

# Calculate the percentage change and save it as a percentage
data['6months % change'] = ((data['Current Value'] - data['Six Months Back Close']) / data['Six Months Back Close']) * 100

# Add '%' symbol to the values in the '6months % change' column
data['6months % change'] = data['6months % change'].map('{:.2f}%'.format)

# Calculate the percentage change and save it as a percentage
data['1months % change'] = ((data['Current Value'] - data['One Month Back Close']) / data['One Month Back Close']) * 100

# Add '%' symbol to the values in the '6months % change' column
data['1months % change'] = data['1months % change'].map('{:.2f}%'.format)

# Print the populated DataFrame
print(data)

# Save the DataFrame to a CSV file
# data.to_csv("stock1.csv")
