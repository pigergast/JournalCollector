from bs4 import BeautifulSoup
import requests

PAGEURL = 'https://libgen.is/scimag/?q='

def checkLibgen(DOI):
    page = requests.get(f"{PAGEURL}{DOI}")
    soup = BeautifulSoup(page.text, "html.parser")
    downloadList = []
    mirrors = soup.find_all('ul', {"class": "record_mirrors"})
    for li in mirrors:
        for a in li.find_all('a'):
            link = a['href']
            if (link.startswith('http://library.lol')):
                downloadList.append(getDownloadLink(a['href']))
    #if downloadlist is not 0, then it is available
    if(len(downloadList) != 0):
        #return first link
        return downloadList[0]
    else:
        return None

def getPage(DOI):
    page = requests.get(f"{PAGEURL}{DOI}")
    soup = BeautifulSoup(page.text, "html.parser")
    downloadList = []
    mirrors = soup.find_all('ul', {"class" : "record_mirrors" })
    if(len(mirrors) != 1):
        return None
    for li in mirrors:
        for a in li.find_all('a'):
            link = a['href']
            if(link.startswith('http://library.lol')):
                downloadList.append(getDownloadLink(a['href']))
    return page

def getDownloadLink(url):
    page = requests.get(url)
    soup = BeautifulSoup(page.text, "html.parser")
    links = soup.find_all("a", string="GET")
    download_links = {link.string: link["href"] for link in links}
    # print(download_links['GET'])
    return download_links['GET']