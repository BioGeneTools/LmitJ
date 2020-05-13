"""
This script takes a link of a journal article and returns a dictionary
"""

import requests
from bs4 import BeautifulSoup

class VocabularCollector():
    TheHeadLine = []
    newVoc = []
    def __init__(self):
        pass
    
    def crawLink(self, link):
        page = requests.get("{}".format(link))
        soup = BeautifulSoup(page.content, 'html.parser')

        # for NW.de
        # headline = soup.find_all(class_="article-detail-headline")[0]
        # headline = list(headline.children)[2].replace('\n','')
        # self.TheHeadLine = headline.split(' ')
        # for i in soup.find_all("p", class_="em_text")[0].get_text().split(' '):
        #     i = i.replace('"', '').replace('.','').replace(',','').replace('(','').replace(')','').replace('–','').replace('„','').strip()
        #     if i and len(i)>1 and not i.isnumeric() and not any(x in "@#$%&*?/" for x in i) and i not in self.mainDict and i not in self.referenceDictList and i not in self.newVoc:
        #         self.newVoc.append(i)

        # for Spiegel
        p = []
        for i in soup.find_all("p"):
            for n in i.get_text().replace('\n','').strip().split():
                p.append(n)
        for i in p:
            i = i.replace('"', '').replace('.','').replace(',','').replace('(','').replace(')','').replace('–','').replace('„','').strip()
            if i and len(i)>1 and not i.isnumeric() and not any(x in "@#$%&*?/" for x in i) and i not in self.newVoc:
                self.newVoc.append(i)
        return self.newVoc
        
    def getSentence(self, j):
        l = len(self.newVoc)
        start = j-3
        end = j+4
        if start < 0:
            start = 0
        elif end > len(self.newVoc):
            end = len(self.newVoc)
        return ' '.join(self.newVoc[start:end]) 


# page = requests.get("http://www.nrttv.com/News.aspx?id=19543&MapID=1")
# soup = BeautifulSoup(page.content, 'html.parser')
# s = soup.find_all(class_="article-detail-headline")[0]
# s = list(s.children)[2]
# s.replace('\n','')
# for i in soup.find_all(class_="em_text"):
#     print(i.get_text())
