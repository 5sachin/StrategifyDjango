from datetime import datetime
from datetime import timedelta

def subtarctdays(startdate,days):
    date_format = '%Y-%m-%d'
    dtObj = datetime.strptime(startdate, date_format)
    past_date = dtObj - timedelta(days=days)
    past_date_str = past_date.strftime(date_format)
    return past_date


def extractMaximum(ss):
    num, res = 0, 0
    for i in range(len(ss)):
        if ss[i] >= "0" and ss[i] <= "9":
            num = num * 10 + int(int(ss[i]) - 0)
        else:
            res = max(res, num)
            num = 0
          
    return max(res, num)