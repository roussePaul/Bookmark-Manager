import urllib.parse
import urllib.request
import bs4 as BeautifulSoup
import json
import pprint
import math
from rauth import OAuth1Service

from yahoo import getNbreResults

from bdd import *

# Analyse le contenu des pages web et renvoie une liste de tags associés
def queryTags(url):
    
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
    
# Renvoi le nombre de résultats associé à la requete de tag, effectue la requpete que si le tag n'est pas dans la BDD
def getTagOccurence(tag):
    n = getTag(tag)
    if n<0:
        print('Query '+tag+'...')
        n = getNbreResults(tag)
        putTag(tag,n)
    return n
    
# Renvoi le nombre de résultats associé à la requete de double tag, effectue la requpete que si le tag n'est pas dans la BDD
def getTagsOccurence(tag1,tag2):
    n = getTags(tag1,tag2)
    if n<0:
        tag='"'+tag1 + '" "' + tag2+'"'
        print('Query '+tag+'...')
        n = getNbreResults(tag)
        putTags(tag1,tag2,n)
    return n
    
# Poids du double tag 
def weigthTags(tag1,tag2):
    n1 = getTagOccurence(tag1)
    n2 = getTagOccurence(tag2)
    n12 = getTagsOccurence(tag1,tag2)
    
    r = n12/math.sqrt(n1 * n2)
    
    return r
    

def distListPage(page1,page2):
    i=0
    d=[]
    for t1 in page1:
            tag1 = t1['text']['content']
            for t2 in page2:
                tag2 = t2['text']['content']
                d.append(weigthTags(tag1, tag2))
    d.sort()
    return d

    
def distancePage(page1, page2):
    seuil = 20
    list = distListPage(page1,page2)
    for i in range(len(list)):
        if list[i]>seuil:
            return 1.0-i/len(list)

def getListTagsWithWeigth():
    list = getListTags()
    weight = [(tag[0],tag[1],weigthTags(tag[0],tag[1])) for tag in list]
    return weight
    
initBDD()

url2 = 'http://edition.cnn.com/2011/11/11/world/europe/greece-main/index.html'
url1 = 'http://edition.cnn.com/2014/06/10/business/greece-crisis-enterpreneurs/index.html'
url1 = 'http://www.nydailynews.com/entertainment/gossip/angel-haze-confirms-ireland-baldwin-romance-article-1.1847527'


p1 = queryTags(url1)
p2 = queryTags(url2)

pp = pprint.PrettyPrinter(indent=4)

print('Distance page 1 et 2 = '+ str(distancePage(p1,p2)))


closeBDD()