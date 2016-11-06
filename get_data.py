"""
    Author: M Wood
    The purpose of this module is to download data from yahoo finance for machine learning applications
    pandas_datareader is very good at downloading table of stock price terent data
    needed to implement own class extension to get good quote data - yahoo quote


"""
import pandas as pd
import pandas_datareader.data as web
import yahoo_quote as yq
import datetime


#set startdate and enddate for trend data
start = datetime.datetime(2016, 1, 1)
end = datetime.datetime(2016, 1, 10)

#assuming asx shares need to add .ax to share name web request
morg_portfolio  = ['CBA.AX','MIN.AX']


#return a pandas array for stats. Stats only exist at current time
#print(yq.get_yahoo_stats(morg_portfolio))

#get historical actions -- dividends etc
#option 'yahoo' for base data
#option 'yahoo-dividends' for dividend data
#option 'yahoo-actions' for action data
#data returned  [Date	,Open	,High	,Low	Close	,Volume	,Adj Close]

df = web.DataReader('CBA.AX', 'yahoo', start, end)
print(df[['Open','High']][:4])

#print(web.DataReader(morg_portfolio, 'yahoo', start, end))
