from django.shortcuts import render
import pandas as pd
import numpy as np
import io
from datetime import datetime
import base64,urllib
import matplotlib.pyplot as plt
from nsepy import get_history
plt.style.use('fivethirtyeight')


def home(response):
    return render(response, 'Strategify/index.html',{})

def registration(response):
    return render(response, 'Strategify/registrationPage.html', {})

def contactus(response):
    return render(response, 'Strategify/contactus.html', {})

def profilepage(response):
    return render(response, 'Strategify/profilePage.html', {})

def createstrategy(response):

    return render(response, 'Strategify/createStrategy.html', {})

def createStrategyForm(response):

    if response.method == "POST":
        # data = movingAverage(response,response.POST.get('scripList'),15,20)
        data = movingAverage(response,response.POST.get('scripList'),7,14,response.POST.get('targetper'),response.POST.get('stoploss'),response.POST.get('quantityLots'))
        # data = exponentialMovingAverage(response,response.POST.get('scripList'),10,15,response.POST.get('targetper'),response.POST.get('stoploss'),response.POST.get('quantityLots'))
        return render(response, 'Strategify/backtestHistory.html',{'data':data})

def movingAverage(response,scrip,fastMa,slowMa,target,steploss,quantity):
    data = pd.read_csv(scrip + '.csv')
    print(quantity)
    shortNo = fastMa
    longNo = slowMa
    data = data.apply(lambda x: x.fillna(x.value_counts().index[0]))
    data['shortAvg'] = data['Close'].rolling(window=shortNo).mean()
    data['longAvg'] = data['Close'].rolling(window=longNo).mean()
    data['Signal'] = np.where(data['shortAvg'] > data['longAvg'], 1, 0)
    data['Position'] = data['Signal'].diff()

    return movingAveragePLCalculaion(response, data, int(target), int(steploss), quantity, fastMa, slowMa)


def ema(df, days, col='Close', start=0):
    pd.set_option('display.max_rows', 500)
    if df.shape[0] > days:
        multiplier = 2 / (days + 1)
        first_ema = df.iloc[:days, df.columns.get_loc(col)].sum(axis=0) / days
        df['EMA{}'.format(days)] = np.nan
        df['EMA{}'.format(days)][days - 1] = first_ema
        for i in range(days, (df.shape[0])):
            EMA = df.iloc[i, df.columns.get_loc(col)] * multiplier + df.iloc[
                (i - 1), df.columns.get_loc("EMA{}".format(days))] * (1 - multiplier)
            df['EMA{}'.format(days)][i] = EMA
            df['EMA{}'.format(days)][i] = EMA
            start = start + 1
    else:
        print("Not Sufficient data to calculate {}-days EMA".format(days))


def exponentialMovingAverage(response,scrip,fastMa,slowMa,target,steploss,quantity):
    data = pd.read_csv(scrip + '.csv')
    print(quantity)
    data = data.apply(lambda x: x.fillna(x.value_counts().index[0]))
    shortNo = fastMa
    longNo = slowMa

    days = [10, 15]
    for i in days:
        ema(data, days=i)

    data['Signal'] = np.where(data['EMA{}'.format(shortNo)] > data['EMA{}'.format(longNo)], 1, 0)
    data['Position'] = data['Signal'].diff()
    data.rename({'EMA{}'.format(shortNo): 'shortAvg', 'EMA{}'.format(longNo): 'longAvg'}, axis=1, inplace=True)

    return movingAveragePLCalculaion(response,data,int(target),int(steploss),quantity,fastMa,slowMa)


def movingAveragePLCalculaion(response,data,target,steploss,quantity,shortNo,longNo):
    a = 0
    status = 0
    WinsCount = 0
    LossCount = 0
    totP = 0
    totL = 0
    balance = 0
    enter = 0

    for i in range(0, len(data['Position'])):

        if data['Position'][i] == 1.0 and enter == 0:
            a = data['Close'][i]
            enter = 1
            print("Buy Date: ",data['Date'][i]," Price: ",a)

        else:
            if a > 0:
                if ((data['Close'][i] - a) / a) * 100 >= int(target):
                    balance += data['Close'][i] - a
                    print("Profit ", " I ", i, " current price ", data['Close'][i], " buy price ", a, " Date: ",
                          data['Date'][i], " net profit ", data['Close'][i] - a)
                    WinsCount += 1
                    totP += data['Close'][i] - a
                    a = 0
                    enter = 0
                elif ((a - data['Close'][i]) / a) * 100 >= int(steploss):
                    balance += data['Close'][i] - a
                    print("Loss ", " I ", i, " current price ", data['Close'][i], " buy price ", a, " Date ",
                          data['Date'][i], " net loss ", data['Close'][i] - a)
                    LossCount += 1
                    totL += data['Close'][i] - a
                    a = 0
                    enter = 0

    print("Balance: ",balance," Total Wins: ",WinsCount," Total Loss: ",LossCount," Total Profit:  ", totP," Total Loss: ",totL)

    if totP + totL > 0:
        status = 1

    periodHigh = "{:.2f}".format(data['Close'].max())
    periodLow = "{:.2f}".format(data['Close'].min())
    balance = "{:.2f}".format(balance)
    totP = "{:.2f}".format(totP)
    totL = "{:.2f}".format(-totL)

    if WinsCount == 0:
        AvgGain = 0
        AvgLoss = "{:.2f}".format(float(totL) * int(quantity) / LossCount)
    elif LossCount == 0:
        AvgLoss = 0
        AvgGain = "{:.2f}".format(float(totP) * int(quantity) / WinsCount)
    else:
        AvgGain = "{:.2f}".format(float(totP) * int(quantity) / WinsCount)
        AvgLoss = "{:.2f}".format(float(totL) * int(quantity) / LossCount)

    print(data.columns)
    x = plt.figure(figsize=(15, 7))
    plt.title('Close Price History w/ Buy & Sell Signals', fontsize=18)
    plt.plot(data['Close'], alpha=0.5, label='Close')
    plt.plot(data['shortAvg'], alpha=1, label='shortAvg', color="green")
    plt.plot(data['longAvg'], alpha=1, label='longAvg', color="red")
    plt.xlabel('Date', fontsize=18)
    plt.ylabel('Close Price', fontsize=18)

    buf = io.BytesIO()
    x.savefig(buf, format="png")
    buf.seek(0)
    string = base64.b64encode(buf.read())
    uri = urllib.parse.quote(string)

    percentBar = (float(totP) / (float(totP) + float(totL))) * 100
    data.to_csv('file.csv')
    alldata = {
        'ScripName': response.POST.get('scripList'),
        'PL': "{:.2f}".format(float(balance) * int(quantity)),
        'Status': status,
        'Signal': WinsCount + LossCount,
        'Wins': WinsCount,
        'Loss': LossCount,
        'MaxGain': "{:.2f}".format(float(totP) * int(quantity)),
        'MaxLoss': "{:.2f}".format(float(totL) * int(quantity)),
        'PeriodHigh': periodHigh,
        'PeriodLow': periodLow,
        'AvgGain': AvgGain,
        'AvgLoss': AvgLoss,
        'Uri': uri,
        'PercentBar': percentBar,
    }

    return alldata