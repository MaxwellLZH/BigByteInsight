from yahoo_finance import Share
from datetime import date, timedelta
import numpy as np
import pandas as pd


class Stock(Share):
    
    #default using 3 years of historical data
    TODAY = date.today()
    DEFAULT_PERIOD = timedelta(365*3)
    
    def __init__(self, symbol):
        super(Stock, self).__init__(symbol)
        self.symbol = symbol
    
    def historical_price(self, period=None, end=None):
        #get the historical prices and volumn of the stock
        #params: end date and time period (in years)
        #return: dataframe
        end_date = end if end else self.TODAY
        period   = timedelta(365*period) if period else self.DEFAULT_PERIOD
        start_date = end_date - period
        history  = self.get_historical(str(start_date), str(end_date))
        
        tick_close = [t['Adj_Close'] for t in history]
        tick_date  = [t['Date'] for t in history]
        tick_volume= [t['Volume'] for t in history]
        return pd.DataFrame({'Date':tick_date[::-1], 'Close':tick_close[::-1],
                           'Volume':tick_volume[::-1]})
    
    
    #########TODO:  some extra methods for getting summary methods ##########
    
    
    
test = Stock('VNQ')
print test.historical_price()