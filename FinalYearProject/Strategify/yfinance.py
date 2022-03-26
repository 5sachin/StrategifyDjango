import yfinance as yf
import pandas as pd

def getScripData(scripname,startdate,enddate):
    data = yf.download(scripname + ".NS", start=startdate, end=enddate)
    return data

def getScripChartsData(scripname,period):
    print("Period: ",period)
    data = yf.download( tickers=scripname+".NS",period = period)

    df = pd.DataFrame(data, columns = ['Close'], index = data.index)
    df['date'] = df.index.date
    return df
