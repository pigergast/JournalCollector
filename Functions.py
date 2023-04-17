from bs4 import BeautifulSoup
import requests

PAGEURL = 'https://libgen.is/scimag/?q='
def getPage(DOI):
    page = requests.get(f"{PAGEURL}{DOI}")
    print(page.content)
    return page