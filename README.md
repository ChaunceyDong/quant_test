# quant test

## 1. Equity Tick Data

for this question, I split into 2 parts: check data quality and aggregate data

### check data quality

> see [q1-check_data.ipynb](q1-check_data.ipynb)

In this notebook. I merged quote and trades, and found out spikes inside the trade price.
Also checked the time diff of quote&trade updates, to check if any missing data.

### add feats
> see [q1-feat.ipynb](q1-feat.ipynb)

In this one, I calculated some features and aggregate them into 5 mins bar.
- general twap, vwap, ohlc, etc
- bbo add and taken(order cancel and trade)
- active buy and sell

for performance, when cal trade direction, I used matrix operation to calculate the features by numpy.where rather than forloop calculation.


## 3. US Treasury Auction

### Code Structure

- `TreasuryDataScraper` from [scraper.py](scraper.py) is the main class to scrape data from website
- `TreasuryDatabaseManager` from [database.py](database.py) is the main class to manage database

### Workflow

can check `daily_example()` from [q3.py](q3.py)
1. call `TreasuryDataScraper` to scrape data from website
2. call `TreasuryDatabaseManager` to save data into database


when using data for backtest
-  call `TreasuryDatabaseManager` to query data from database

