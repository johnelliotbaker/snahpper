import json

ALLOWED_MODE = ['snahp', 'local']


class Configurator(object):
    
    @property
    def filename(self): return self._filename
    
    @filename.setter
    def filename(self, val):
        self._filename = val
        with open(val, 'r', encoding="utf-8") as fh:
            self.cfg = json.loads(fh.read())
        self.forumDef = self.getForumDef()
        self.mode = self.getMode()
        self.connection = self.getConnection(self.mode)
        self.auth = self.getAuth()
        self.host = self.getHost()
    
    def __init__(self, filename):
        self.cfg = None
        self.filename = filename

    def setMode(self, mode):
        if mode in ALLOWED_MODE:
            self.cfg['mode'] = mode
            self.mode = mode
            self.connection = self.getConnection(self.mode)
            self.auth = self.getAuth()
            self.host = self.getHost()

    def getMode(self):
        return self.cfg['mode']

    def getConnection(self, mode):
        return self.cfg['connection'][mode]

    def getHost(self):
        return self.connection['host']

    def getAuth(self):
        return self.connection['credentials']

    def getPubConvention(self):
        return 

    def getForumDef(self):
        filepath = self.cfg['forumDef']['filepath']
        with open(filepath, 'r', encoding="utf-8") as fh:
            forumDef = json.loads(fh.read())
        return forumDef

    
