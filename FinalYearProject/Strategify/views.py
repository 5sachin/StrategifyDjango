from django.shortcuts import render
import pandas as pd
import numpy as np
import io
import yfinance as yf
import base64,urllib
import matplotlib.pyplot as plt

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
        a = response.POST.get("indicator1").split(",")
        b = response.POST.get("indicator2").split(",")
        scriplist = response.POST.get('allscriplist')
        scriplist = scriplist.split(",")
        alldata = []
        for i in range(0,len(scriplist)-1):
            if a[0] == "MA":
                data = movingAverage(response, scriplist[i], int(a[1]), int(b[1]), response.POST.get('targetper'),
                                     response.POST.get('stoploss'), response.POST.get('quantityLots'))
                alldata.append(data)
            elif a[0] == "EMA":
                data = exponentialMovingAverage(response, scriplist[i], int(a[1]), int(b[1]),
                                                response.POST.get('targetper'), response.POST.get('stoploss'),
                                                response.POST.get('quantityLots'))
                alldata.append(data)
            elif a[0] == "WMA":
                data = weightedmovingaverage(response, scriplist[i], int(a[1]), int(b[1]), response.POST.get('targetper'),
                                     response.POST.get('stoploss'), response.POST.get('quantityLots'))
                alldata.append(data)

        return render(response, 'Strategify/backtestHistory.html',{'data':alldata})

def movingAverage(response,scrip,fastMa,slowMa,target,steploss,quantity):
    # data = pd.read_csv(scrip + '.csv')
    data = yf.download(scrip, start=response.POST.get('startDate'), end=response.POST.get('stopDate'))
    shortNo = fastMa
    longNo = slowMa
    data = data.apply(lambda x: x.fillna(x.value_counts().index[0]))
    data['shortAvg'] = data['Close'].rolling(window=shortNo).mean()
    data['longAvg'] = data['Close'].rolling(window=longNo).mean()
    data['Signal'] = np.where(data['shortAvg'] > data['longAvg'], 1, 0)
    data['Position'] = data['Signal'].diff()

    return movingAveragePLCalculaion(response, scrip, data, int(target), int(steploss), quantity)


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
    data = yf.download(scrip, start=response.POST.get('startDate'), end=response.POST.get('stopDate'))

    data = data.apply(lambda x: x.fillna(x.value_counts().index[0]))
    shortNo = fastMa
    longNo = slowMa

    days = [shortNo, longNo]
    for i in days:
        ema(data, days=i)

    data['Signal'] = np.where(data['EMA{}'.format(shortNo)] > data['EMA{}'.format(longNo)], 1, 0)
    data['Position'] = data['Signal'].diff()
    data.rename({'EMA{}'.format(shortNo): 'shortAvg', 'EMA{}'.format(longNo): 'longAvg'}, axis=1, inplace=True)

    return movingAveragePLCalculaion(response, scrip, data, int(target), int(steploss), quantity)


def wma(df,n):
    column = 'Close'
    weights = np.arange(1, n + 1)
    wmas = df[column].rolling(n).apply(lambda x: np.dot(x, weights) /
                                       weights.sum(), raw=True).to_list()
    df[f'WMA{n}'] = wmas


def weightedmovingaverage(response,scrip,fastMa,slowMa,target,steploss,quantity):
    data = yf.download(scrip, start=response.POST.get('startDate'), end=response.POST.get('stopDate'))

    data = data.apply(lambda x: x.fillna(x.value_counts().index[0]))
    shortNo = fastMa
    longNo = slowMa

    wma(data,shortNo)
    wma(data, longNo)

    data['Signal'] = np.where(data['WMA{}'.format(shortNo)] > data['WMA{}'.format(longNo)], 1, 0)
    data['Position'] = data['Signal'].diff()
    data.rename({'WMA{}'.format(shortNo): 'shortAvg', 'WMA{}'.format(longNo): 'longAvg'}, axis=1, inplace=True)

    return movingAveragePLCalculaion(response, scrip, data, int(target), int(steploss), quantity)

def movingAveragePLCalculaion(response,scrip,data,target,steploss,quantity):
    a = 0
    status = 0
    WinsCount = 0
    LossCount = 0
    totP = 0
    totL = 0
    balance = 0
    enter = 0
    alllist = []

    for i in range(0, len(data['Position'])):

        if data['Position'][i] == 1.0 and enter == 0:
            a = data['Close'][i]
            enter = 1
            alllist.append({
                'date': data.index[i],
                'price': data['Close'][i],
                'buysell': "buy",
                'balance': balance,
            })
            print("Buy Date: ",data.index[i]," Price: ",a)

        else:
            if a > 0:
                if ((data['Close'][i] - a) / a) * 100 >= int(target):
                    balance += data['Close'][i] - a
                    print("Profit ", " I ", i, " current price ", data['Close'][i], " buy price ", a, " Date: ",
                          data.index[i], " net profit ", data['Close'][i] - a)
                    WinsCount += 1
                    totP += data['Close'][i] - a
                    alllist.append({
                        'date': data.index[i],
                        'price': data['Close'][i],
                        'buysell': "sell",
                        'balance': balance
                    })
                    a = 0
                    enter = 0
                elif ((a - data['Close'][i]) / a) * 100 >= int(steploss):
                    balance += data['Close'][i] - a
                    print("Loss ", " I ", i, " current price ", data['Close'][i], " buy price ", a, " Date ",
                          data.index[i], " net loss ", data['Close'][i] - a)
                    LossCount += 1
                    totL += data['Close'][i] - a
                    alllist.append({
                        'date': data.index[i],
                        'price': data['Close'][i],
                        'buysell': "sell",
                        'balance': balance
                    })
                    a = 0
                    enter = 0

    print("Balance: ",balance," Total Wins: ",WinsCount," Total Loss: ",LossCount," Total Profit:  ", totP," Total Loss: ",totL)

    if totP + totL > 0:
        status = 1

    pd.DataFrame(alllist).to_csv('Strategify/static/Output.csv')
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
    alldata = {
        'ScripName': scrip.replace('.NS', ''),
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