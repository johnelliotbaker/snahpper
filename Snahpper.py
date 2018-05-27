from lib.Browser import Browser
from lib.Crawler import Crawler
from lib.Configurator import Configurator
from lib.Filter import Filter
from lib.Publisher import Publisher
from lib.HtmlMaker import HtmlMaker

from os.path import splitext
from os.path import join as pjoin
import os 
import json

CONFIG_PATH = './config.json'
JOBS_PATH = './jobs.json'

class Snahpper(object):
    def __init__(self):
        self.config = None
        self.aJob = []
        self.browser = Browser()
        self.configure(CONFIG_PATH)
        self.loadJobs(JOBS_PATH)

    def configure(self, configFile):
        self.config = Configurator(configFile)

    def loadJobs(self, jobFile):
        with open(jobFile, 'r', encoding="utf-8") as fh:
            jsjob = json.loads(fh.read())
        self.aJob = jsjob['jobs']
        jobMode =  jsjob['mode']
        self.config.setMode(jobMode)
        return self.aJob

    def publishIndex(self, aPublishedFile):
        hm = HtmlMaker()
        hm.setTitle('Snahpper Index')
        hm.addCard()
        hm.addCardTitle('')
        curDir = os.path.dirname(os.path.realpath(__file__))
        for filename in aPublishedFile:
            base, ext = splitext(filename)
            link = '<li><a href="{}" style="color:black;">{}</a></li>'.format(
                    pjoin(curDir, filename), base)
            hm.addCardText(link)
        hm.save('index.html')


    def exec(self):
        config = self.config
        aPublishedFile = []
        for job in self.aJob:
            bOnline = False if config.getMode() == 'local' else True
            title = job['title']
            minYear = job['minYear'] if 'minYear' in job else None
            if job['enabled']:
                days = job['days']
                basename = title
                crawler = Crawler(config, self.browser)
                if bOnline: queue = job['queue']
                else: queue = [9]
                crawler.crawl(queue, days)
                if minYear is not None:
                    filt = Filter(crawler.data)
                    crawler.data = filt.removeBeforeYear(minYear)
                for style in config.cfg['publish']['queue']:
                    filename = basename + config.cfg['publish'][style]['filename']['extension']
                    crawler.publish(filename=filename, days=days, style=style)
                    aPublishedFile.append(filename)
        self.publishIndex(aPublishedFile)

if __name__ == "__main__":
    snahpper = Snahpper()
    snahpper.exec()
