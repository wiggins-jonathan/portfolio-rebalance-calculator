import yaml
import pandas_datareader    as web
from pathlib    import Path as path

# Get paths
rel_path        = path(__file__).parent
secrets_file    = path(f'{rel_path}/secrets.yaml')

# Get Alpha Vantage api key
with open(secrets_file, 'r') as f:
    try:
        api = yaml.safe_load(f)
        key = api['alpha_vantage']['api_key']
    except yaml.YAMLError as yaml_error:
        print(yaml_error)

stocks = input('Enter ticker symbols:\n')
'''
 We need to decide how to parse user input here.
 A few ways we could do this in rising levels of difficulty:
    1). Split on delimmiter <- We are doing this now using a comma. It sucks & is lazy
    2). Ask user how many tickers they need. Take in n tickers. This kind of sucks,
       But would work quickly.
    4). Loop through multiple inputs & take in n tickers until we get a null ticker,
       (the user hits enter without specifying anything)
    5). We take in command line arguments using the argparse module.
    6). We create an ncurses TUI
    7). We create a webapp
'''

def get_close_price(stocks):
    stocks = stocks.split(', ')
    df = web.av.quotes.AVQuotesReader(symbols=stocks, api_key=key)
    print(df.read())

get_close_price(stocks)
