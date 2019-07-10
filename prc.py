import pandas_datareader.data as web
from datetime import datetime as dt

# Get current time
pretty_date = '%Y-%m-%d'
now         = (dt.now().strftime(pretty_date))

stocks = input('Enter ticker symbols:\n')
'''
 We need to decide how to parse user input here
 A few ways we could do this:
 1). Split on comma
 2). Split on space
 3). Ask user how many tickers they need. Take in n tickers
 4). Take in n tickers until we get a null ticker (the user hits enter without
    specifying a anything
 5). Some other ways I can't think of right now
'''
# Print closing price
df = web.DataReader(stocks, 'stooq')
close = (df.loc[now, 'Close'])
print(close)
