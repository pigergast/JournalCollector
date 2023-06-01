from bs4 import BeautifulSoup
import requests
from pymed import PubMed

PAGEURL = 'https://libgen.is/scimag/?q='
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
    print(download_links['GET'])
    return download_links['GET']


def getListOfDoiByYear(year):

    ISSN = "1527-6546"  # Journal of Nursing Scholarship ISSN
    query = f'("{year}/1/1"[Date - Publication] : "{year}/12/31"[Date - Publication]) AND {ISSN}[IS]'
    pubmed = PubMed(tool="MyTool", email="tangkwo1@hotmail.com")
    results = pubmed.query(query, max_results=9999)

    doi_list = []
    for article in results:
        if article.doi:
            doi_list.append(article.doi)

    return doi_list
