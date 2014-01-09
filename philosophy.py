import sys
import urllib2,cookielib
import mechanize
import re
from bs4 import BeautifulSoup
import tidylib

goal = "http://en.wikipedia.org/wiki/Philosophy"

visited = []
special = []
loop = []
error = []
limit = 35			# No. of pages to hop before marking as a failure to reach philosophy.

header = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
       'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
       'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
       'Accept-Encoding': 'none',
       'Accept-Language': 'en-US,en;q=0.8',
       'Connection': 'keep-alive'}


def get_html(url):
    global header

    request = urllib2.Request(url, headers=header)

    try:
        br = mechanize.Browser()
        response = br.open(request)
        return response.get_data()
    
    except urllib2.HTTPError, e:
        print e.fp.read()

  
def search(url, count):
    global randomURL, limit
    print '.',
    resultHTML = get_html(url)
    bodySoup = BeautifulSoup(resultHTML)
    body = bodySoup.find('div', { 'class' : 'mw-content-ltr', 'id' : 'mw-content-text' })

    content = BeautifulSoup(str(body))
    firstParagraph = content.find('p')
    
    def find_first_link(content, braces):
        link = content.find('a')
        page = link.get('href')
        URL = 'http://en.wikipedia.org' + page
        content = str(content)
        index = content.index(str(link))

        searchArea = content[0:index]
        for i in range(0, len(searchArea)):
            if searchArea[i] == '(':
                braces += 1
            elif searchArea[i] == ')' and braces != 0:
                braces -= 1
   
        firstLinkRemoved = content[index + len(str(link)):len(content)]
        firstLinkRemoved = str(tidylib.tidy_fragment(firstLinkRemoved))
        firstLinkRemoved = firstLinkRemoved[1:len(firstLinkRemoved) - 2]
        
        if braces != 0 or page[0] == '#' or page[6:16] == 'Wikipedia:' or page[6:11] == 'Help:':
            corrected = BeautifulSoup(firstLinkRemoved)
            return find_first_link(corrected, braces)
        else:
            return URL
        
    firstLink = find_first_link(firstParagraph, 0)
    
    count += 1
    #print str(count) + ' . Flying: ' + str(firstLink)

    if count >= limit:
        special.append(randomURL)
        return 0
    elif firstLink == goal:
        return count
    else:
        return search(firstLink, count)

def get_random_page():
    global headers, visited
    url = 'http://en.wikipedia.org/wiki/Special:Random'
    req = urllib2.Request(url, '', header)
    res = urllib2.urlopen(req)
    page = res.geturl()
    if page in visited:
        return get_random_page()
    else:
        visited.append(page)
        #print 'Got a page: ' + page
        return page
    
count = 0
for i in range(0, 10):
    try:
        randomURL = get_random_page()
        count = search(randomURL, count)
        print '\n' + str(count) + ' ',
        with open("analysis.csv", "a") as myfile:
            myfile.write(str(count) + ', ')
    except AttributeError:
        error.append(randomURL)
