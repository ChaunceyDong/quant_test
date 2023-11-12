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
import sys
sys.path.append('/Users/chuanlin/Documents/GitHub/hft-playground')
from hft_play import plot_toolbox

# %%

df = quote_df.merge(trade_df, how='outer', left_index=True, right_index=True)
df.hplot(
    ['bid_price', 'ask_price', 'price'],
    output_name='px.html'
)

# %%
# check time diff

def cal_time_diff(df):
    """
    Calculate time difference between rows, also consider noon break
    """
    df = df.copy()
    df['time_diff'] = 0

    # morning trading
    trading_morning = (
        (df.index.time >= datetime.strptime('09:31:00', '%H:%M:%S').time()) 
        & (df.index.time <= datetime.strptime('12:00:00', '%H:%M:%S').time())
    )
    df.loc[trading_morning, 'time_diff'] = df[trading_morning].index.to_series().diff().dt.total_seconds()
    
    # afternoon
    trading_afternoon = (
        (df.index.time >= datetime.strptime('13:01:00', '%H:%M:%S').time()) 
        & (df.index.time <= datetime.strptime('16:00:00', '%H:%M:%S').time())
    )
    df.loc[trading_afternoon, 'time_diff'] = df[trading_afternoon].index.to_series().diff().dt.total_seconds()
    
    return df['time_diff']

quote_df['time_diff'] = cal_time_diff(quote_df)
quote_df.plotDistrib(
    'time_diff', bins=100,
)
print(quote_df['time_diff'].describe())
# %%
quote_df[quote_df['time_diff']>3]
# %%
trade_df['time_diff'] = cal_time_diff(trade_df)
trade_df.plotDistrib(
    'time_diff', bins=100,
)
print(trade_df['time_diff'].describe())

# %%
