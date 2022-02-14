import requests


class NSE:
    def __init__(self):
        self.header = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                          'Chrome/97.0.4692.99 Safari/537.36'}
        self.session = requests.Session()
        self.session.get('http://nseindia.com', headers=self.header)

    def marketstatus(self):
        return self.session.get(f"https://www1.nseindia.com//emerge/homepage/smeNormalMktStatus.json",
                                   headers=self.header).json()


    def allscrip(self):
        data = self.session.get(f"https://www1.nseindia.com/homepage/peDetails.json",
                                   headers=self.header).json()
        allscrip = []

        for key in data.keys():
            allscrip.append(str(key)+".NS")
            
        return allscrip
