import requests
from requests_oauthlib import OAuth1
import json
import urllib.parse
from config import *

def getNbreResults(tag):
    url = "http://yboss.yahooapis.com/ysearch/limitedweb?q="+tag
    auth = OAuth1(OAUTH_CONSUMER_KEY, OAUTH_CONSUMER_SECRET)

    req = requests.get(url, auth=auth)

    jreq = json.loads(req.content.decode('utf-8'))
    return int(jreq['bossresponse']['limitedweb']['totalresults'])
