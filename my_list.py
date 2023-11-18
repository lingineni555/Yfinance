
import yfinance as yf
import pandas as pd
from datetime import datetime, timedelta

# Define a list of stock symbols
stock_symbols = ["AAPL", "MSFT", "GOOGL", "TSLA","NIO","BABA","AMZN","ADBE","NVDA","JPM"]  # Add more stock symbols as needed

# Create an empty DataFrame to store the data
data = pd.DataFrame(columns=["current_date","stock_name", "current_value", "12m_back_close","12m_back_date","6m_back_close","6m_back_date",
                             "1m_back_close","1m_back_date","1wk_back_close","1wk_back_date",
                             "insiders_stocks%", "institutions_stocks%","num_of_inst"])

def adjust_to_friday(date_obj):
        # Adjust the date if it's a Saturday or Sunday
          if date_obj.weekday() == 5:  # Saturday
              return date_obj - timedelta(days=1)
          elif date_obj.weekday() == 6:  # Sunday
              return date_obj - timedelta(days=2)
          else:
              return date_obj

# Loop through each stock symbol
for symbol in stock_symbols:
    try:
        # Create a Ticker object for the stock
        stock = yf.Ticker(symbol)

        # Get historical data of last 15 months
        historical_data = stock.history(period="15mo")  # Adjust the period as needed
        historical_data = historical_data.reset_index()

        
        # Calculate the Current values

        current_value = round(historical_data.iloc[-1]["Close"],2) #Most recent value
        current_date = historical_data.iloc[-1]["Date"].date() #Most recent value
        

        # Calculate the date 1 Week back
        onewk_back = current_date - relativedelta(days=7)
        # Adjust if it's a weekend
        onewk_back = adjust_to_friday(onewk_back)
        
        # Calculate the date 1 month back
        onemo_back = current_date - relativedelta(months=1)
        # Adjust if it's a weekend
        onemo_back = adjust_to_friday(onemo_back)

        # Calculate the date 6 months back
        sixmo_back = current_date - relativedelta(months=6)
        # Adjust if it's a weekend
        sixmo_back = adjust_to_friday(sixmo_back)
        
        # Calculate the date 12 months back
        oneyear_back = current_date - relativedelta(months=12)
        # Adjust if it's a weekend
        oneyear_back = adjust_to_friday(oneyear_back)

        # Convert the Date column to just date for comparison
        historical_data['Date'] = historical_data['Date'].dt.date

        # Filter the DataFrame where the Date is equal to required dates 
        one_year_back_close = round(historical_data[historical_data.Date == oneyear_back].iloc[0]["Close"],2)
        one_year_back_date = oneyear_back
        six_months_back_close = round(historical_data[historical_data.Date == sixmo_back].iloc[0]["Close"],2)
        six_month_back_date = sixmo_back
        one_month_back_close = round(historical_data[historical_data.Date == onemo_back].iloc[0]["Close"],2)  # Approx. 1 month data
        one_month_back_date = onemo_back
        one_wk_back_close = round(historical_data[historical_data.Date == onewk_back].iloc[0]["Close"],2)  # Approx. 1 month data
        one_wk_back_date = onewk_back


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
            "current_date": current_date,
            "stock_name": symbol,
            "current_value": current_value, 
            "12m_back_close": one_year_back_close,
            "6m_back_close": six_months_back_close,
            "1m_back_close": one_month_back_close,
            "1wk_back_close": one_wk_back_close,
            "insiders_stocks%": insider ,  
            "institutions_stocks%": institutions,  
            "num_of_inst": num_of_inst,
            "12m_back_date": one_year_back_date,
            "6m_back_date": six_month_back_date,
            "1m_back_date": one_month_back_date,
            "1wk_back_date": one_wk_back_date
        }, ignore_index=True)

    except Exception as e:
        print(f"Error fetching data for {symbol}: {str(e)}")

# Calculate the percentage change and save it as a percentage
data['12m%_change'] = ((data['current_value'] - data['12m_back_close']) / data['12m_back_close']) * 100
# Add '%' symbol to the values in the '6months % change' column
data['12m%_change'] = data['12m%_change'].map('{:.2f}%'.format)

# Calculate the percentage change and save it as a percentage
data['6m%_change'] = ((data['current_value'] - data['6m_back_close']) / data['6m_back_close']) * 100
# Add '%' symbol to the values in the '6months % change' column
data['6m%_change'] = data['6m%_change'].map('{:.2f}%'.format)

# Calculate the percentage change and save it as a percentage
data['1m%_change'] = ((data['current_value'] - data['1m_back_close']) / data['1m_back_close']) * 100
# Add '%' symbol to the values in the '6months % change' column
data['1m%_change'] = data['1m%_change'].map('{:.2f}%'.format)

# Calculate the percentage change and save it as a percentage
data['1wk%_change'] = ((data['current_value'] - data['1wk_back_close']) / data['1wk_back_close']) * 100
# Add '%' symbol to the values in the '6months % change' column
data['1wk%_change'] = data['1wk%_change'].map('{:.2f}%'.format)

data = data[['current_date', 'stock_name', 'current_value', '1wk%_change','1m%_change', '6m%_change','12m%_change','12m_back_close',
       '6m_back_close',  '1m_back_close'
       ,'insiders_stocks%', 'institutions_stocks%',
       'num_of_inst','12m_back_date','6m_back_date','1m_back_date','1wk_back_date']]

# Print the populated DataFrame
data.style.set_table_styles(
    [{'selector': 'th', 'props': [('background-color', '#f4f4f4'), ('color', 'black')]}]
).set_properties(**{'background-color': 'white', 'color': 'black', 'border-color': 'black'})

# Save the DataFrame to a CSV file
#data.to_csv("stock2.csv")
