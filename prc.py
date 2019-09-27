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
parse = argparse.ArgumentParser(
    description = 'Program to rebalance a securities portfolio.'
    )

#
## Args
#

parse.add_argument(
    "-a", "--assets",
    action      = "append",
    type        = str,
    required    = True,
    metavar     = "[Assets]",
    nargs       = "+",
    help        = "List ticker number of assets to be balanced."
                    " Separate multiple tickers by spaces"
)
parse.add_argument(
    "-$", "--amounts",
    action      = "append",
    type        = int,
    required    = True,
    metavar     = "[Amounts]",
    nargs       = "+",
    help        = "List amounts of each asset to be balanced"
)

parse.add_argument(
    "-%", "--percentages",
    action      = "append",
    type        = int,
    required    = True,
    metavar     = "[Percentages]",
    nargs       = "+",
    help        = "List desired percentages to rebalance into porfolio."
)

# Parse file if argument given. This will be more complicated & will be done later
parse.add_argument(
    "-f", "--file",
    action      = "append",
    type        = str,
    required    = False,
    metavar     = "[File]",
    help        = "A file with arguments to parse"
)

parse.add_argument(
    "-t", "--total",
    action      = "store",
    type        = int,
    required    = True,
    metavar     = "[Total]",
    help        = "Total amount to be rebalanced."
)

# Parse args namespace & convert to dictionary
args = vars(parse.parse_args())

#
## End args
#

# Loop through assets & get price
stocks = args["assets"]
def get_close_price(stocks):
    for stock in stocks:
        df = web.av.quotes.AVQuotesReader(symbols=stock, api_key=key)
        print(df.read())
        df.close()
    # Figure out syntax to get specific dataframe column, price

if __name__ == "__main__":
    get_close_price(stocks)
