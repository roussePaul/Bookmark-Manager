import urllib.parse
import urllib.request
import bs4 as BeautifulSoup
import json
import pprint
from pygoogle import pygoogle
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
    
    
def getNbreResults(search):
    g = pygoogle(search)
    return int(g.get_result_count())
    
def distanceTags(tag1,tag2):
    n1 = getNbreResults(tag1)
    n2 = getNbreResults(tag2)
    n12 = getNbreResults(tag1 + ' ' + tag2)
    
    r = 1- 2*n12/(n1 + n2)
    return r/(1.0-r)

result = getTags('http://edition.cnn.com/2014/06/27/world/asia/japan-begins-whaling-season-meal-for-school-children/index.html?hpt=ias_c1')

pp = pprint.PrettyPrinter(indent=4)
pp.pprint(result)

print(distanceTags('banane','carotte'))


