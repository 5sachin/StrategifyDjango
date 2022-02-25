from django.http import JsonResponse
from django.shortcuts import render
from .StockData import *
import pandas as pd
import numpy as np
import io
import yfinance as yf
import base64
import matplotlib.pyplot as plt
from .models import *
import datetime
from django.core.mail import send_mail
import math, random
from django.core.exceptions import *
from django.db import *

plt.style.use('fivethirtyeight')
data = None
USERNAME = None

def home(response):
    return render(response, 'Strategify/index.html',{})

def registration(request):
    return render(request, 'Strategify/registrationPage.html', {})


def stockdata(request):
    response_data = {}
    try:
        nse = NSE()
        scrip = request.POST.get('scripname');
        response_data['success'] = nse.getscripdata(scrip,"22-11-2021","22-02-2022")
        return JsonResponse(response_data)
    except Exception as e:
        response_data['success'] = str(e)
        print("Error: ",e)
        return JsonResponse(response_data)



def charts(request):
    data = UserRegistration.objects.get(username=request.session['username'])
    allscrip = []
    try:
        nse = NSE()
        allscrip = nse.allscrip()
    except Exception as e:
        print("Connection Error NSE: ",e)
        response_data['error'] = "Unable to Load"
        return JsonResponse(response_data)
        
    userData = {
    'username': request.session['username'],
    'name': data.name,
    'allscripname':allscrip,
    }
    return render(request,'Strategify/charts.html', {'data':userData})

def signup(request):
    response_data = {}
    if request.method == 'POST':
        username = request.POST.get('username')
        name = request.POST.get('name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        password = request.POST.get('password')

        if request.POST.get('otp')==str(request.session['otp']):
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
            except IntegrityError as e:
                print("Error Account Creating: "+str(e))
                response_data['error'] = str("Already Account Created")
            except Exception as e:
                print("Error Account Creating: "+str(e))
                response_data['error'] = str(e)
                return JsonResponse(response_data)
        else:
            print("Incorrect OTP")
            response_data['error'] = "Incorrect OTP"
            return JsonResponse(response_data)

    return JsonResponse(response_data)

def checkUsername(request):
    response_data = {}
    if request.method == 'POST':
        username = request.POST.get('username')
        try:
            if UserRegistration.objects.filter(username=username).exists():
                response_data['success'] = "Availiable"
            else:
                response_data['error'] = "Not Available"
        except Exception as e:
            response_data['error'] = str(e)
        return JsonResponse(response_data)

def generateOTP():
    digits = "0123456789"
    OTP = ""
    for i in range(4):
        OTP += digits[math.floor(random.random() * 10)]
    return OTP

def deploypage(request):
    data = UserRegistration.objects.get(username=request.session['username'])
    userData = {
        'username': USERNAME,
        'name': data.name,
    }
    return render(request, 'Strategify/deployed.html', {'data': userData})

def generateotp(request):
    response_data = {}
    email = request.POST.get("email")
    try:
        otp = generateOTP()
        request.session['otp'] = otp
        print(otp)
        htmlgen = '<p>Dear Customer, We thank you for registration at Strategify.</p><br><p>Your OTP is <strong>'+otp+'</strong></p>'
        # send_mail('OTP request', otp, 'Strategify', [email], fail_silently=False, html_message=htmlgen)
        print("OTP has been SENT")
        response_data['success'] = "OTP has been sent."
    except Exception as e:
        print("Error OTP sending: "+str(e))
        response_data['error'] = str(e)
        return JsonResponse(response_data)
    return JsonResponse(response_data)

def signIn(request):
    global USERNAME
    response_data = {}
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        try:
            user_data = UserRegistration.objects.get(username=username,password=password)
            if(user_data):
                response_data['success'] = "Logged In Success"
                USERNAME = username
                request.session['username'] = user_data.username
                dashboard(request)
            else:
                response_data['error'] = "Invalid Login"
        except ObjectDoesNotExist as e:
            response_data['error'] = "Invalid Login"
        except Exception as e:
            response_data['error'] = str(e)
        return JsonResponse(response_data)

def contactus(response):
    return render(response, 'Strategify/contactus.html', {})

def profilepage(response):
    return render(response, 'Strategify/profilePage.html', {})

def checkstrategyName(request):
    response_data = {}
    if request.method == 'POST':
        try:
            if StrategyRegistration.objects.filter(username=request.session['username'],strategyname=request.POST.get('strategyname')).exists():
                response_data['success'] = "Availiable"
            else:
                response_data['error'] = "Not Available"
        except ObjectDoesNotExist as e:
            response_data['success'] = "Availiable"
        except Exception as e:
            response_data['error'] = str(e)
        return JsonResponse(response_data)

def openStrategy(response):
    response_data = {}
    showStrategyDetails(response)
    data = UserRegistration.objects.get(username=response.session['username'])

    strategydata = None
    if response.method == "GET":
        strategydata = StrategyRegistration.objects.get(strategyid=response.GET.get('strategyid'))

    try:
        nse = NSE()
    except Exception as e:
        print("Connection Error NSE: ", e)
        response_data['error'] = "Unable to Load"
        return JsonResponse(response_data)
    userData = {
        'username': USERNAME,
        'name': data.name,
        'scripdata': nse.allscrip(),
    }
    return render(response, 'Strategify/createStrategy.html', {'data': userData, 'strategydata': strategydata})

def createstrategy(response):
    response_data = {}
    showStrategyDetails(response)
    data = UserRegistration.objects.get(username=response.session['username'])

    # try:
    #     nse = NSE()
    # except Exception as e:
    #     print("Connection Error NSE: ",e)
    #     response_data['error'] = "Unable to Load"
    #     return JsonResponse(response_data)
    userData = {
        'username': USERNAME,
        'name': data.name,
        'scripdata': "nse.allscrip()",
    }
    return render(response, 'Strategify/createStrategy.html', {'data':userData,'strategydata': None})


def topgainers(response):
    response_data = {}
    try:
        nse = NSE()
        response_data['success'] = nse.topgainers()
        return JsonResponse(response_data)
    except ConnectionError as e:
        print("Connection Error: ",e)
    except Exception as e:
        print("Top Gainers Error: ",str(e))
        response_data['error'] = str(e)
        return JsonResponse(response_data)

def toplosers(response):
    response_data = {}
    try:
        nse = NSE()
        response_data['success'] = nse.toplosers()
        return JsonResponse(response_data)
    except ConnectionError as e:
        print("Connection Error: ",e)
    except Exception as e:
        print("Top Losers Error: ",str(e))
        response_data['error'] = str(e)
        return JsonResponse(response_data)

def indexdata(response):
    response_data = {}
    try:
        nse = NSE()
        response_data['success'] = nse.allindex()
        return JsonResponse(response_data)
    except ConnectionError as e:
        print("Connection Error: ",e)
    except Exception as e:
        print("Top Losers Error: ",str(e))
        response_data['error'] = str(e)
        return JsonResponse(response_data)


def dashboard(response):
    data = UserRegistration.objects.get(username=response.session['username'])
    userData = {
    'username': response.session['username'],
    'name': data.name,
    }

    allstrategydata = []
    for i in showStrategyDetails(response):
        current = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        ends = datetime.datetime.strptime(i.createDate, '%Y-%m-%d %H:%M:%S')
        start = datetime.datetime.strptime(current, '%Y-%m-%d %H:%M:%S')
        strategydata={
            'strategyname':i.strategyname,
            'quantity':i.quantity,
            'scripname':i.scripname,
            'entrycondition':i.entrycondition,
            'stoploss':i.stoploss,
            'target':i.target,
            'exitcondition':i.exitcondition,
            'startdate':i.startdate,
            'enddate':i.enddate,
            'createDate':convertTime(start-ends),
        }
        allstrategydata.append(strategydata)
    return render(response,'Strategify/dashboard.html', {'data':userData,'strategydata':allstrategydata})



def convertTime(time):
    time = str(time).split(":")
    if (time[0] == "0" and time[1] == "00" and time[2] == "00"):
        return "0 sec ago"
    elif time[0] == "0" and time[1] == "00" and time[2] != "00":
        return str(time[2])+" sec ago"
    elif time[0] == "0" and time[1] != "00":
        return str(time[1])+" min ago"
    elif time[0] != "0":
        return str(time[0])+" hours ago"
    else:
        print("Error")

def showStrategyDetails(response):
    data = StrategyRegistration.objects.filter(username=response.session['username'])
    return data

def createStrategyForm(response):
    global data
    entryCondition = []
    exitCondition = []
    response_data = {}
    dataentryCondition = ""
    dataexitCondition = ""
    try:
        if response.method == "POST":
            j = 1
            for i in response.POST:
                tempCondition = []
                a = response.POST.get("entryfirindicator"+str(j))
                b = response.POST.get("entrysecindicator"+str(j))
                c = response.POST.get("entrycomparator" + str(j))
                
                if((a and b and c) != None):
                    tempCondition.append(a)
                    tempCondition.append(c)
                    tempCondition.append(b)
                    entryCondition.append(tempCondition)
                    dataentryCondition += str(a)+"-"+str(b)+"-"+str(c)+"/"
                j +=1
            j = 1
            for i in response.POST:
                tempCondition = []
                a = response.POST.get("exitfirindicator"+str(j))
                b = response.POST.get("exitsecindicator"+str(j))
                c = response.POST.get("exitcomparator" + str(j))
                
                if((a and b and c) != None):
                    tempCondition.append(a)
                    tempCondition.append(c)
                    tempCondition.append(b)
                    exitCondition.append(tempCondition)
                    dataexitCondition += str(a) + "-" + str(b) + "-" + str(c) + "/"
                j +=1

            startDate = response.POST.get('startDate')
            stopDate = response.POST.get('stopDate')
            scriplist = response.POST.get('allscriplist')
            scriplist = scriplist.split(",")
            alldata = []
            for i in range(0,len(scriplist)-1):
                try:
                    data = yf.download(scriplist[i], start=startDate, end=stopDate)
                    data['Position'] = None
                except ConnectionError as e:
                    print(e)

                for k in range(len(entryCondition)):
                    a = entryCondition[k][0].split(",")
                    b = entryCondition[k][2].split(",")
                    x = b[0]
                    b[0] = a[1]
                    a[1] = x

                    for j in range(0,2):
                        globals()[a[j]]("ENTRY", int(b[0]))
                        if j == 1:
                            globals()[a[j]]("ENTRY", int(b[1]))
                            entrySignalGeneration(str(a[0])+str(b[0]), str(a[1])+str(b[1]))

                if exitCondition:
                    for k in range(len(exitCondition)):
                        a = exitCondition[k][0].split(",")
                        b = exitCondition[k][2].split(",")
                        x = b[0]
                        b[0] = a[1]
                        a[1] = x
                        for j in range(0, 2):
                            globals()[a[j]]("EXIT", int(b[0]))
                            if j == 1:
                                globals()[a[j]]("EXIT", int(b[1]))
                                exitSignalGeneration(str(a[0]) + str(b[0]), str(a[1]) + str(b[1]))
                if exitCondition:
                    val = ProfitLossCalculationWithExit(response.session['username'],scriplist[i],response.POST.get('targetper'),response.POST.get('stoploss'),response.POST.get('quantityLots'))
                else:
                    val = ProfitLossCalculationWithoutExit(response.session['username'],scriplist[i], response.POST.get('targetper'),response.POST.get('stoploss'),response.POST.get('quantityLots'))
                alldata.append(val)

            if dataexitCondition == "":
                dataexitCondition = "None"
            try:
                insertStrategyData(response,dataentryCondition,dataexitCondition)
            except IntegrityError as e:
                response_data['error'] = "Strategy Name Already Exist Hence Not Saved. Use different Name"
            except Exception as e:
                response_data['error'] = str(e)
            return render(response, 'Strategify/backtestHistory.html',{'response':response,'data':alldata,'strategyName':response.POST.get('strategyname'),'error':response_data})
    except Exception as e:
        print("Error",e)


def insertStrategyData(response,dataentryCondition,dataexitCondition):
    try:
        if StrategyRegistration.objects.filter(username=response.session['username'],strategyid=response.session['username'] + response.POST.get('strategyname')).exists():
            user = UserRegistration.objects.get(username=response.session['username'])
            StrategyRegistration.objects.filter(strategyid = response.session['username'] + response.POST.get('strategyname')).update(
                strategyid=response.session['username'] + response.POST.get('strategyname'),
                username=user,
                strategyname=response.POST.get('strategyname'),
                quantity=response.POST.get('quantityLots'),
                scripname=response.POST.get('allscriplist'),
                entrycondition=dataentryCondition,
                stoploss=response.POST.get('stoploss'),
                target=response.POST.get('targetper'),
                exitcondition=dataexitCondition,
                startdate=response.POST.get('startDate'),
                enddate=response.POST.get('stopDate'),
                createDate=datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                )
        else:
            saveStrategyDetails(response,dataentryCondition,dataexitCondition)
    except ObjectDoesNotExist as e:
        saveStrategyDetails(response,dataentryCondition,dataexitCondition)

def saveStrategyDetails(response,dataentryCondition,dataexitCondition):
    user = UserRegistration.objects.get(username=response.session['username'])
    StrategyRegistration.objects.create(
            strategyid=response.session['username'] + response.POST.get('strategyname'),
            username=user,
            strategyname=response.POST.get('strategyname'),
            quantity=response.POST.get('quantityLots'),
            scripname=response.POST.get('allscriplist'),
            entrycondition=dataentryCondition,
            stoploss=response.POST.get('stoploss'),
            target=response.POST.get('targetper'),
            exitcondition=dataexitCondition,
            startdate=response.POST.get('startDate'),
            enddate=response.POST.get('stopDate'),
            createDate=datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            )

def Value(period):
    data['Value{}'.format(period)] = period

def MA(condition,period):
    global data
    try:
        data['{}MA{}'.format(condition,period)] = data['Close'].rolling(window=period).mean()
    except Exception as e:
        print("Error Line 200",e)

def EMA(condition,days):
    global data
    data['{}EMA{}'.format(condition,days)] = data['Close'].ewm(span=days, adjust=False).mean();

def WMA(condition,period):
    global data
    column = 'Close'
    weights = np.arange(1, period + 1)
    wmas = data[column].rolling(period).apply(lambda x: np.dot(x, weights) /weights.sum(), raw=True).to_list()
    data[f'{condition}WMA{period}'] = wmas

def RSI(condition,period):
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
    data['{}RSI{}'.format(condition,period)] = rsi_df[3:]

def entrySignalGeneration(period1,period2):
    global data
    data['EntrySignal'] = np.where(data['ENTRY{}'.format(period1)] > data['ENTRY{}'.format(period2)], 1, 0)
    data['ENTRYPosition{}'.format(str(period1)+str(period2))] = data['EntrySignal'].diff()


    for i in range(0, len(data['ENTRYPosition{}'.format(str(period1)+str(period2))])):
        if data['Position'][i] != 1.0:
            data['Position'][i] = data['ENTRYPosition{}'.format(str(period1)+str(period2))][i]
    data['Position'] = data['Position'].replace([-1.0],[0.0])

def exitSignalGeneration(period1,period2):
    global data
    data['ExitSignal'] = np.where(data['EXIT{}'.format(period1)] > data['EXIT{}'.format(period2)], 0, 1)
    data['EXITPosition{}'.format(str(period1)+str(period2))] = data['ExitSignal'].diff()

    for i in range(0, len(data['EXITPosition{}'.format(str(period1)+str(period2))])):
        if data['Position'][i] != -1.0:
            if data['Position'][i] == 1.0 and data['EXITPosition{}'.format(str(period1)+str(period2))][i] == -1.0:
                data['Position'][i] = 0.0
            elif data['Position'][i] == 1.0:
                data['Position'][i] = 1.0
            else:
                data['Position'][i] = data['EXITPosition{}'.format(str(period1)+str(period2))][i]

def ProfitLossCalculationWithExit(username,scrip,target,steploss,quantity):
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
            print("Buy:    Date: ", data.index[i], " Price: ", a)
        elif data['Position'][i] == -1.0 and enter == 1:
            balance += data['Close'][i] - a
            if data['Close'][i]-a >= 0:
                print("Sell:   Profit  Price: ", data['Close'][i], " Date: ", data.index[i], " Net Profit: ",
                      data['Close'][i] - a)
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
            else:
                print("Sell:   Loss   Price: ", data['Close'][i], " Date: ", data.index[i], " Net Loss: ",
                      data['Close'][i] - a)
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
        else:
            if a > 0 and enter == 1:
                if ((data['Close'][i] - a) / a) * 100 >= int(target):
                    balance += data['Close'][i] - a
                    print("Sell:   Profit  Price: ", data['Close'][i], " Date: ", data.index[i], " Net Profit: ",
                          data['Close'][i] - a)
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
                    print("Sell:   Loss   Price: ", data['Close'][i], " Date: ", data.index[i], " Net Loss: ",
                          data['Close'][i] - a)
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

    print("Balance: ", balance, " Total Wins: ", WinsCount, " Total Loss: ", LossCount, " Total Profit:  ", totP,
          " Total Loss: ", totL)

    if totP + totL > 0:
        status = 1

    pd.DataFrame(alllist).to_csv('Strategify/static/' + ''+username+''+scrip.replace('.NS', '')+'.csv')
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
    # plt.plot(data['{}'.format(period1)], alpha=1, label='shortAvg', color="green")
    # plt.plot(data['{}'.format(period2)], alpha=1, label='longAvg', color="red")
    plt.xlabel('Date', fontsize=18)
    plt.ylabel('Close Price', fontsize=18)

    buf = io.BytesIO()
    x.savefig(buf, format="png")
    buf.seek(0)
    string = base64.b64encode(buf.read())
    uri = urllib.parse.quote(string)

    percentBar = (float(totP) / (float(totP) + float(totL))) * 100
    alldata = {
        'username': username,
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

def ProfitLossCalculationWithoutExit(username,scrip,target,steploss,quantity):
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
    ltp = 0


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
            print("Buy:    Date: ",data.index[i]," Price: ",a)

        else:
            if a > 0:
                if ((data['Close'][i] - a) / a) * 100 >= int(target):
                    balance += data['Close'][i] - a
                    print("Sell:   Profit  Price: ", data['Close'][i], " Date: ", data.index[i], " Net Profit: ", data['Close'][i] - a)
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
                    print("Sell:   Loss   Price: ", data['Close'][i], " Date: ",data.index[i], " Net Loss: ", data['Close'][i] - a)
                    LossCount += 1
                    totL += data['Close'][i] - a
                    alllist.append({
                        'date': data.index[i],
                        'price': data['Close'][i],
                        'buysell': "sell",
                        'balance': balance
                    })
                    ltp = data['Close'][i]
                    PL += 1
                    PS = 0
                    if PL > streakL:
                        streakL = PL
                    a = 0
                    enter = 0

    print("Balance: ",balance," Total Wins: ",WinsCount," Total Loss: ",LossCount," Total Profit:  ", totP," Total Loss: ",totL)

    if totP + totL > 0:
        status = 1

    pd.DataFrame(alllist).to_csv('Strategify/static/'+''+username+''+scrip.replace('.NS', '')+'.csv')
    periodHigh = "{:.2f}".format(data['Close'].max())
    periodLow = "{:.2f}".format(data['Close'].min())
    balance = "{:.2f}".format(balance)
    totP = "{:.2f}".format(totP)
    totL = "{:.2f}".format(-totL)
    ltp = "{:.2f}".format(float(ltp))



    if WinsCount != 0 and LossCount != 0:
        AvgGain = "{:.2f}".format(float(totP) * int(quantity) / WinsCount)
        AvgLoss = "{:.2f}".format(float(totL) * int(quantity) / LossCount)
    elif WinsCount == 0 and LossCount != 0:
        AvgGain = 0
        AvgLoss = "{:.2f}".format(float(totL) * int(quantity) / LossCount)
    elif LossCount == 0 and WinsCount != 0:
        AvgLoss = 0
        AvgGain = "{:.2f}".format(float(totP) * int(quantity) / WinsCount)
    else:
        AvgGain = 0
        AvgLoss = 0




    x = plt.figure(figsize=(15, 7))
    plt.title('Close Price History w/ Buy & Sell Signals', fontsize=18)
    plt.plot(data['Close'], alpha=0.5, label='Close')
    # plt.plot(data['{}'.format(period1)], alpha=1, label='shortAvg', color="green")
    # plt.plot(data['{}'.format(period2)], alpha=1, label='longAvg', color="red")
    plt.xlabel('Date', fontsize=18)
    plt.ylabel('Close Price', fontsize=18)

    buf = io.BytesIO()
    x.savefig(buf, format="png")
    buf.seek(0)
    string = base64.b64encode(buf.read())
    uri = urllib.parse.quote(string)

    print(type(totP))
    if float(totP) == 0.00 and float(totL) == 0.00:
        print("Here 1")
        percentBar = 0
    else: 
        percentBar = (float(totP) / (float(totP) + float(totL))) * 100
    alldata = {
        'username':username,
        'ScripName': scrip.replace('.NS', ''),
        'PL': "{:.2f}".format(float(balance) * int(quantity)),
        'Status': status,
        'LTP': ltp,
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