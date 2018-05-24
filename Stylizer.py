import re

MEGA_COLOR = "#800000"
ZS_COLOR = "#404000"
SIZE_COLOR = "#008000"



FORUM_COLOR_PATTERN = "[color={}]{}[/color]"
HTML_COLOR_PATTERN = '<span class="host" style="color: {};">{}</span>'


def recursiveReplace(strn, sPattern, dPattern):
    bLoop = True
    if strn is None:
        return ''
    while (bLoop):
        if strn is None:
            return ''
        newStrn = strn.replace(sPattern, dPattern)
        if newStrn == strn:
            return newStrn
        strn = newStrn


class Stylizer(object):
    def __init__(self, strn, **kwargs):
        self.strn = strn
        self.kwargs = kwargs
        self.categorizer = None
        if 'categorizer' in kwargs:
            self.categorizer = kwargs['categorizer']
        self.normalizeBrackets()
        self.normalizeHost()
    
    def init(self, strn, **kwargs):
        self.__init__(strn, **kwargs)

    def colorizeSize(self, strn, style):
        color = SIZE_COLOR
        pattern = "{1:s}"
        if style == 'forum':
            pattern = FORUM_COLOR_PATTERN
        elif style == 'html':
            pattern = HTML_COLOR_PATTERN
        strn = pattern.format(color, strn)
        return strn

    def colorizeHost(self, strn, style):
        if strn == 'MEGA':
            color = MEGA_COLOR
        if strn == 'ZS':
            color = ZS_COLOR
        #  strn = "[color={}]".format(color) + strn + "[/color]"
        pattern = "{1:s}"
        if style == 'forum':
            pattern = FORUM_COLOR_PATTERN
        elif style == 'html':
            pattern = HTML_COLOR_PATTERN
        strn = pattern.format(color, strn)
        return strn

    def removeExtras(self):
        aFrom = ['.', '  ', '[/]']
        aTo   = [' ', ' ', '']
        for i, v in enumerate(aFrom):
            self.strn = recursiveReplace(self.strn, aFrom[i], aTo[i])

    def normalizeHost(self):
        aFrom =  ['MEGA/ZS',  'ZS/MEGA', 'Mega']
        aTo =    ['MEGA][ZS', 'ZS][MEGA','MEGA']
        for i, v in enumerate(aFrom):
            self.strn = recursiveReplace(self.strn, aFrom[i], aTo[i])

    def normalizeBrackets(self):
        strn = self.strn
        aFrom =  ['(', '{', '【', '】', ')', '}']
        aTo =    ['[', '[', '[',  ']' , ']', ']']
        aFrom += ['（', '）']
        aTo   += ['[' , ']']
        for i, v in enumerate(aFrom):
            strn = recursiveReplace(strn, aFrom[i], aTo[i])
        self.strn = strn

    def appendSize(self, categorizer, style='html', bColorize=True):
        for size in categorizer.aSize:
            if bColorize:
                size = self.colorizeSize(size, style=style)
            self.strn += ''.join([ '[', size, ']' ])

    def appendHost(self, categorizer, style='html', bColorize=True):
        for host in categorizer.aHost:
            if bColorize:
                host = self.colorizeHost(host, style=style)
            self.strn += ''.join([ '[', host, ']' ])

    def appendTag(self, cat, style):
        if cat.tag is not None:
            if style == 'html':
                tagStrn = ' <span class="ftag">[{}]</span>'.format(cat.tag)
            elif style == 'forum':
                tagStrn = ' [{}]'.format(cat.tag)
            self.strn += tagStrn

    def stylize(self, style, categorizer=None):
        self.appendHost(categorizer, style)
        self.appendSize(categorizer, style)
        self.appendTag(categorizer, style)
        self.strn = self.strn.strip()



