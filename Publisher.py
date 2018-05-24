from Stylizer import Stylizer
from Categorizer import Categorizer
from datetime import datetime, timedelta
from HtmlMaker import HtmlMaker
import time
from os.path import splitext


FORUM_TEMPLATE = '[url={}]{}[/url]'
HTML_TEMPLATE = '<li><a href={}>{}</a></li>'


class Publisher(object):
    def __init__(self, data, days=7):
        self.aRawData = data
        self.days = days
        self.aData = []
        self.markup = []
        self.stylizer = Stylizer('')
        self.categorizer = Categorizer('')
        self.getDatetimeArray(self.days)
        self.hm = HtmlMaker()

        self.preprocess()

    def getDatetimeArray(self, days=7):
        now = datetime.now()+timedelta(minutes=5)
        res = []
        for i in range(days+1):
            res.append(now-timedelta(days=i))
        self.aDatetime = res
        return res
    
    def publish(self, style, filename='published.txt'):
        totalFiles = 0
        if style == 'html':
            self.hm.appendBody('<ul>')
        aData = []
        for i, date in enumerate(self.aDatetime[:-1]):
            dateStrn = '{}'.format(date.strftime("%B %d"))
            aStrn = []
            for data in self.aData:
                title = data[0]
                href = data[1]
                dt = data[2]
                fgroup = data[3]
                ftag = data[4]
                if dt <= self.aDatetime[i] and dt > self.aDatetime[i+1]:
                    cat = self.categorizer
                    stylizer = self.stylizer
                    cat.init(title)
                    cat.popSize()
                    cat.popHost()
                    cat.registerTag(ftag)
                    stylizer.init(cat.strn)
                    stylizer.removeExtras()
                    stylizer.stylize(style, cat)
                    title = stylizer.strn
                    if style == "forum":
                        strn = FORUM_TEMPLATE.format(href, title)
                        aStrn.append(FORUM_TEMPLATE.format(href, title))
                    else:
                        strn = HTML_TEMPLATE.format(href, title)
                        aStrn.append(HTML_TEMPLATE.format(href, title))
                    totalFiles += 1
            dateStrn += ' - {}'.format(fgroup.upper())
            aData.append( {'dt': dateStrn, 'data': aStrn} )
        if style == 'html':
            for data in aData:
                if len(data['data']) > 0:
                    self.hm.addCard()
                    self.hm.addCardTitle(data['dt'])
                    for strn in data['data']:
                        self.hm.addCardText(strn)
            self.hm.setTitle('{} - Snahp Harvester'.format(splitext(filename)[0]))
            self.hm.save(filename)
        elif style == 'forum':
            with open(filename, 'w', encoding="utf-8") as fh:
                for data in aData:
                    if len(data['data']) > 0:
                        fh.write(data['dt'])
                        fh.write('\n\n')
                        for strn in data['data']:
                            fh.write(strn)
                            fh.write('\n\n')

    def preprocess(self):
        for data in self.aRawData:
            tmp = []
            self.stylizer.init(data[0])
            tmp.append( self.stylizer.strn.strip() )
            tmp.append(data[1].strip())
            tmp.append(data[2])
            tmp.append(data[3])
            tmp.append(data[4])
            self.aData.append(tmp)

    def writefile(self):
        with open('markup.txt', 'w', encoding="utf-8") as fh:
            fh.write('\n'.join(self.markup))
