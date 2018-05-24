from Browser import Browser
from Publisher import Publisher
from Collector import Collector
from bs4 import BeautifulSoup
from Stylizer import Stylizer
from Categorizer import Categorizer
from Configurator import Configurator
from Filter import Filter

from datetime import datetime, timedelta
from urllib.parse import urljoin
from os.path import join as pjoin
import shutil
import json


PUBLISH_PATH = './pub/'
CONFIG_PATH = './config.json'
ARCHIVE_PATH = '/mnt/Z/pub'
N_FORGIVENESS = 10


def getNow():
    #  return datetime.utcnow()
    return datetime.now()


class Crawler(object):
    @property
    def config(self): return self._config
    
    @config.setter
    def config(self, val):
        self._config = val
        self.host = val.getHost()
        self.auth = val.getAuth()
        self.bOnline = True if self.host == 'local' else False
    
    def __init__(self, config):
        self.config = config
        self.br = Browser()
        self.collector = Collector(self.br)
        self.idx = 0
        self.data = []
        self.resp = self.br.login(self.host, self.auth['username'], self.auth['password'])

    def getForumUrl(self, fid):
        forumUrl = './viewforum.php?f={}&sk=c'.format(fid)
        url = urljoin(self.host, forumUrl)
        return url

    #  def publish(self, filename='dailyHarvest.txt'):
    def publish(self, **kwargs):
        filename = kwargs['filename'] if 'filename' in kwargs else 'published.text'
        days = kwargs['days'] if 'days' in kwargs else 7
        style = kwargs['style'] if 'style' in kwargs else 'html'

        pub = Publisher(self.data, days)
        pub.publish(style, filename)


    def crawl(self, queue, days):
        collector = self.collector
        for fid in queue:
            forumDef = self.config.forumDef
            fidStrn = str(fid)
            ftag = '{}'.format(
                    forumDef[fidStrn]['title'],
                    ) if fidStrn in forumDef else 'unknown'
            fgroup = '{}'.format(
                    forumDef[fidStrn]['group'],
                    ) if fidStrn in forumDef else 'unknown'
            url = self.getForumUrl(fid)
            res = []
            nextUrl = url
            bLoop = True
            nForgive = N_FORGIVENESS
            iForgive = 0
            while nextUrl is not None and bLoop:
                resp = collector.collect(nextUrl)
                topic = collector.collectTopics(response=resp)
                dt = collector.collectDatetime(response=resp)
                for i,t in enumerate(topic):
                    res.append( (t[0], t[1], dt[i], fgroup, ftag))
                    if dt[i] < getNow() - timedelta(days=days):
                        iForgive += 1
                        if iForgive > nForgive:
                            bLoop = False
                            break
                nextUrl = collector.getNextPageUrl()
            res.sort(key=lambda x:x[1], reverse=True)
            collector.data = res
            for data in collector.data:
                if data[2] > getNow()-timedelta(days=days):
                    self.data.append(data)
        self.data.sort(key=lambda x:x[2], reverse=True)
    

if __name__ == "__main__":
    config = Configurator(CONFIG_PATH)
    with open('jobs.json', 'r', encoding="utf-8") as fh:
        jsjob = json.loads(fh.read())
        aJob = jsjob['jobs']
        jobMode =  jsjob['mode']
        config.setMode(jobMode)
    for job in aJob:
        bOnline = False if config.getMode() == 'local' else True
        title = job['title']
        minYear = job['minYear'] if 'minYear' in job else None
        if job['enabled']:
            days = job['days']
            basename = title
            crawler = Crawler(config)
            if bOnline: queue = job['queue']
            else: queue = [9]
            crawler.crawl(queue, days)
            if minYear is not None:
                filt = Filter(crawler.data)
                crawler.data = filt.removeBeforeYear(minYear)
            for style in config.cfg['publish']['queue']:
                filename = basename + config.cfg['publish'][style]['filename']['extension']
                crawler.publish(filename=filename, days=days, style=style)
                if config.cfg['publish']['bArchive'] == 1:
                    shutil.copyfile(filename, pjoin(ARCHIVE_PATH, filename))
