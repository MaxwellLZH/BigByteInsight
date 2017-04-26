from stockdata import Stock
import numpy as np
import pandas as pd
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("symbol", help="Store the information of a given stock into local MySQL database")
parser.add_argument("-p", "--period", type=int, help="Specify the number of years for historical prices")
parser.add_argument("-v", "--verbose", help="increase output verbosity", action="store_true")
args = parser.parse_args()


#price history
s = Stock(args.symbol)
if args.period:
	price_history = s.historical_price(args.period)
else:
	#using default 3 year period
	price_history = s.historical_price()
symbol = s.symbol

if args.verbose:
	print "Number of entries: {}".format(len(price_history))

#summmary data
market_cap = s.get_market_cap()
book_value = s.get_book_value()
ebitda     = s.get_ebitda()
div_share  = s.get_dividend_share()
div_yield  = s.get_dividend_yield()
pe_ratio   = s.get_price_earnings_ratio()
short_ratio= s.get_short_ratio()
summary = pd.Series({'market_cap':market_cap, 'book_value':book_value,
                       'ebitda':ebitda, 'div_share':div_share})

if args.verbose:
	print "Stock summary information successfully retrieved."


#write to MySQL as two tables: price history and summary data
import MySQLdb
from sqlalchemy import create_engine

engine = create_engine("mysql+mysqldb://root:caonima@localhost:3306/stock")
price_history.to_sql(name=symbol, con=engine, if_exists='replace', index=False)

#TODO: Summary data into database
if args.verbose:
	print "Information successfully stored in local MySQL database."