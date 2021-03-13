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

    @property
    def current(self):
        return self._current
    @current.setter
    def current(self, value):
        if value < 0:
            print(f'The current value of {self.name} in your portfolio cannot '
                'be less than 0')
            sys.exit(1)
        else:
            self._current = value

    @property
    def desired(self):
        return self._desired
    @desired.setter
    def desired(self, value):
        if value < 0 or value > 100:
            print(f'The desired percentage of {self.name} in your portfolio '
            'cannot be less than 0% greater than 100%')
            sys.exit(1)
        else:
            self._desired = value

    # I think we can have a doMath function that will take in anonymous functions (lambda),
    # register the answer with the Ticker object, & also return the answer
    def sharesToBuy(self, sum_amounts, cash_addition):
        self.actualPercent  = (self.current / sum_amounts) * 100
        log.debug(f'{self.name} is {self.actualPercent}% of total portfolio.')

        self.percentDiff    = self.desired - self.actualPercent
        log.debug(f'Percent difference from desired percent is {self.percentDiff}%')

        self.targetPercent  = self.percentDiff + self.desired
        log.debug(f'Percent of cash addition to add to equal desired percent is {self.targetPercent}%')

        self.amountToChange = (self.targetPercent * cash_addition) / 100
        log.debug(f'Need to buy ${self.amountToChange} worth of {self.name} to equal desired percentage.')

        self.sharesToBuy    = self.amountToChange / self.price
        log.debug(f'Need to buy {self.sharesToBuy} shares of {self.name} to equal desired portfolio.')
        return self.sharesToBuy

def convertToFloat(value):
    try:
        return float(value)
    except:
        print("The value you just entered must be a number")
        sys.exit(1)

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

    total, sum_amounts, sum_percents = 0, 0, 0
    objects         = []
    for ticker in data:
        if ticker == 'total':
            total = data[ticker]
            continue

        sum_amounts     += (data[ticker]['current'])
        sum_percents    += (data[ticker]['desired'])

        t = Ticker(ticker)
        t.current = data[ticker]['current']
        t.desired = data[ticker]['desired']
        objects.append(t)

    # Validate inputs
    if sum_amounts < 0:
        print(f'The sum of all amounts cannot be less than 0')
        sys.exit(1)
    if sum_percents != 100:
        print(f'The desired percents of all tickers in your portfolio must add '
            'up to 100%')
        sys.exit(1)

    # Calculate shares to buy
    for ticker in objects:
        sharesToBuy = ticker.sharesToBuy(sum_amounts, total)

        # Round share & dollar amounts to 2 sig figs
        sharesToBuy     = round(sharesToBuy, 2)
        amountToChange  = round(ticker.amountToChange, 2)

        # If amount is negative we need to sell, not buy
        var = 'Buy'
        if sharesToBuy < 0:
            sharesToBuy = abs(sharesToBuy)
            var = 'Sell'

        print(f'{var} ${amountToChange} of {ticker.name} or about {sharesToBuy} shares')

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
        data[ticker]['current'] = convertToFloat(input(prompt))

        prompt = f'Enter desired percentage of {ticker} in portfolio -> '
        data[ticker]['desired'] = convertToFloat(input(prompt))

    prompt = f'Enter total amount being contributed to porfolio -> '
    data['total'] = convertToFloat(input(prompt))

    return data

if __name__ == '__main__':
    main()
