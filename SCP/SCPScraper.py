from requests import get
from requests.exceptions import RequestException
from contextlib import closing
from bs4 import BeautifulSoup
import random

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
    #print(html)
    return html

def write_scp(html, scp):    
    doc = open("SCP_"+str(scp)+".txt", 'w', encoding='utf-8')
    for p in html.select('p'):
        if ("SCP by Series" in p) or ("SCP Tales by Series" in p) or ("SCP Library" in p) or ("Discover Content" in p) or ("Discover Content" in p) or ("SCP Community" in p) or ("User Resources" in p):
            continue
        doc.write(p.text)
        doc.write("\n\n")
    doc.write("\n")
    doc.close()

def main():
    scp = 1
    while (scp < 4639):
        if (scp < 10):
            url = "http://www.scp-wiki.net/scp-00"+str(scp)
        elif (scp < 100):
            url = "http://www.scp-wiki.net/scp-0"+str(scp)
        else:
            url = "http://www.scp-wiki.net/scp-"+str(scp)
        raw_html = simple_get(url)
        html = get_html(raw_html)
        #print(html)
        write_scp(html, scp)
        scp += 1
    #print("Done!")




main()