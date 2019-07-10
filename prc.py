import pandas_datareader.data as web
from datetime import datetime as dt

# Get current time
date = dt.now()

print('Enter security ticker symbols')
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
stocks = input()

# The 'iex' API is forbidden. It's either deprecated or we need an API key.
# Get a key, or find a suitable subsitute. Until then, the following code bails:
df = web.DataReader(stocks, 'iex', date, date)
print(df)
