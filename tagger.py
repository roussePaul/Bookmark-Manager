import urllib.parse
import urllib.request
import bs4 as BeautifulSoup
import json
import pprint
from rauth import OAuth1Service

from yahoo import getNbreResults

from bdd import *


def getTags(url):
    
    param = { 'q' : 'select * from contentanalysis.analyze where url=\'' + url +'\';', 'format' : 'json', 'diagnostics' : 'true'}
    query = urllib.parse.urlencode(param)
    
    queryURL = 'https://query.yahooapis.com/v1/public/yql?' + query
    
    
    result = urllib.request.urlopen(queryURL).read().decode('utf-8')
    
    decoded = json.loads(result)
    
    result = decoded['query']['results']
    if result == None:
        return None
    else:
        return result['entities']['entity']
    
def getTagOccurence(tag):
    n = getTag(tag)
    if n<0:
        print('Query '+tag+'...')
        n = getNbreResults(tag)
        putTag(tag,n)
    return n
    
def distanceTags(tag1,tag2):
    n1 = getTagOccurence(tag1)
    n2 = getTagOccurence(tag2)
    n12 = getTagOccurence(tag1 + ' ' + tag2)
    
    r = 1- 2*n12/(n1 + n2)
    dist =  r/(1.01-r)
    
    return dist
    

def distListPage(page1,page2):
    i=0
    d=[]
    for t1 in page1:
            tag1 = t1['text']['content']
            for t2 in page2:
                tag2 = t2['text']['content']
                d.append(distanceTags(tag1, tag2))
    d.sort()
    return d

    
def distancePage(page1, page2):
    seuil = 20
    list = distListPage(page1,page2)
    for i in range(len(list)):
        if list[i]>seuil:
            return 1.0-i/len(list)
    
initBDD()

url1 = 'http://edition.cnn.com/2011/11/11/world/europe/greece-main/index.html'
url2 = 'http://edition.cnn.com/2014/06/10/business/greece-crisis-enterpreneurs/index.html'
url3 = 'http://edition.cnn.com/2014/06/27/world/africa/world-fragile-nations/index.html'

url2 = url1

p1 = getTags(url1)
p2 = getTags(url2)
p3 = getTags(url3)

pp = pprint.PrettyPrinter(indent=4)


print('Distance page 1 et 2 = '+ str(distancePage(p1,p2)))
print('Distance page 3 et 2 = '+ str(distancePage(p3,p2)))
print('Distance page 1 et 3 = '+ str(distancePage(p1,p3)))


closeBDD()