#!/usr/bin/env python

import  yaml
import  argparse
import  pandas_datareader   as web
from    pathlib import Path as path

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

# Instantiate argparse object
parse = argparse.ArgumentParser()

#
## Args
#

# Add total amount to be rebalanced
parse.add_argument(
    "-t",
    "--total",
    action      = "store",
    type        = int,
    required    = True,
    metavar     = "[Total]",
    help        = "Total amount to be rebalanced."
)

# Add Assets
parse.add_argument(
    "-a",       # This is the short option
    "--assets", # This is the long option
    action      = "append",
    type        = str,
    required    = True,
    metavar     = "[Assets]",
    # You'll probably want to separate them by commas when passed to a function.
    help        = "List assets to be balanced."
)
# Add Amounts
parse.add_argument(
    "-$",
    "--amounts",
    action      = "append",
    type        = int,
    required    = True,
    metavar     = "[Amounts]",
    help        = "List amounts of each asset to be balanced"
)

# Add target allocation
parse.add_argument(
    "-%",
    "--percentages",
    action      = "append",
    type        = int,
    required    = True,
    metavar     = "[Percentages]",
    help        = "List desired percentages to rebalance into porfolio."
)

# Parse file if argument given. This will be more complicated & must use nargs
parse.add_argument(
    "-f",
    "--file",
    required    = False,
    metavar     = "[File]",
    help        = "File to parse. Expand this help text later."
)

# Parse args
parse.parse_args()

#
## End args
#

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
