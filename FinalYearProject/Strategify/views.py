from django.http import JsonResponse
from django.shortcuts import render, redirect
import pandas as pd
import numpy as np
import io
import yfinance as yf
import base64,urllib
import matplotlib.pyplot as plt
from .models import UserRegistration

plt.style.use('fivethirtyeight')
data = None

def home(response):
    return render(response, 'Strategify/index.html',{})



def registration(request):
    return render(request, 'Strategify/registrationPage.html', {})


def signup(request):
    response_data = {}
    if request.method == 'POST':
        username = request.POST.get('username')
        name = request.POST.get('name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        password = request.POST.get('password')

        try:
            UserRegistration.objects.create(
                username = username,
                name = name,
                email = email,
                phone = phone,
                password = password,
            )
            response_data['success'] = "Account Created"
            return JsonResponse(response_data)
        except Exception as e:
            response_data['error'] = e
            return JsonResponse(response_data)
    else:
        response_data['error'] = "Error Occured"
        return JsonResponse(response_data)

def checkUsername(request):
    response_data = {}
    if request.method == 'POST':
        username = request.POST.get('username')
        try:
            if UserRegistration.objects.filter(username=username).exists():
                response_data['success'] = "Availiable"
            else:
                response_data['error'] = "Not Availiable"
        except Exception as e:
            print(e)
        return JsonResponse(response_data)


def signIn(request):
    response_data = {}
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        try:
            user_data = UserRegistration.objects.get(username=username)
            if(user_data):
                if user_data.email == email and user_data.password == password:
                    response_data['success'] = "Logged In Success"
                    dashboard(request)
                else:
                    response_data['error'] = "Invalid Login"
            else:
                response_data['error'] = "Invalid Login"
        except Exception as e:
            response_data['error'] = "Invalid Login"
        return JsonResponse(response_data)

def contactus(response):
    return render(response, 'Strategify/contactus.html', {})

def profilepage(response):
    return render(response, 'Strategify/profilePage.html', {})

def createstrategy(response):
    return render(response, 'Strategify/createStrategy.html', {})

def dashboard(response):
    print(response.POST.get('username'))
    return render(response,'Strategify/dashboard.html', {})

def createStrategyForm(response):
    global data
    try:
        if response.method == "POST":
            a = response.POST.get("indicator1").split(",")
            b = response.POST.get("indicator2").split(",")
            startDate = response.POST.get('startDate')
            stopDate = response.POST.get('stopDate')
            x = b[0]
            b[0]= a[1]
            a[1] = x
            scriplist = response.POST.get('allscriplist')
            scriplist = scriplist.split(",")
            alldata = []

            for i in range(0,len(scriplist)-1):
                try:
                    data = yf.download(scriplist[i], start=startDate, end=stopDate)
                except ConnectionError as e:
                    print(e)
                val = None
                for j in range(0,2):
                    if a[j] == "MA":
                        MA(int(b[0]))
                        if j == 1:
                            MA(int(b[1]))
                            val = signalGenearation(scriplist[i],str(a[0])+str(b[0]),str(a[1])+str(b[1]),response.POST.get('targetper'), response.POST.get('stoploss'),
                                                        response.POST.get('quantityLots'))
                            alldata.append(val)
                    elif a[j] == "EMA":
                        EMA(int(b[0]))
                        if j == 1:
                            EMA(int(b[1]))
                            val = signalGenearation(scriplist[i], str(a[0]) + str(b[0]),
                                                        str(a[1]) + str(b[1]), response.POST.get('targetper'),
                                                        response.POST.get('stoploss'),
                                                        response.POST.get('quantityLots'))
                            alldata.append(val)
                    elif a[j] == "WMA":
                        WMA(int(b[0]))
                        if j == 1:
                            WMA(int(b[1]))
                            val = signalGenearation(scriplist[i], str(a[0]) + str(b[0]), str(a[1]) + str(b[1]),
                                                    response.POST.get('targetper'), response.POST.get('stoploss'),
                                                    response.POST.get('quantityLots'))
                            alldata.append(val)
                    elif a[j] == "RSI":
                        RSI(int(b[0]))
                        if j == 1:
                            RSI(int(b[1]))
                            val = signalGenearation(scriplist[i], str(a[0]) + str(b[0]), str(a[1]) + str(b[1]),
                                                    response.POST.get('targetper'), response.POST.get('stoploss'),
                                                    response.POST.get('quantityLots'))
                            alldata.append(val)
                    elif a[j] == "Value":
                        Value(int(b[0]))
                        if j == 1:
                            Value(int(b[1]))
                            val = signalGenearation(scriplist[i], str(a[0]) + str(b[0]), str(a[1]) + str(b[1]),
                                                    response.POST.get('targetper'), response.POST.get('stoploss'),
                                                    response.POST.get('quantityLots'))
                            alldata.append(val)

            return render(response, 'Strategify/backtestHistory.html',{'data':alldata,'strategyName':response.POST.get('strategyname'),'startDate':startDate,'stopDate':stopDate})
    except Exception as e:
        print(e)

def Value(period):
    data['Value{}'.format(period)] = period

def MA(period):
    global data
    try:
        data = data.apply(lambda x: x.fillna(x.value_counts().index[0]))
        data['MA{}'.format(period)] = data['Close'].rolling(window=period).mean()
    except Exception as e:
        print(e)

def EMA(days):
    global data
    data = data.apply(lambda x: x.fillna(x.value_counts().index[0]))
    col = 'Close'
    start = 0
    if data.shape[0] > days:
        multiplier = 2 / (days + 1)
        first_ema = data.iloc[:days, data.columns.get_loc(col)].sum(axis=0) / days
        data['EMA{}'.format(days)] = np.nan
        data['EMA{}'.format(days)][days - 1] = first_ema
        for i in range(days, (data.shape[0])):
            EMA = data.iloc[i, data.columns.get_loc(col)] * multiplier + data.iloc[
                (i - 1), data.columns.get_loc("EMA{}".format(days))] * (1 - multiplier)
            data['EMA{}'.format(days)][i] = EMA
            start = start + 1
    else:
        print("Not Sufficient data to calculate {}-days EMA".format(days))


def WMA(period):
    global data
    column = 'Close'
    weights = np.arange(1, period + 1)
    wmas = data[column].rolling(period).apply(lambda x: np.dot(x, weights) /weights.sum(), raw=True).to_list()
    data[f'WMA{period}'] = wmas

def RSI(period):
    ret = data['Close'].diff()
    up = []
    down = []
    for i in range(len(ret)):
        if ret[i] < 0:
            up.append(0)
            down.append(ret[i])
        else:
            up.append(ret[i])
            down.append(0)
    up_series = pd.Series(up)
    down_series = pd.Series(down).abs()
    up_ewm = up_series.ewm(com=period - 1, adjust=False).mean()
    down_ewm = down_series.ewm(com=period - 1, adjust=False).mean()
    rs = up_ewm / down_ewm
    rsi = 100 - (100 / (1 + rs))
    rsi_df = pd.DataFrame(rsi).rename(columns={0: 'rsi'}).set_index(data['Close'].index)
    rsi_df = rsi_df.dropna()
    data['RSI{}'.format(period)] = rsi_df[3:]


def signalGenearation(scrip,period1,period2,target,steploss,quantity):
    global data
    data['Signal'] = np.where(data['{}'.format(period1)] > data['{}'.format(period2)], 1, 0)
    data['Position'] = data['Signal'].diff()
    return ProfitLossCalculation(scrip,period1,period2,target,steploss,quantity)


def ProfitLossCalculation(scrip,period1,period2,target,steploss,quantity):
    global data
    a = 0
    status = 0
    WinsCount = 0
    LossCount = 0
    totP = 0
    totL = 0
    balance = 0
    enter = 0
    alllist = []
    PS = 0
    PL = 0
    streakP = 0
    streakL = 0

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
                    PS += 1
                    PL = 0
                    if PS > streakP:
                        streakP = PS
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
                    PL += 1
                    PS = 0
                    if PL > streakL:
                        streakL = PL
                    a = 0
                    enter = 0

    print("Balance: ",balance," Total Wins: ",WinsCount," Total Loss: ",LossCount," Total Profit:  ", totP," Total Loss: ",totL)

    if totP + totL > 0:
        status = 1

    pd.DataFrame(alllist).to_csv('Strategify/static/'+scrip.replace('.NS', '')+'.csv')
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
    plt.plot(data['{}'.format(period1)], alpha=1, label='shortAvg', color="green")
    plt.plot(data['{}'.format(period2)], alpha=1, label='longAvg', color="red")
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
        'WinStreak': streakP,
        'LossStreak': streakL,
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