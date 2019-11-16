#!/usr/bin/env python

import  yaml
import  argparse
import  logging
import  pandas_datareader   as web
from    pathlib import Path as path

# Get paths
rel_path        = path(__file__).parent
secrets_file    = path(f'{rel_path}/secrets.yaml')

log = logging.getLogger(__name__)   # Instantiate logger object

# Print debug statements to console if debug mode is on
def _check_debug(args):
    if args['debug'] == 1:
        logging.basicConfig(
            level   = logging.DEBUG,
            format  = '%(levelname)s - %(message)s'
        )

# Get Alpha Vantage api key
with open(secrets_file, 'r') as f:
    try:
        api = yaml.safe_load(f)
        key = api['alpha_vantage']['api_key']
    except yaml.YAMLError as yaml_error:
        print(yaml_error)

def main():
    args = _get_args()
    _check_debug(args)

    tickers = (args["assets"][0])

    log.debug('Rounding final totals to 2 significant figures...')
    totals = _round_list(_get_final_totals(args),   2)
    shares = _round_list(_get_share_amounts(args),  0)

    for z, y, x in zip(shares, tickers, totals):
        if x < 0:
            x   = abs(x)
            z   = abs(z)
            var = 'Sell'
        else:
            var = 'Buy'

        print(f'{var} ${x} of {y} or about {z} share(s)')

#
## Helper Functions
#

def _get_args():
    # Instantiate argparse object
    parse = argparse.ArgumentParser(
        description = 'Program to rebalance a securities portfolio.'
    )

    parse.add_argument(
        "-a", "--assets",
        action      = "append",
        type        = str,
        required    = True,
        metavar     = "assets",
        nargs       = "+",
        help        = "List ticker number of assets to be balanced."
                      " Separate multiple tickers by spaces."
    )
    parse.add_argument(
        "-$", "--amounts",
        action      = "append",
        type        = float,
        required    = True,
        metavar     = "amounts",
        nargs       = "+",
        help        = "List amounts of each asset to be balanced."
                      " Separate multiple amounts by spaces."
    )
    parse.add_argument(
        "-%", "--percentages",
        action      = "append",
        type        = float,
        required    = True,
        metavar     = "percentages",
        nargs       = "+",
        help        = "List desired percentages to rebalance into porfolio."
    )
    # Parse file if argument given. This will be more complicated & will be done later
    parse.add_argument(
        "-f", "--file",
        action      = "append",
        type        = str,
        required    = False,
        metavar     = "file",
        help        = "A file with arguments to parse."
    )
    parse.add_argument(
        "-t", "--total",
        action      = "store",
        type        = float,
        required    = True,
        metavar     = "total",
        help        = "Total amount to be contributed."
    )
    parse.add_argument(
        "-d", "--debug",
        action      = "store_true",
        required    = False,
        help        = "Outputs important debugging info to stdout."
    )

    args = vars(parse.parse_args()) # Parse args namespace & convert to dictionary

    return args

#
## Math functions
#

def _get_share_price(args):
    stocks = args["assets"]

    # Loop through assets & get current prices
    for stock in stocks:
        data    = web.av.quotes.AVQuotesReader(symbols=stock, api_key=key)
        df      = (data.read())
        prices  = (df["price"].tolist())
        data.close()
        return(prices)

def _get_share_amounts(args):
    prices = _get_share_price(args)
    totals = _get_final_totals(args)

    share_amounts = [y / x for y, x in zip(totals, prices)]

    return(share_amounts)

def _get_amount_totals(args):
    amount_args = args["amounts"][0]
    total       = sum(amount_args)

    return(total)

def _get_actual_percentages(args):
    percent_args    = args["amounts"][0]
    actual_percents = []

    for percent in percent_args:
        totals = 100 * (percent / _get_amount_totals(args))
        actual_percents.append(totals)

    return(actual_percents)

def _get_target_percents(args):
    desired = args["percentages"][0]
    actual  = _get_actual_percentages(args)

    diffs           = []
    target_percents = []

    diffs           = [y - x for y, x in zip(desired, actual)]
    target_percents = [y + x for y, x in zip(diffs, desired)]

    return(target_percents)

def _get_final_totals(args):
    total   = args["total"]
    targets = _get_target_percents(args)

    final_totals = []

    for target in targets:
        final_total = (target * total) / 100
        final_totals.append(final_total)

    return(final_totals)

def _round_list(list_to_round, sig_fig):
    totals = list_to_round

    rounded_totals = []

    for total in totals:
        rounded_total = round(total, sig_fig)
        rounded_totals.append(rounded_total)

    return(rounded_totals)

#
## End Helper Functions
#

if __name__ == "__main__":
    main()
