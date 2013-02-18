import sys
import requests
from bs4 import BeautifulSoup

class LAFitness:

    URLS = {
        'LOGIN': 'https://www.lafitness.com/Pages/login.aspx',
        'CHECKIN_HISTORY': 'https://www.lafitness.com/Pages/checkinhistory.aspx'
    }

    SESSION_COOKIE = 'ASP.NET_SessionId'

    USERNAME = 'ctl00$MainContent$Login1$txtUser2'
    PASSWORD = 'ctl00$MainContent$Login1$txtPassword2'
    
    LOGIN_FORM = {
        '__EVENTTARGET': '',
        '__EVENTARGUMENT': '',
        'Menu_txtZipCode': 'Enter ZIP Code',
        'ctl00$MainContent$Login1$txtUser1': '',
        'ctl00$MainContent$Login1$txtPassword1': '',
        'ctl00$MainContent$Login1$btnLogin2': 'Sign in'
    }

    DEFAULT_HEADERS = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Origin': 'https://www.lafitness.com',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_6_8) AppleWebKit/537.17 (KHTML, like Gecko) Chrome/24.0.1312.57 Safari/537.17',
        'Referer': 'https://www.lafitness.com/Pages/login.aspx',
        'Accept-Encoding': 'gzip,deflate,sdch',
        'Accept-Language': 'en-US,en;q=0.8',
        'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3'
    }

    def __init__(self, username, password, *args, **kwargs):
        self.username = username
        self.password = password
        self.login()

    def _http_get(self, url):
        return requests.get(url, cookies=self.cookies, headers=self.DEFAULT_HEADERS)

    def _http_post(self, url, data):
        return requests.post(url, data=data, cookies=self.cookies, headers=self.DEFAULT_HEADERS)

    def login(self):
        rsp = requests.get(self.URLS['LOGIN'])
        self.cookies = rsp.cookies

        TO_EXTRACT = ('__VIEWSTATE', '__EVENTVALIDATION', 'RaiseException')

        soup = BeautifulSoup(rsp.content)

        for param in TO_EXTRACT:
            element = soup.find(attrs={'name': param})
            self.LOGIN_FORM[param] = element['value']

        self.LOGIN_FORM.update({self.USERNAME: self.username, self.PASSWORD: self.password})
        rsp = self._http_post(self.URLS['LOGIN'], data=self.LOGIN_FORM)

        try:
            assert rsp.headers['location'] == '/Pages/memberServices.aspx?task=CustomerManagement'
        except AssertionError:
            print "Did not get the expected 302 Location; probably wrong username + password"
            sys.exit(1)

    def get_checkin_history(self):
        rsp = self._http_get(self.URLS['CHECKIN_HISTORY'])

        soup = BeautifulSoup(rsp.content)

        i = soup.find(attrs={'id': 'ctl00_MainContent_checkinHistoryGrid'})
        i = i.findAll('td')[2:]

        c = [e.contents[0] for e in i]
        check_ins = zip(c[0::2], c[1::2])

        return check_ins


la = LAFitness(username='YOUR_USERNAME', password='YOUR_PASSWORD')
print la.get_checkin_history()