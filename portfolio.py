#want an easy way to track the profit/loss of a portfolio
#Inputs are share price bought for, starttime, soldtime or null
import  datetime
import pandas_datareader.data as web
import  pandas as pd
import os

#share class does not make a great deal of sense
class Share():
    def __init__(self,name,quantity,price,fee,bought,sold):

        self.__init__(self,None,None,None,None,None)
        self.name = name
        self.bought = bought
        self.sold = sold
        self.quantity = quantity
        self.price = price
        self.fee = fee

def test(x):
    split_detail = str(x[1]).split(' ')
    date = x[0]
    val = x[3]

    if split_detail[0] == 'B':
        #share was bought at this time
        #temp_share = Share(split_detail[2],split_detail[1],val, val - )

    elif split_detail[0] == 'S':
        #share was sold at this time
    else:
        #errenous data
        pass
    print(t)
    #print(str(x[0]) + ' ' +  str(x[1]) + ' ' +  str(x[2]))

class Portfolio():

    def __init__(self):
        self.shares = []

    def add_share(self,share):
        self.shares.append(share)


    def calc_return(self):
        #for each share calculate the return for the specified dates
        for share in self.shares:
            df = web.DataReader(share.name, 'yahoo', share.bought, share.sold)
            print(df['Close'][:4])

    def import_csv_shares(self,path,source):

        df = pd.read_csv(path,parse_dates=['Date'] ,dayfirst=True)
        #df = pd.read_csv(path,parse_dates=['Date'] ,dayfirst=True)

        df = df.drop(['Reference', 'Debit ($)', 'Credit ($)', 'Type'], axis=1).dropna(how='any')

        df.columns = ['date','detail','balance']
        df.apply(test, axis=1)

        #print(df)

        # imports a csv share_name, date
        pass


start = datetime.datetime(2016, 1, 1)
end = datetime.datetime(2016, 4, 10)

m_port = Portfolio()

m_port.import_csv_shares(os.path.normpath("C:/Users/morga/Desktop/Learning/shares/transactions.csv"),'comsec')


#m_port.add_share(Share('MIN.AX',20,start,end))
#m_port.add_share(Share('MND.AX',20,start,end))
#m_port.calc_return()

