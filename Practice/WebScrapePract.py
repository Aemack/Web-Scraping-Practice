from requests import get
from requests.exceptions import RequestException
from contextlib import closing
from bs4 import BeautifulSoup


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

def save_p_to_doc(urlStr):
    raw_html = simple_get(urlStr)
    # Parses the raw html by passing it to BeautifulSoup constructor
    html = BeautifulSoup(raw_html, 'html.parser')

    # Opens/creates html doc
    htmlDoc = open('htmlPara.txt', 'w')

    # Loops through each p and writes text to doc
    for p in html.select('p'):
        htmlDoc.write(str(p))
    htmlDoc.close()

save_p_to_doc('https://en.wikipedia.org/wiki/Scotland')