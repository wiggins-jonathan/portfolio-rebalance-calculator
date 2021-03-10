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

def main():
    args = arguments.get_args()

    if args['debug'] == 1:  # Print debug to stdout if debug mode is on.
        logging.basicConfig(
            level   = logging.DEBUG,
            format  = '%(levelname)s - %(message)s'
        )

    if args['file']:
        data = ingest.parseYaml(args['file'])
        log.debug(f"Data from {args['file']} is {data}")
    else:
        data = promptUser()
        log.debug(f"Data from user input is {data}")

    # Instantiate all ticker objects
    total       = 0
    sum_amounts = 0
    for ticker in data:
        if ticker == 'total':
            total = data[ticker]
            continue
        sum_amounts += (data[ticker]['current'])
    for ticker in data:
        if ticker == 'total':
            total = data[ticker]
            continue
        t           = Ticker(ticker)
        sharesToBuy = t.sharesToBuy(
                data[ticker]['current'],
                data[ticker]['desired'],
                sum_amounts,
                total
                )

        # Round share & dollar amounts to 2 sig figs
        sharesToBuy     = round(sharesToBuy, 2)
        amountToChange  = round(t.amountToChange, 2)

        # If amount is negative we need to sell, not buy
        var = 'Buy'
        if sharesToBuy < 0:
            sharesToBuy = abs(sharesToBuy)
            var = 'Sell'

        print(f'{var} ${amountToChange} of {t.name} or about {sharesToBuy} shares')

def promptUser():
    '''Gets input from user. Returns that input in a dictionary'''
    def readInput(prompt):
        '''Reads input continuously until no input received.'''
        '''Returns a generator for each input loop'''
        x = input(prompt)
        while x:
            yield x
            x = input(prompt)

    tickers = list(readInput('Enter ticker symbols -> '))
    data    = dict.fromkeys(tickers)
    for ticker in data:
        data[ticker] = dict.fromkeys(['current', 'desired'])

        prompt = f'Enter current amount in portfolio for {ticker} -> '
        data[ticker]['current'] = float(input(prompt))

        prompt = f'Enter desired percentage of {ticker} in portfolio -> '
        data[ticker]['desired'] = float(input(prompt))

    prompt = f'Enter total amount being contributed to porfolio -> '
    data['total'] = float(input(prompt))

    return data

if __name__ == '__main__':
    main()
