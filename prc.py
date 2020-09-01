#!/usr/bin/env python

import  arguments
import  logging
import  sys
import  yfinance as yf

log = logging.getLogger(__name__)   # Instantiate logger object

class Ticker:
    def __init__(self, name, amount, desiredPercent):
        self.name           = name
        self.amount         = amount
        self.desiredPercent = desiredPercent

        # Get today's closing price
        try:
            log.debug(f'Getting closing price for {self.name} from yf')
            df = yf.download(               # yf returns a pandas dataframe
                    self.name,
                    period      = "1d",     # 1 day
                    auto_adjust = True,     # Adjust for stock splits
                    progress    = False,    # Prints download progress to stdout
                    threads     = True      # Multi-thread download of ticker
                    )

            self.price = df["Close"][0]

            log.debug(f'Closing price for {self.name} is {self.price}.')
        except:
            print("Downloading data using yfinance failed. They probably changed their API.")
            sys.exit(1)

    # I think we can have a doMath function that will take in anonymous functions (lambda),
    # register the answer with the Ticker object, & also return the answer
    def sharesToBuy(self, sum_total, cash_addition):
        self.actualPercent  = (self.amount / sum_total) * 100
        log.debug(f'{self.name} is {self.actualPercent}% of total portfolio.')

        self.percentDiff    = self.desiredPercent - self.actualPercent
        log.debug(f'Percent difference from desired percent is {self.percentDiff}%')

        self.targetPercent  = self.percentDiff + self.desiredPercent
        log.debug(f'Percent to add to equal desired percent is {self.targetPercent}%')

        self.amountToChange = (self.targetPercent * cash_addition) / 100
        log.debug(f'Need to buy ${self.amountToChange} worth of {self.name} to equal desired percentage.')

        self.sharesToBuy    = self.amountToChange / self.price
        log.debug(f'Need to buy {self.sharesToBuy} shares of {self.name} to equal desired portfolio.')
        return self.sharesToBuy

def _check_debug(args):
    if args['debug'] == 1:
        logging.basicConfig(
            level   = logging.DEBUG,
            format  = '%(levelname)s - %(message)s'
        )

def main():
    args = arguments.get_args()
    _check_debug(args)

    # Data is in a list of lists at the 0th index
    tickers     = args["assets"][0]
    amounts     = args["amounts"][0]
    percents    = args["percents"][0]
    sum_total   = sum(amounts)

    # Instantiate all ticker objects
    for i in range(len(tickers)):
        t           = Ticker(tickers[i], amounts[i], percents[i])
        sharesToBuy = t.sharesToBuy(sum_total, args["total"])

        # Round share & dollar amounts to 2 sig figs
        sharesToBuy     = round(sharesToBuy, 2)
        amountToChange  = round(t.amountToChange, 2)

        # Display if we should buy or sell
        if sharesToBuy < 0:
            sharesToBuy = abs(sharesToBuy)
            var = "Sell"
        else:
            var = "Buy"
        print(f'{var} ${amountToChange} of {t.name} or about {sharesToBuy} shares')



if __name__ == "__main__":
    main()
