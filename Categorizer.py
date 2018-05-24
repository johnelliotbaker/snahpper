import re
import pdb


HOST_LIST = ['MEGA', 'ZS']
HOST_PATTERN = {
        'MEGA': r'[\(\[]{1}MEGA[\)\]]',
        'ZS': r'[\(\[]{1}ZS[\)\]]'
        }

SIZE_LIST = ['GB', 'MB']
SIZE_PATTERN = {
        'GB': r'([\[]?((\d+)(([\.,])?(\d)+)?(\s)?(gb|GB|Gb|GiB|Gib))[\]]?)',
        'MB': r'([\[]?((\d+)(([\.,])?(\d)+)?(\s)?(mb|MB|Mb))[\]]?)'
        }

YEAR_PATTERN = {
        'FourDigitYear': r'\d{4}'
        }

class Categorizer(object):
    def __init__(self, strn):
        self.strn = strn
        self.tag = None

    def init(self, strn):
        self.__init__(strn)

    def registerTag(self, tag):
        self.tag = tag
    
    def popHost(self):
        strn = self.strn
        aHost = []
        for host in HOST_LIST:
            match = re.findall(HOST_PATTERN[host], strn)
            if len(match)>0:
                aHost.append(host)
                for item in match:
                    strn = strn.replace(item, '')
        self.aHost = aHost
        self.strn = strn

    def popSize(self):
        strn = self.strn
        aSize = []
        for size in SIZE_LIST:
            match = re.findall(SIZE_PATTERN[size], strn)
            if len(match)>0:
                aSize.append(match[0][1])
                strn = strn.replace(match[0][0], '')
        self.aSize = aSize
        self.strn = strn

    def getYear(self):
        strn = self.strn
        pattern = YEAR_PATTERN['FourDigitYear']
        match = re.findall(pattern, strn)
        year = 0
        if len(match) > 0:
            year = int(match[0])
            year = year if year > 1800 else 0
        else:
            year == 9999
        return year


if __name__ == "__main__":
    with open('markup.txt', 'r', encoding="utf-8") as fh:
        entry = fh.readline()
    print(entry)
    ct = Categorizer(entry)
    ct.popHost()
    ct.popSize()

