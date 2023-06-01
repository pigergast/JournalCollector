from bs4 import BeautifulSoup
import requests
import urllib.parse
import re
import os
from pymed import PubMed

PAGEURL = 'https://libgen.is/scimag/?q='
def getPDF(DOI):
    page = requests.get(f"{PAGEURL}{DOI}")
    soup = BeautifulSoup(page.text, "html.parser")
    downloadList = []
    mirrors = soup.find_all('ul', {"class" : "record_mirrors" })
    if(len(mirrors) != 1):
        return False, "No PDF found"
    safeDOI = urllib.parse.quote(DOI, safe='')
    title = soup.find('a', href=f'/scimag/{safeDOI}').text
    for li in mirrors:
        for a in li.find_all('a'):
            link = a['href']
            if(link.startswith('http://library.lol')):
                downloadList.append(getDownloadLink(a['href']))
    #Go through each link in the download list and attempt to download. If download is successful, return true, else return false. If error occur, print exception
    for link in downloadList:
        try:
            downloadPdf(link, f"{title}.pdf")
            return True, title
        except Exception as e:
            print(e)
            continue
    return False, title

def getDownloadLink(url):
    page = requests.get(url)
    soup = BeautifulSoup(page.text, "html.parser")
    links = soup.find_all("a", string="GET")
    download_links = {link.string: link["href"] for link in links}
    return download_links['GET']

def downloadPdf(url, title):
    isExist = os.path.exists("Downloads")
    if not isExist:
        # Create a new directory because it does not exist
        os.makedirs("Downloads")
    response = requests.get(url)
    fileTitle = re.sub(r'[\\/*?:"<>|]', "", title)
    file = open(f"Downloads/{fileTitle}" , "wb")
    file.write(response.content)
    file.close()

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

