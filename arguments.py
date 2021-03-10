import  argparse

def get_args():
    # Instantiate argparse object
    parse = argparse.ArgumentParser(
        description = 'Program to rebalance a securities portfolio.'
    )

    parse.add_argument(
        "-d", "--debug",
        action      = "store_true",
        required    = False,
        help        = "Outputs debugging info to stdout."
        )

    # Parse file if argument given. This will be more complicated & will be done later
    parse.add_argument(
        "file",
        nargs       = '?',
        help        = "A file to parse. Currently supports yaml."
        )

    args = vars(parse.parse_args()) # Parse args namespace & convert to dictionary

    return args
