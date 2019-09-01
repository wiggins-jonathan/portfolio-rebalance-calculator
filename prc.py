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
    "-a",
    "--assets",
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
    action      = "append",
    type        = str,
    required    = False,
    metavar     = "[File]",
    nargs       = "+",
    help        = "Files and itemizes arguments given"
)

# Parse args
parse.parse_args()

#
## End args
#

stocks = input('Enter ticker symbols:\n')

def get_close_price(stocks):
    stocks = stocks.split(', ')
    df = web.av.quotes.AVQuotesReader(symbols=stocks, api_key=key)
    print(df.read())

if __name__ == "__main__":
    get_close_price(stocks)
