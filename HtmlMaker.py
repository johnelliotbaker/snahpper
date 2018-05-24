CARD_TEMPLATE = """
<div class="card border-light mw-100" style="margin-bottom:10px;">
  <h5 class="card-header" style="padding-left: 12px;">{{cardtitle}}</h5>
  <div class="card-body" style="padding:0px 10px 0px 30px;">
    <p class="card-text" style="margin:5px;">{{cardtext}}</p>
  </div>
</div>
"""

HEAD_TEMPLATE = """
<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN"
"http://www.w3.org/TR/html4/loose.dtd">
<html>
<head>
  <meta charset="utf-8">
  <title>{{title}}</title>
  <link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.1.1/css/bootstrap.min.css" integrity="sha384-WskhaSGFgHYWDcbwN70/dfYBj47jz9qbsMId/iRN3ewGhXQFZCSftd1LZCfmhktB" crossorigin="anonymous">
  <script src="https://code.jquery.com/jquery-3.3.1.slim.min.js" integrity="sha384-q8i/X+965DzO0rT7abK41JStQIAqVgRVzpbzo5smXKp4YfRvH+8abtTE1Pi6jizo" crossorigin="anonymous"></script>
  <script src="https://cdnjs.cloudflare.com/ajax/libs/popper.js/1.14.3/umd/popper.min.js" integrity="sha384-ZMP7rVo3mIykV+2+9J3UJ46jBk0WLaUAdn689aCwoqbBJiSnjAK/l8WvCWPIPm49" crossorigin="anonymous"></script>
  <script src="https://stackpath.bootstrapcdn.com/bootstrap/4.1.1/js/bootstrap.min.js" integrity="sha384-smHYKdLADwkXOn1EmN1qk/HfnUcbVRZyYmZ4qpPea6sjB/pTJ0euyQp0Mk8ck+5T" crossorigin="anonymous"></script>
  <link href='https://fonts.googleapis.com/css?family=Lato' rel='stylesheet' type='text/css'>
  <link href='https://fonts.googleapis.com/css?family=Anton' rel='stylesheet' type='text/css'>
  <link href='https://fonts.googleapis.com/css?family=Fjalla+One' rel='stylesheet' type='text/css'>
  <link href='https://fonts.googleapis.com/css?family=Patua+One' rel='stylesheet' type='text/css'>
  <style>
  @import url(https://fonts.googleapis.com/css?family=Lato);
  @import url(https://fonts.googleapis.com/css?family=Anton);
  @import url(https://fonts.googleapis.com/css?family=Fjalla+One);
  @import url(https://fonts.googleapis.com/css?family=Patua+One);
  @font-face { font-family: 'Patua One', cursive; }
  @font-face { font-family: 'Anton', sans-serif; }
  @font-face { font-family: 'Lato', sans-serif; }
  @font-face { font-family: 'Fjalla One', sans-serif; }
  body { font-family: 'Patua One', sans-serif; font-size: 1.3em;}
  .host { font-family: 'Anton', sans-serif; font-size: 0.65em; }
  .ftag { color: #DDD; }
  ul { list-style-type: none; padding: 0px;}
  li { padding-bottom: 5px; }
  a { color: black; }
  a:link { text-decoration: none; color: #444; }
  a:visited { text-decoration: none; color: #DDD;}
  {{style}}
  </style>
</head>
"""

BODY_TEMPLATE = """
<body>
{{body}}
"""

TAIL_TEMPLATE = """
</body>
</html>
"""


class HtmlMaker(object):
    def __init__(self):
        self.head = ''
        self.body = ''
        self.tail = ''
        self.html = ''
        self.init()
    
    def init(self):
        self.html = ''
        self.makeHead()
        self.makeBody()
        self.makeTail()
        self.html += self.head + self.body + self.tail

    def makeHead(self, title="Snahp Harvester"):
        strn = HEAD_TEMPLATE
        self.head = strn

    def setTitle(self, title):
        self.html = self.html.replace("{{title}}", title)

    def addStyle(self, strn):
        strn = """
        @font-face { font-family: 'Anton', sans-serif; }
        body { font-family: 'Anton', sans-serif; }
        {{style}}
        """
        self.html = self.html.replace("{{style}}", strn)

    def makeBody(self):
        strn = BODY_TEMPLATE
        self.body = strn

    def appendBody(self, strn):
        self.html = self.html.replace("{{body}}", strn + "{{body}}")

    def addCard(self): 
        self.cleanupCard()
        strn = CARD_TEMPLATE
        self.html = self.html.replace("{{body}}", strn + "{{body}}")

    def addCardTitle(self, strn):
        self.html = self.html.replace("{{cardtitle}}", strn + "{{cardtitle}}")

    def addCardText(self, strn):
        self.html = self.html.replace("{{cardtext}}", strn + "{{cardtext}}")


    def makeTail(self, title="Snahp Harvester"):
        strn = TAIL_TEMPLATE
        self.tail = strn

    def cleanupCard(self):
        self.html = self.html.replace("{{cardtitle}}", "")
        self.html = self.html.replace("{{cardtext}}", "")

    def cleanup(self):
        self.html = self.html.replace("{{style}}", "")
        self.html = self.html.replace("{{body}}", "")
        self.cleanupCard()

    def save(self, filename):
        self.cleanup()
        path = filename
        with open(path, 'w', encoding="utf-8") as fh:
            fh.write(self.html)

if __name__ == "__main__":
    hm = HtmlMaker()
    hm.init()
    hm.addStyle('')
    hm.appendBody('<p><a href="#">What is your name</a></p>')
    hm.save()
    print(hm.html)

    
