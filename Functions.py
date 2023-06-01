from bs4 import BeautifulSoup
import requests

PAGEURL = 'https://libgen.is/scimag/?q='
def getPage(DOI):
    page = requests.get(f"{PAGEURL}{DOI}")
    soup = BeautifulSoup(page.text, "html.parser")
    downloadList = []
    mirrors = soup.find_all('ul', {"class" : "record_mirrors" })
    title = soup.find('a').text;
    print(title)
    if(len(mirrors) != 1):
        return None
    for li in mirrors:
        for a in li.find_all('a'):
            link = a['href']
            if(link.startswith('http://library.lol')):
                downloadList.append(getDownloadLink(a['href']))
    #go through each link and download the pdf. If one download is sucessful, exit and return true
    for link in downloadList:
            print(link)
            downloadPdf(link, f"{DOI}.pdf")

def getDownloadLink(url):
    page = requests.get(url)
    soup = BeautifulSoup(page.text, "html.parser")
    links = soup.find_all("a", string="GET")
    download_links = {link.string: link["href"] for link in links}
    print(download_links['GET'])
    return download_links['GET']

def downloadPdf(url, title):
    response = requests.get(url)
    file = open("test.pdf", "wb")
    file.write(response.content)
    file.close()
