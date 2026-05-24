from html.parser import HTMLParser
from html.entities import name2codepoint
import urllib.request

class MyHTMLParser(HTMLParser):

    def __init__(self):
        super().__init__()
        self.processTag = False
        self.line = []
        self.lines = []
        self.lines.append('Link,Longitude,Latitude,Name')

    def handle_starttag(self, tag, attrs):
        for attr in attrs:
            if attr[0] == 'class' and attr[1] == 'place':
               self.processTag = True
        
        if self.processTag == True:
            self.line.append(attrs[0][1])
            self.line.append(attrs[2][1])
            self.line.append(attrs[3][1])

    def handle_data(self, data):
        if self.processTag == True:
            self.line.append(data)
            self.lines.append(','.join(self.line))
            self.line = []
            self.processTag = False


parser = MyHTMLParser()
url = urllib.request.urlopen("https://topostext.org/work/245") 
html = url.read().decode()
url.close()
parser.feed(html)

with open("virgil-aeneid.csv", "w") as txt_file:
    for line in parser.lines:
        txt_file.write(line + "\n")
