from Browser import Browser
from Crawler import Crawler
from Configurator import Configurator
from Filter import Filter
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

    def exec(self):
        config = self.config
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

if __name__ == "__main__":
    snahpper = Snahpper()
    snahpper.exec()
