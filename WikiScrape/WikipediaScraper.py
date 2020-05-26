from requests import get
from requests.exceptions import RequestException
from contextlib import closing
from bs4 import BeautifulSoup
import random
import re

def simple_get(url):
    """ 
    Attempts to get the content at 'url' by making an HTTP GET request.
    If the content-type of response is some kind of HTML/XML, return the text content, otherwise return none
    """
    try:
        with closing(get(url, stream=True)) as resp:
            if is_good_response(resp):
                return resp.content
            else:
                return None
    
    except RequestException as e:
        log_error('Error during requests at {0} : {1}'.format(url,str(e)))
        return None

def is_good_response(resp):
    """
    Returns True if the response seems to be HTML, False otherwise
    """

    content_type = resp.headers['Content-Type'].lower()
    return (resp.status_code == 200
            and content_type is not None
            and content_type.find('html') > -1)

def log_error(e):
    """
    It is always a  good idea to log errors.
    This function just prints them, but you can make it do anything.
    """
    print(e) 

def get_html(resp):
    # Parses the raw html by passing it to BeautifulSoup constructor
    html = BeautifulSoup(resp, 'html.parser')
    return html

def get_title(html):
    for h1 in html.select('h1'):
        if h1['id'] == "firstHeading":
            titleDoc = open('WikiTitles.txt', 'a')
            titleDoc.write(str(h1.text))
            titleDoc.write("\n   V   \n")
        titleDoc.close()

def getLink(html, toFind):
    links =[]
    for link in html.find_all("a", href=True):
        #print(link)
        url = link.get("href", "")
        #print(url)
        if "/wiki/" in url:
            if ("wikipedia" not in url) and ("#" not in url)  and ("ī" not in url) and ("ṃ" not in url) and ("ā" not in url) and ("/wiki/Talk" not in url) and ("/wiki/File" not in url) and ("(" not in url) and ("/wiki/Special" not in url) and ("/wiki/Wiki" not in url) and ("/wiki/Privacy" not in url)and (".org" not in url)and ("/wiki/Help" not in url) and ("/wiki/Category" not in url) and ("/wiki/Template" not in url) and ("," not in url) and ("%" not in url) and ("Portal" not in url):        
                fullUrl = "https://en.wikipedia.org"+url
                if (toFind in fullUrl):
                    return fullUrl
                #print(fullUrl)
                links.append(fullUrl)
    #print(links)
    randNum = random.randint(1, len(links))
    if len(links) == 0:
        return html
    print(links[randNum-1])
    return links[randNum-1]


def main(startUrl,toFind):
    startUrl = "https://en.wikipedia.org/wiki/"+startUrl
    count = 1
    resp = simple_get(startUrl)
    html = get_html(resp)
    get_title(html)
    newUrl = getLink(html, toFind)
    while(toFind not in newUrl):
        #print(newUrl)
        count += 1
        resp = simple_get(newUrl)
        html = get_html(resp)
        get_title(html)
        newUrl = getLink(html, toFind)
    count += 1
    resp = simple_get(newUrl)
    html = get_html(resp)
    get_title(html)
    print("Total Jumps: "+str(count))

    

main('Dracula',"Iron Man")

