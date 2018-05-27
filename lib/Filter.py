from lib.Categorizer import Categorizer

class Filter(object):
    def __init__(self, aData):
        self.aData = aData

    def removeBeforeYear(self, target):
        res = []
        for data in self.aData:
            entry = data[0]
            cat = Categorizer(entry)
            year = cat.getYear()
            if year >= target:
                res.append(data)
        return res

        
    
