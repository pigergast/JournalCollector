from bs4 import BeautifulSoup
import requests
import urllib.parse
import re
PAGEURL = 'https://libgen.is/scimag/?q='
def getPDF(DOI):
    page = requests.get(f"{PAGEURL}{DOI}")
    soup = BeautifulSoup(page.text, "html.parser")
    downloadList = []
    mirrors = soup.find_all('ul', {"class" : "record_mirrors" })
    if(len(mirrors) != 1):
        return False
    safeDOI = urllib.parse.quote(DOI, safe='')
    title = soup.find('a', href=f'/scimag/{safeDOI}').text
    print(title)
    for li in mirrors:
        for a in li.find_all('a'):
            link = a['href']
            if(link.startswith('http://library.lol')):
                downloadList.append(getDownloadLink(a['href']))
    #Go through each link in the download list and attempt to download. If download is successful, return true, else return false. If error occur, print exception
    for link in downloadList:
        try:
            downloadPdf(link, f"{title}.pdf")
            return True
        except Exception as e:
            print(e)
            continue
    return False

def getDownloadLink(url):
    page = requests.get(url)
    soup = BeautifulSoup(page.text, "html.parser")
    links = soup.find_all("a", string="GET")
    download_links = {link.string: link["href"] for link in links}
    return download_links['GET']

def downloadPdf(url, title):
    response = requests.get(url)
    print(title)
    fileTitle = re.sub(r'[\\/*?:"<>|]', "", title)
    file = open(fileTitle , "wb")
    file.write(response.content)
    file.close()
