# -*- coding: utf-8 -*-
"""
Created on Mon Oct 19 22:39:10 2020

@author: tanay
"""
import pandas as pd
from datetime import datetime,timedelta
from Utility import getHistQuote

def prepareData():
    data = pd.DataFrame()
    
    for symbol in symbols:    
        df = getHistQuote(symbol,start=(datetime.now()-timedelta(days=12*365)),\
                          end=datetime.now())
        df = df[df.index>='2009-01-01']
        
        df.reset_index(inplace=True)
        
        df.columns = ['datadate','prcod','prchd','prcld','prccd','Adj Close','cshtrd']
        df['ajexdi'] = df.prccd/df['Adj Close']
        df['tic'] = symbol
        df = df[['datadate', 'tic', 'prccd', 'ajexdi', 'prcod', 'prchd',\
                     'prcld', 'cshtrd']]
        data = data.append(df)
    
    data.datadate = data.datadate.apply(lambda x: x.strftime('%Y%m%d')).astype(int)
    
    data.to_csv('../data/TopTech_2009_2020.csv')
    
    print(data.head())
    
if __name__ == '__main__':
    symbols=['MSFT','ADBE','AAPL','GOOG','AMZN','BA','ORCL','IBM']
    prepareData()
    