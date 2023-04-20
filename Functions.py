from bs4 import BeautifulSoup
import requests

PAGEURL = 'https://libgen.is/scimag/?q='
def getPage(DOI):
    page = requests.get(f"{PAGEURL}{DOI}")
    soup = BeautifulSoup(page.text, "html.parser")
    for li in  soup.find_all('ul', {"class" : "record_mirrors" }):
        for a in li.find_all('a'):
            print(a['href'])
            getDownloadLink(a['href'])
    return page

def getDownloadLink(url):
    page = requests.get(url)
    soup = BeautifulSoup(page.text, "html.parser")
    links = soup.find_all("a", string="GET")
    download_links = {link.string: link["href"] for link in links}
    print(download_links)
    return download_links
