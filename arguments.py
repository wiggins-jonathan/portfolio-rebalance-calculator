import  argparse

def get_args():
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
