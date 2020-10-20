# -*- coding: utf-8 -*-
"""
Created on Fri May 26 11:09:50 2017

@author: tanach
"""
import urllib
import pandas as pd
from datetime import datetime,timedelta
from urllib.request import urlopen
import re
import time
from xml.dom import minidom
from yahoo_historical import Fetcher
import requests_html
from bs4 import BeautifulSoup
#pip install yahoo-historical

#def getHistQuote(symbol,start=(datetime.now()-timedelta(days=1*365)).strftime('%Y-%m-%d'),\
#                  end=datetime.now().strftime('%Y-%m-%d')):
#    '''Get historical stock quote'''
#    url_string = "https://finance.google.com/finance/historical?q={0}".format(symbol)
#    url_string += "&startdate={0}&enddate={1}&output=csv".format(
#                         start,end)
#    csv = urllib.urlopen(url_string).readlines()
#    csv.reverse()
#    sDate = map(lambda x:datetime.strptime(x.split(',')[0],'%d-%b-%y'),csv[:-1])
#    sOpen=map(lambda x:x.split(',')[1],csv[:-1])
#    sHigh=map(lambda x:x.split(',')[2],csv[:-1])
#    sLow=map(lambda x:x.split(',')[3],csv[:-1])
#    sClose=map(lambda x:x.split(',')[4],csv[:-1])    
#    df = pd.DataFrame({'Open':sOpen,'High':sHigh,'Low':sLow,'Adj Close':sClose},index=sDate)
#    df = df[df.Open!='-']
#    for c in df.columns:
#        df[c] = pd.to_numeric(df[c])
#    return df
def getDividend(symbol):
    ht = pd.read_html('https://finance.yahoo.com/quote/'+symbol+'?p='+symbol+'&.tsrc=fin-srch')
    s = ht[1].iloc[5][1]
    if len(s)>9:
        dp = float(s[:s.find("(")])
        dv = float(s[s.find("(")+1:s.find("%)")])
    else:
        dv,dp = 0,0
    return dv,dp

def getHistQuote(symbol,start=(datetime.now()-timedelta(days=1*365)),\
                  end=datetime.now()):
    start = [start.year,start.month,start.day]
    end = [end.year,end.month,end.day]
    data = Fetcher(symbol, start, end)
    df=pd.DataFrame(data.getHistorical())
    df.set_index('Date',inplace=True)
    df.index=pd.to_datetime(df.index)
    return df


def getHistQuotes(symbol,start=(datetime.now()-timedelta(days=2*365)).strftime('%m/%d/%Y'),\
                  end=datetime.now().strftime('%m/%d/%Y')):
    '''Get historical stock quote'''
    url_string = "https://www.investopedia.com/markets/api/partial/historical/?Symbol={0}".format(symbol)
    url_string += "&Type=%20Historical+Prices&Timeframe=Daily&StartDate={0}&EndDate={1}"\
    .format(start,end)
    st = pd.read_html(url_string)
    st = st[0]
    df = st.loc[1:]
    df.columns = st.loc[0]
    df = df.dropna()
    df.Date = pd.to_datetime(df.Date)
    df.set_index('Date',drop=True,inplace=True)
    df.columns = ['Open', 'High', 'Low', 'Adj Close', 'Volume']
    df['Close']=df['Adj Close']
    for c in df.columns:
        df[c] = pd.to_numeric(df[c])
    return df

def getQuotes(symbol):
    '''Get current stock quote'''
#    html = urlopen('https://finance.yahoo.com/quote/'+symbol).read()
#    html = html.decode('utf8').encode()
#    quote = re.findall(r'\d+\.\d+',html[html.find('regularMarketPrice')+27:\
#                                   html.find('regularMarketPrice')+37])
    html = pd.read_html('https://finance.yahoo.com/quote/'+symbol)
    quote = float(html[0][1][2].split('x')[0].replace(',',''))#html[0][1][1]
    return float(quote)

def getQuote(symbol):
    session = requests_html.HTMLSession()
    url = 'https://in.finance.yahoo.com/quote/' + symbol
    r = session.get(url)
    content = BeautifulSoup(r.content, 'lxml')
    try:
        price = str(content).split('data-reactid="32"')[4].split('</span>')[0].replace('>','')
    except IndexError:
        price = 0.00
    price = price or "0"
    try:
        price = float(price.replace(',',''))
    except ValueError:
        price = 0.00
    return price
    

def getQuoteCNN(symbol):
    '''Get current stock quote'''
    html = pd.read_html('http://money.cnn.com/quote/quote.html?symb='+symbol)
    quote = re.findall(r'\d+\.\d+',html[0][0][0])
    return float(quote[0])

def getRatios(symbol):
    '''Get important financial ratios such as P/E,PEG'''
    try:
        response = urlopen('''https://query.yahooapis.com/v1/public/yql?q=select%20*%20from%20yahoo.finance.quotes%20where%20symbol%3D%22'''+symbol+'''%22&env=store://datatables.org/alltableswithkeys''')
        xmldoc = minidom.parseString(response.read())
        EarningsShare = xmldoc.getElementsByTagName('EarningsShare')[0].firstChild.nodeValue
        PERatio = xmldoc.getElementsByTagName('PERatio')[0].firstChild.nodeValue
        PEGRatio = xmldoc.getElementsByTagName('PEGRatio')[0].firstChild.nodeValue
        ShortRatio = xmldoc.getElementsByTagName('ShortRatio')[0].firstChild.nodeValue
        OneyrTargetPrice = xmldoc.getElementsByTagName('OneyrTargetPrice')[0].firstChild.nodeValue
    except AttributeError:
        EarningsShare,PERatio,PEGRatio,ShortRatio,OneyrTargetPrice=0,0,0,0,0
    return EarningsShare,PERatio,PEGRatio,ShortRatio,OneyrTargetPrice        

if __name__ == '__main__':
    pass;
    
    
# http://www.google.com/finance/historical?q=msft&startdate=2012-05-22&enddate=2017-05-24&output=csv
    
