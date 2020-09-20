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
        help        = "Outputs important debugging info to stdout."
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

    args = vars(parse.parse_args()) # Parse args namespace & convert to dictionary

    return args
