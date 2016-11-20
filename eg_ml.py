import pandas_datareader.data as web

import pandas as pd
import math,datetime
import numpy as np
from sklearn import preprocessing, cross_validation, svm
from sklearn.linear_model import LinearRegression
import matplotlib.pyplot as plt
from matplotlib import style
import pickle #can be used to save the classifier


style.use('ggplot')

#set the data that you want to download - if you are training a new stock you will want all of it
start = datetime.datetime(2011, 1, 1)
end = datetime.datetime(2017, 1, 1)

stock = 'TGA'

#Get the data for the stock specified from yahoo and put it in a data fram
df = web.DataReader(stock + '.AX', 'yahoo', start, end)


df = df[['Open','High','Low','Adj Close','Volume']]
#define some ratios to use to train the dataset
df['HL_PCT'] = (df['High'] - df['Adj Close'])/df['Adj Close'] * 100
df['PCT_change'] = (df['Adj Close'] - df['Open'])/df['Open'] * 100
df = df[['Adj Close','HL_PCT','PCT_change','Volume']]

#set the forcust column - the column you are trying to predict
forecast_col = 'Adj Close'

#ML can't work with Nulls, so treat them as outliers instead
df.fillna(-99999,inplace=True)

#This is the number of days you want to forecast out too
forecast_out = int(math.ceil(0.01*len(df)))

#The label (is the forecast column 0.01 % of the data frame in the future).
df['Label'] = df[forecast_col].shift(-forecast_out)

#features - df.drop returns a new df
X = np.array(df.drop(['Label'],1))

#scale all x to be between [0-1]
X = preprocessing.scale(X)
#define x lately which are just the rows you want to predict data for
X_lately = X[-forecast_out:]
X = X[:-forecast_out]


#X = X[:-forecast_out + 1] #need to make sure that x and y is the same length
df.dropna(inplace=True)

#labels
y = np.array(df['Label'])

#Get some training and testing data - 20%
X_train,X_test,y_train,y_test = cross_validation.train_test_split(X,y,test_size=0.2)

#set the classifier to linear regression
clf = LinearRegression()
#Set the clasifier to and svm
#clf = svm.SVR()

#train the clasifier with the data
clf.fit(X_train,y_train)

#test how confident we are in this clasifier with the training data
confidence = clf.score(X_test,y_test)

forecast_set = clf.predict(X_lately)
print('Confidence: ' + str(confidence) + '. Days forcasted:' +str(forecast_out))

#make a new row called forecast and set all values to nan
df['Forecast'] = np.nan

#Get the last date. iloc is used as an index based reference only. -1 can be used to get the last rows data
#name is the index column in this case
last_date = df.iloc[-1].name
last_unix = last_date.timestamp()
print(last_unix)
one_day = 86400
next_unix = last_unix + one_day

#this bit of code adds a row full of nans and a value to the forcast set to the next_date index
for i in forecast_set:
    next_date = datetime.datetime.fromtimestamp(next_unix)
    next_unix += one_day
    df.loc[next_date] = [np.nan for _ in range(len(df.columns)-1)] + [i]

#plot the data
df['Adj Close'].plot()
df['Forecast'].plot()
plt.legend(loc=4)
plt.xlabel('Date')
plt.ylabel('price')
plt.show()