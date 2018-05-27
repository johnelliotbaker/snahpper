from lib.Browser import Browser
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from datetime import datetime
import re


class Collector(object):
    def __init__(self, br):
        self.url = None
        self.br = br
        self.bs = BeautifulSoup('', 'html.parser')
        self.lastResp = ''
        self.data = []

    def loadbs(self, resp):
        self.bs.__init__(resp.text, 'html.parser')

    def collect(self, url):
        self.url = url
        resp = self.br.request(url=url)
        #  self.br.writelog(resp)
        self.loadbs(resp)
        self.lastResp = resp
        return resp

    def writelog(self):
        with open('clog.txt', 'w', encoding="utf-8") as fh:
            for d in self.data:
                fh.writelines(d[0])
                fh.write('\n')

    def collectDatetime(self, **kwargs):
        resp = None
        if 'response' in kwargs:
            resp = kwargs['response']
        elif 'url' in kwargs:
            resp = self.br.request(url=url)
        else:
            print("Require at least one of url or response.")
            return None
        self.loadbs(resp)
        bs = self.bs
        topic = bs.find("div", text=re.compile("Topics"))
        bLoop = True
        res = []
        while bLoop:
            try:
                topic = topic.find_next("a", {"class": "topictitle"})
                t = topic.find_next("div", {"class": "topic-poster responsive-hide left-box"})
                t =  t.text.split('»')[1].strip()
                dt = datetime.strptime(t, '%a %b %d, %Y %I:%M %p')
                res.append(dt)
            except Exception as e:
                bLoop = False
        return res

    def collectTopics(self, **kwargs):
        resp = None
        if 'response' in kwargs:
            resp = kwargs['response']
        elif 'url' in kwargs:
            resp = self.br.request(url=url)
        else:
            print("Require at least one of url or response.")
            return None
        self.loadbs(resp)
        bs = self.bs
        topic = bs.find("div", text=re.compile("Topics"))
        bLoop = True
        res = []
        while bLoop:
            try:
                topic = topic.find_next("a", {"class": "topictitle"})
                href = topic['href']
                title = topic.string
                fullurl = urljoin(self.url, href)
                entry = (title, fullurl)
                res.append(entry)
            except:
                bLoop = False
        return res

    def getNextPageUrl(self):
        try:
            item = self.bs.body.find_all("div", {"class": "pagination"}
                    )[0].ul.find_all("li", {"class": "active"})[0]
            nextPartialUrl = item.find_next('li').a['href']
            nextUrl = urljoin(self.url, nextPartialUrl)
        except Exception as e:
            print('No more pages after {}'.format(self.url))
            nextUrl = None
        return nextUrl
