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
        data = movingAvergaeWithtargetsteploss(response,response.POST.get('scripList'),15,40,response.POST.get('targetper'),response.POST.get('stoploss'),response.POST.get('quantityLots'))
        return render(response, 'Strategify/backtestHistory.html',{'data':data})

def movingAvergaeWithtargetsteploss(response,scrip,fastMa,slowMa,target,steploss,quantity):
    data = pd.read_csv(scrip + '.csv')
    print(quantity)
    shortNo = fastMa
    longNo = slowMa
    data = data.apply(lambda x: x.fillna(x.value_counts().index[0]))
    data['shortAvg'] = data['Close'].rolling(window=shortNo).mean()
    data['longAvg'] = data['Close'].rolling(window=longNo).mean()
    data['Signal'] = np.where(data['shortAvg'] > data['longAvg'], 1, 0)
    data['Position'] = data['Signal'].diff()

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
        else:
            if a > 0:
                if ((data['Close'][i] - a) / a) * 100 >= int(target):
                    balance += data['Close'][i] - a
                    print("Profit: ", "For  Index:  ", i, " Sell price: ", data['Close'][i], " Buy price: ", a, " On Date: ",
                          data['Date'][i], " Net profit ", data['Close'][i] - a)
                    WinsCount += 1
                    totP += data['Close'][i] - a
                    a = 0
                    enter = 0
                elif ((a - data['Close'][i]) / a) * 100 >= int(steploss):
                    balance += data['Close'][i] - a
                    print("Loss: ", "For  Index:  ", i, " Sell price: ", data['Close'][i], " Buy price: ", a,
                          " On Date: ", data['Date'][i], " Net profit ", data['Close'][i] - a)
                    LossCount += 1
                    totL += data['Close'][i] - a
                    a = 0
                    enter = 0

    print(balance, WinsCount, LossCount, totP, totL)

    if totP + totL > 0:
        status = 1


    periodHigh = "{:.2f}".format(data['Close'].max())
    periodLow = "{:.2f}".format(data['Close'].min())
    balance = "{:.2f}".format(balance)
    totP = "{:.2f}".format(totP)
    totL = "{:.2f}".format(-totL)

    AvgGain = 0
    AvgLoss = 0
    if WinsCount == 0:
        AvgGain = 0
        AvgLoss = "{:.2f}".format(float(totL) * int(quantity) / LossCount)
    elif LossCount == 0:
        AvgLoss = 0
        AvgGain = "{:.2f}".format(float(totP) * int(quantity) / WinsCount)
    else:
        AvgGain = "{:.2f}".format(float(totP)*int(quantity)/WinsCount)
        AvgLoss = "{:.2f}".format(float(totL)*int(quantity)/LossCount)

    x = plt.figure(figsize=(15, 8))
    plt.title(response.POST.get('strategyname') + " ON " + response.POST.get('scripList'), fontsize=18)
    plt.plot(data['Close'], alpha=1, label='Close')
    plt.plot(data['shortAvg'], alpha=1, label="SHORTAVG ", color="green")
    plt.plot(data['longAvg'], alpha=1, label='LONGAVG', color="red")
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
        'PL': float(balance) * int(quantity),
        'Status': status,
        'Signal': WinsCount + LossCount,
        'Wins': WinsCount,
        'Loss': LossCount,
        'MaxGain': float(totP)*int(quantity),
        'MaxLoss': float(totL)*int(quantity),
        'PeriodHigh': periodHigh,
        'PeriodLow': periodLow,
        'AvgGain': AvgGain,
        'AvgLoss': AvgLoss,
        'Uri': uri,
        'PercentBar': percentBar,
    }

    return alldata

def movingAverage(response, scrip,fastMa,slowMa):
    data = pd.read_csv(scrip+'.csv')
    shortNo = fastMa
    longNo = slowMa
    data = data.apply(lambda x: x.fillna(x.value_counts().index[0]))
    data['shortAvg'] = data['Close'].rolling(window=shortNo).mean()
    data['longAvg'] = data['Close'].rolling(window=longNo).mean()
    data['Signal'] = np.where(data['shortAvg'] > data['longAvg'], 1, 0)
    data['Position'] = data['Signal'].diff()

    a = 0
    wins = 0
    loss = 0
    totP = 0
    totL = 0
    balance = 0
    status = 0

    for i in range(0, len(data['Position'])):
        if data['Position'][i] == 1.0:
            a = data['Close'][i]
        elif data['Position'][i] == -1.0:
            b = data['Close'][i]
            balance += b - a
            if b - a > 0:
                wins += 1
                totP += b - a
            else:
                loss += 1
                totL += b - a

    if totP + totL > 0:
        status = 1

    print(totP,totL,status)
    print(data)

    periodHigh = "{:.2f}".format(data['Close'].max())
    periodLow = "{:.2f}".format(data['Close'].min())
    balance = "{:.2f}".format(balance)
    totP = "{:.2f}".format(totP)
    totL = "{:.2f}".format(-totL)


    x = plt.figure(figsize=(15, 8))
    plt.title(response.POST.get('strategyname')+" ON "+response.POST.get('scripList'), fontsize=18)
    plt.plot(data['Close'], alpha=1, label='Close')
    plt.plot(data['shortAvg'], alpha=1, label="SHORTAVG ", color="green")
    plt.plot(data['longAvg'], alpha=1, label='LONGAVG', color="red")
    plt.xlabel('Date', fontsize=18)
    plt.ylabel('Close Price', fontsize=18)

    buf = io.BytesIO()
    x.savefig(buf, format="png")
    buf.seek(0)
    string = base64.b64encode(buf.read())
    uri = urllib.parse.quote(string)

    percentBar = (float(totP)/(float(totP)+float(totL)))*100
    data.to_csv('file.csv')

    alldata = {
        'ScripName': response.POST.get('scripList'),
        'PL': balance,
        'Status': status,
        'Signal': wins+loss,
        'Wins': wins,
        'Loss': loss,
        'MaxGain': totP,
        'MaxLoss': totL,
        'PeriodHigh': periodHigh,
        'PeriodLow': periodLow,
        'Uri': uri,
        'PercentBar': percentBar,
    }

    return alldata
