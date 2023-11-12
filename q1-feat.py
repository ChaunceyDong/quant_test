# %%
import pandas as pd
from datetime import datetime

# Function to convert time strings to datetime objects
def convert_to_datetime(time_str):
    return datetime.strptime(time_str, "%H:%M:%S.%f")

# %%
# Load the data
trade_df = pd.read_csv('data/trade.csv')
quote_df = pd.read_csv('data/quote.csv')

# %%
# Convert time columns
trade_df['datetime'] = trade_df['time'].apply(convert_to_datetime)
quote_df['datetime'] = quote_df['time'].apply(convert_to_datetime)
trade_df.set_index('datetime', inplace=True)
quote_df.set_index('datetime', inplace=True)

# %%
# Aggregate trade data
def vwap(df):
    v = df['volume']
    p = df['price']
    return (v * p).sum() / v.sum()


def twap(df):
    return df['price'].mean()


trade_ohlcv = trade_df.resample('5T').agg({
    'price': ['first', 'max', 'min', 'last'],
    'volume': 'sum',
    'time': 'count'
})
trade_ohlcv.columns = ['open', 'high', 'low', 'close', 'volume', 'n_trd']
trade_vwap = trade_df.resample('5T').apply(vwap).rename('vwap')
trade_twap = trade_df.resample('5T').apply(twap).rename('twap')
trade_agg = pd.concat([trade_ohlcv, trade_vwap, trade_twap], axis=1)
# %%
# Aggregate quote data
quote_agg = quote_df.resample('5T').agg({
    'bid_price': 'last', 'ask_price': 'last',
    'bid_size': 'last', 'ask_size': 'last',
    'time': 'count'
}).rename(columns={'time': 'n_quo'})
# %%
# Calculate liquidity flow data

# Shift the quote dataframe by one period forward to get the previous quote
quote_shifted = quote_df.shift(1)

# Calculate liquidity metrics using the shifted data
# Liquidity addition is the increase in bid/ask size
liquidity_add_bid = (quote_df['bid_size'] - quote_shifted['bid_size']).clip(lower=0)
liquidity_add_ask = (quote_df['ask_size'] - quote_shifted['ask_size']).clip(lower=0)

# Liquidity taken is the decrease in bid/ask size
liquidity_taken_bid = (quote_shifted['bid_size'] - quote_df['bid_size']).clip(lower=0)
liquidity_taken_ask = (quote_shifted['ask_size'] - quote_df['ask_size']).clip(lower=0)

# Assigning liquidity metrics to the quote dataframe
quote_df['liquidity_add_bid'] = liquidity_add_bid
quote_df['liquidity_add_ask'] = liquidity_add_ask
quote_df['liquidity_taken_bid'] = liquidity_taken_bid
quote_df['liquidity_taken_ask'] = liquidity_taken_ask

# Aggregate liquidity metrics into the 5-minute bins
liquidity_agg = quote_df.resample('5T').agg({
    'liquidity_add_bid': 'sum',
    'liquidity_add_ask': 'sum',
    'liquidity_taken_bid': 'sum',
    'liquidity_taken_ask': 'sum'
})

# %%

# Combine all data
final_aggregated_data = pd.concat([trade_agg, quote_agg, liquidity_agg], axis=1)
final_aggregated_data.to_csv('output/aggregated_data.csv')
# %%
