from django.http import JsonResponse
from django.shortcuts import render
from .StockData import *
import pandas as pd
import numpy as np
import yfinance as yf
from .models import *
from datetime import *
from django.core.mail import send_mail
import math, random
from django.core.exceptions import *
from django.db import *
from django.http import HttpResponse
from django.template.loader import render_to_string
from .updatestrategy import *
from .constants import *
from django.contrib import messages
from .profitlosscalculation import *

data = None


def home(response):
    return render(response, 'Strategify/index.html', {})


def registration(request):
    return render(request, 'Strategify/registrationPage.html', {})


def stockdata(request):
    response_data = {}
    try:
        nse = NSE()
        response_data['success'] = nse.getscripdata(request.POST.get('scripname'), request.POST.get('fromdate'),
                                                    request.POST.get('enddate'))
        return JsonResponse(response_data)
    except Exception as e:
        response_data['success'] = str(e)
        print(STOCK_DATA_ERROR, e)
        return JsonResponse(response_data)


def charts(request):
    response_data = {}
    data = UserRegistration.objects.get(username=request.session['username'])
    allscrip = []
    try:
        nse = NSE()
        allscrip = nse.allscrip()
    except Exception as e:
        print("Connection Error NSE: ", e)
        response_data['error'] = CONNECTION_ERROR

    userData = {
        'username': request.session['username'],
        'name': data.name,
        'allscripname': allscrip,
    }
    return render(request, 'Strategify/charts.html', {'data': userData, 'status': response_data})


def signup(request):
    response_data = {}
    if request.method == 'POST':
        if request.POST.get('otp') == str(request.session['otp']):
            try:
                UserRegistration.objects.create(
                    username=request.POST.get('username'),
                    name=request.POST.get('name'),
                    email=request.POST.get('email'),
                    phone=request.POST.get('phone'),
                    password=request.POST.get('password'),
                )
                response_data['success'] = ACCOUNT_CREATED
                return JsonResponse(response_data)
            except IntegrityError as e:
                print("Error Account Creating: " + str(e))
                response_data['error'] = ALREADY_ACCOUNT_CREATED
            except Exception as e:
                print("Error Account Creating: " + str(e))
                response_data['error'] = str(e)
                return JsonResponse(response_data)
        else:
            print(INCORRECT_OTP)
            response_data['error'] = INCORRECT_OTP
            return JsonResponse(response_data)
    return JsonResponse(response_data)


def checkUsername(request):
    response_data = {}
    if request.method == 'POST':
        username = request.POST.get('username')
        try:
            if UserRegistration.objects.filter(username=username).exists():
                response_data['success'] = AVAILABLE
            else:
                response_data['error'] = NOT_AVAILABLE
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
        'username': request.session['username'],
        'name': data.name,
    }
    return render(request, 'Strategify/deployed.html', {'data': userData})


def tradingviewsetup(request):
    return render(request, 'Strategify/deployed.html', {})


def generateotp(request):
    response_data = {}
    email = request.POST.get("email")
    try:
        otp = generateOTP()
        request.session['otp'] = otp
        print(otp)
        htmlgen = '<p>Dear Customer, We thank you for registration at Strategify.</p><br><p>Your OTP is <strong>' + otp + '</strong></p>'
        # send_mail('OTP request', otp, 'Strategify', [email], fail_silently=False, html_message=htmlgen)
        print("OTP has been SENT")
        response_data['success'] = OTP_SENT
    except Exception as e:
        print("Error OTP sending: " + str(e))
        response_data['error'] = str(e)
        return JsonResponse(response_data)
    return JsonResponse(response_data)


def signIn(request):
    response_data = {}
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        try:
            user_data = UserRegistration.objects.get(username=username, password=password)
            if (user_data):
                response_data['success'] = LOGGED_IN
                request.session['username'] = user_data.username
                dashboard(request)
            else:
                response_data['error'] = INVALID_LOGIN
        except ObjectDoesNotExist as e:
            response_data['error'] = INVALID_LOGIN
        except Exception as e:
            response_data['error'] = str(e)
        return JsonResponse(response_data)


def contactus(response):
    return render(response, 'Strategify/contactus.html', {})


def profilepage(response):
    return render(response, 'Strategify/profilePage.html', {})


def allindices(request):
    data = UserRegistration.objects.get(username=request.session['username'])
    userData = {
        'username': request.session['username'],
        'name': data.name,
    }
    return render(request, 'Strategify/allindices.html', {'data': userData})


def checkstrategyName(request):
    response_data = {}
    if request.method == 'POST':
        try:
            if StrategyRegistration.objects.filter(username=request.session['username'],
                                                   strategyname=request.POST.get('strategyname')).exists():
                response_data['success'] = AVAILABLE
            else:
                response_data['error'] = NOT_AVAILABLE
        except ObjectDoesNotExist as e:
            response_data['success'] = AVAILABLE
        except Exception as e:
            response_data['error'] = str(e)
        return JsonResponse(response_data)


def openStrategy(request):
    response_data = {}
    showStrategyDetails(request)
    data = UserRegistration.objects.get(username=request.session['username'])
    strategydata = None

    try:
        if request.method == "GET":
            strategydata = StrategyRegistration.objects.get(strategyid=request.GET.get('strategyid'))
        # nse = NSE()
        userData = {
            'username': request.session['username'],
            'name': data.name,
            'scripdata': "nse.allscrip()",
        }
        return render(request, 'Strategify/createStrategy.html',
                      {'data': userData, 'strategydata': strategydata, 'status': response_data})
    except BrokenPipeError as e:
        print("Connection Error NSE: ", e)
        response_data['error'] = BROKEN_PIPE_ERROR
        return render(request, 'Strategify/createStrategy.html', {'status': response_data})
    except ConnectionError as e:
        print("Connection Error NSE: ", e)
        response_data['error'] = CHECK_CONNECTION
        return render(request, 'Strategify/createStrategy.html', {'status': response_data})
    except Exception as e:
        print("Connection Error NSE: ", e)
        response_data['error'] = str(e)
        return render(request, 'Strategify/createStrategy.html', {'status': response_data})


def deletestrategy(request):
    response_data = {}
    if request.method == "GET":
        try:
            StrategyRegistration.objects.get(
                strategyid=str(request.session['username']) + str(request.GET.get('strategyname'))).delete()
            print("Deleted Sucess")
            return HttpResponse(dashboard(request))
        except ObjectDoesNotExist as e:
            response_data['error'] = str(e)
            rendered = render_to_string('Strategify/error.html', {'error': str(e)})
            return HttpResponse(rendered)
        except Exception as e:
            response_data['error'] = str(e)
            rendered = render_to_string('Strategify/error.html', {'error': str(e)})
            return HttpResponse(rendered)


def createstrategy(request):
    print(request)
    data = UserRegistration.objects.get(username=request.session['username'])

    # try:
    #     nse = NSE()
    # except Exception as e:
    #     print("Connection Error NSE: ",e)
    #     response_data['error'] = "Unable to Load"
    #     return JsonResponse(response_data)
    userData = {
        'username': request.session['username'],
        'name': data.name,
        'scripdata': "nse.allscrip()",
    }
    return render(request, 'Strategify/createStrategy.html', {'data': userData, 'strategydata': None})


def deploystrategy(request):
    response_data = {}
    scriplist = request.POST.get('allscriplist').split("/")
    strategyname = scriplist[0]
    scriplist = scriplist[:-1]
    strategyid = StrategyRegistration.objects.get(strategyid=request.session['username'] + strategyname)
    user = UserRegistration.objects.get(username=request.session['username'])

    for i in range(1, len(scriplist)):
        try:
            Deploy.objects.create(
                deployid=request.session['username'] + "/" + strategyname + "/" + scriplist[i],
                strategyid=strategyid,
                username=user,
                scripname=scriplist[i],
                deploytime=date.today().strftime('%Y-%m-%d'),
                algocycles=request.POST.get('algocycles'),
            )
            response_data['success'] = DEPLOYED_SUCCESS
        except Exception as e:
            print("Depoy Error: ",str(e))
            response_data['success'] = ERROR_OCCURRED

    print(response_data)
    return JsonResponse(response_data)


def topgainers():
    response_data = {}
    try:
        nse = NSE()
        response_data['success'] = nse.topgainers()
        return JsonResponse(response_data)
    except ConnectionError as e:
        response_data['error'] = FAILED_TO_LOAD
        print("Connection Error: ", e)
        return JsonResponse(response_data)
    except Exception as e:
        print("Top Gainers Error: ", str(e))
        response_data['error'] = FAILED_TO_LOAD
        return JsonResponse(response_data)


def toplosers():
    response_data = {}
    try:
        nse = NSE()
        response_data['success'] = nse.toplosers()
        return JsonResponse(response_data)
    except ConnectionError as e:
        response_data['error'] = FAILED_TO_LOAD
        print("Connection Error: ", e)
        return JsonResponse(response_data)
    except Exception as e:
        print("Top Losers Error: ", str(e))
        response_data['error'] = FAILED_TO_LOAD
        return JsonResponse(response_data)


def indexdata():
    response_data = {}
    try:
        nse = NSE()
        response_data['success'] = nse.allindex()
        return JsonResponse(response_data)
    except ConnectionError as e:
        print("Connection Error: ", e)
    except Exception as e:
        print("Top Losers Error: ", str(e))
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
        strategydata = {
            'strategyname': i.strategyname,
            'quantity': i.quantity,
            'scripname': i.scripname,
            'entrycondition': i.entrycondition,
            'stoploss': i.stoploss,
            'target': i.target,
            'exitcondition': i.exitcondition,
            'startdate': i.startdate,
            'enddate': i.enddate,
            'createDate': convertTime(start - ends),
        }
        allstrategydata.append(strategydata)
    return render(response, 'Strategify/dashboard.html', {'data': userData, 'strategydata': allstrategydata})


def convertTime(time):
    time = str(time).split(":")
    if (time[0] == "0" and time[1] == "00" and time[2] == "00"):
        return "0 sec ago"
    elif time[0] == "0" and time[1] == "00" and time[2] != "00":
        return str(time[2]) + " sec ago"
    elif time[0] == "0" and time[1] != "00":
        return str(time[1]) + " min ago"
    elif time[0] != "0":
        return str(time[0]) + " hours ago"
    else:
        print(ERROR)


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
                a = response.POST.get("entryfirindicator" + str(j))
                b = response.POST.get("entrysecindicator" + str(j))
                c = response.POST.get("entrycomparator" + str(j))

                if ((a and b and c) != None):
                    tempCondition.append(a)
                    tempCondition.append(c)
                    tempCondition.append(b)
                    entryCondition.append(tempCondition)
                    dataentryCondition += str(a) + "-" + str(b) + "-" + str(c) + "/"
                j += 1
            j = 1
            for i in response.POST:
                tempCondition = []
                a = response.POST.get("exitfirindicator" + str(j))
                b = response.POST.get("exitsecindicator" + str(j))
                c = response.POST.get("exitcomparator" + str(j))

                if ((a and b and c) != None):
                    tempCondition.append(a)
                    tempCondition.append(c)
                    tempCondition.append(b)
                    exitCondition.append(tempCondition)
                    dataexitCondition += str(a) + "-" + str(b) + "-" + str(c) + "/"
                j += 1

            startDate = response.POST.get('startDate')
            stopDate = response.POST.get('stopDate')
            scriplist = response.POST.get('allscriplist')
            scriplist = scriplist.split(",")
            alldata = []
            for i in range(0, len(scriplist) - 1):
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

                    for j in range(0, 2):
                        globals()[a[j]]("ENTRY", int(b[0]))
                        if j == 1:
                            globals()[a[j]]("ENTRY", int(b[1]))
                            entrySignalGeneration(str(a[0]) + str(b[0]), str(a[1]) + str(b[1]))

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
                    val = ProfitLossCalculationWithExit(data, response.session['username'], scriplist[i],
                                                        response.POST.get('targetper'), response.POST.get('stoploss'),
                                                        response.POST.get('quantityLots'))
                else:
                    val = ProfitLossCalculationWithoutExit(data, response.session['username'], scriplist[i],
                                                           response.POST.get('targetper'),
                                                           response.POST.get('stoploss'),
                                                           response.POST.get('quantityLots'))
                alldata.append(val)

            if dataexitCondition == "":
                dataexitCondition = "None"
            try:
                updateStrategyData(response, dataentryCondition, dataexitCondition)
            except IntegrityError as e:
                response_data['error'] = STRATEGY_ALREADY_EXIT
            except Exception as e:
                response_data['error'] = str(e)
            return render(response, 'Strategify/backtestHistory.html',
                          {'response': response, 'data': alldata, 'strategyName': response.POST.get('strategyname'),
                           'error': response_data})
    except Exception as e:
        print("Error", e)


def Value(condition, period):
    global data
    data['{}Value{}'.format(condition, period)] = period


def Close(condition, period):
    global data
    data['{}Close{}'.format(condition, period)] = data['Close']


def MA(condition, period):
    global data
    try:
        data['{}MA{}'.format(condition, period)] = data['Close'].rolling(window=period).mean()
    except Exception as e:
        print("Error MA: ", e)


def EMA(condition, days):
    global data
    data['{}EMA{}'.format(condition, days)] = data['Close'].ewm(span=days, adjust=False).mean();


def WMA(condition, period):
    global data
    weights = np.arange(1, period + 1)
    wmas = data['Close'].rolling(period).apply(lambda x: np.dot(x, weights) / weights.sum(), raw=True).to_list()
    data['{}WMA{}'.format(condition, period)] = wmas


def RSI(condition, period):
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
    data['{}RSI{}'.format(condition, period)] = rsi_df[3:]


def entrySignalGeneration(period1, period2):
    global data
    data['EntrySignal'] = np.where(data['ENTRY{}'.format(period1)] > data['ENTRY{}'.format(period2)], 1, 0)
    data['ENTRYPosition{}'.format(str(period1) + str(period2))] = data['EntrySignal'].diff()
    x = data['ENTRYPosition{}'.format(str(period1) + str(period2))]
    data.loc[data['Position'] != 1.0, ['Position']] = data['ENTRYPosition{}'.format(str(period1) + str(period2))]
    data['Position'] = data['Position'].replace([-1.0], [0.0])


def myfunc(position, exit):
    if position != -1.0:
        if position == 1.0 and exit == -1.0:
            position = 0.0
        elif position == 1.0:
            position = 1.0
        else:
            position = exit
    return position

def exitSignalGeneration(period1, period2):
    global data
    data['ExitSignal'] = np.where(data['EXIT{}'.format(period1)] > data['EXIT{}'.format(period2)], 0, 1)
    data['EXITPosition{}'.format(str(period1) + str(period2))] = data['ExitSignal'].diff()
    data['Position'] = data.apply(
        lambda x: myfunc(x['Position'], x['EXITPosition{}'.format(str(period1) + str(period2))]), axis=1)


def admincode(request):
    return render(request, 'Strategify/admincode.html', {})
