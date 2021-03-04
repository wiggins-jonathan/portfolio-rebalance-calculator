#!/usr/bin/env python

import  arguments
import  ingest
import  logging
import  sys
import  yfinance as yf

log = logging.getLogger(__name__)   # Instantiate logger object

class Ticker:
    def __init__(self, name):
        self.name = name

        # Get today's closing price
        try:
            log.debug(f'Getting closing price for {self.name} from yf')
            df = yf.download(               # yf returns a pandas dataframe
                    self.name,
                    period      = '1d',     # 1 day
                    auto_adjust = True,     # Adjust for stock splits
                    progress    = False,    # Prints download progress to stdout
                    threads     = True      # Multi-thread download of ticker
                    )

            self.price = df['Close'][0] # Grab closing price out of data frame

            log.debug(f'Closing price for {self.name} is {self.price}.')
        except:
            print('Downloading data using yfinance failed.')
            sys.exit(1)

    # I think we can have a doMath function that will take in anonymous functions (lambda),
    # register the answer with the Ticker object, & also return the answer
    def sharesToBuy(self, amount, desiredPercent, sum_amounts, cash_addition):
        self.amount         = amount
        self.desiredPercent = desiredPercent
        self.actualPercent  = (self.amount / sum_amounts) * 100
        log.debug(f'{self.name} is {self.actualPercent}% of total portfolio.')

        self.percentDiff    = self.desiredPercent - self.actualPercent
        log.debug(f'Percent difference from desired percent is {self.percentDiff}%')

        self.targetPercent  = self.percentDiff + self.desiredPercent
        log.debug(f'Percent of cash addition to add to equal desired percent is {self.targetPercent}%')

        self.amountToChange = (self.targetPercent * cash_addition) / 100
        log.debug(f'Need to buy ${self.amountToChange} worth of {self.name} to equal desired percentage.')

        self.sharesToBuy    = self.amountToChange / self.price
        log.debug(f'Need to buy {self.sharesToBuy} shares of {self.name} to equal desired portfolio.')
        return self.sharesToBuy

# Print debug statements to stdout if debug mode is on.
def _check_debug(args):
    if args['debug'] == 1:
        logging.basicConfig(
            level   = logging.DEBUG,
            format  = '%(levelname)s - %(message)s'
        )

# Reads input continuously until no input received.
# Returns a generator for each input loop
def readInput(prompt):
    x = input(prompt)
    while x:
        yield x
        x = input(prompt)

def main():
    args = arguments.get_args()
    _check_debug(args)

    tickers, amounts, percents = [], [], []
    if args['file']:    # If there is a file
        yamlData = ingest.parseYaml(args['file'])

        # We might want to revisit the names of these variables
        total = 0
        for key in yamlData:
            if key == 'total':
                total = yamlData['total']
                continue
            tickers.append(key)
            amounts.append(yamlData[key]['current'])
            percents.append(yamlData[key]['desired'])
    else:               # No file. Run prompt
        tickers = list(readInput('Enter ticker symbols -> '))

        for ticker in tickers:
            prompt = f'Enter current amount in portfolio for {ticker} -> '
            amounts.append(float(input(prompt)))

            prompt = f'Enter desired percentage of {ticker} in portfolio -> '
            percents.append(float(input(prompt)))


        total = float(input('Enter total amount being contributed to porfolio -> '))

    sum_amounts = sum(amounts)

    # Instantiate all ticker objects
    for i in range(len(tickers)):
        t           = Ticker(tickers[i])
        sharesToBuy = t.sharesToBuy(amounts[i], percents[i], sum_amounts, total)

        # Round share & dollar amounts to 2 sig figs
        sharesToBuy     = round(sharesToBuy, 2)
        amountToChange  = round(t.amountToChange, 2)

        # If amount is negative we need to sell, not buy
        var = 'Buy'
        if sharesToBuy < 0:
            sharesToBuy = abs(sharesToBuy)
            var = 'Sell'

        print(f'{var} ${amountToChange} of {t.name} or about {sharesToBuy} shares')

if __name__ == '__main__':
    main()
