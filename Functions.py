from bs4 import BeautifulSoup
import requests, re, os, csv, json
import urllib.parse
# pip install lxml

PAGEURL = 'https://libgen.is/scimag/?q='


def getPDF(DOI):
    page = requests.get(f"{PAGEURL}{DOI}")
    soup = BeautifulSoup(page.text, "html.parser")
    downloadList = []
    mirrors = soup.find_all('ul', {"class": "record_mirrors"})
    if (len(mirrors) != 1):
        return False, "No PDF found"
    safeDOI = urllib.parse.quote(DOI, safe='')
    title = soup.find('a', href=f'/scimag/{safeDOI}').text
    for li in mirrors:
        for a in li.find_all('a'):
            link = a['href']
            if (link.startswith('http://library.lol')):
                downloadList.append(getDownloadLink(a['href']))
    # Go through each link in the download list and attempt to download. If download is successful, return true, else return false. If error occur, print exception
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
    file = open(f"Downloads/{fileTitle}", "wb")
    file.write(response.content)
    file.close()

def downloadTarGz(url, title):
    isExist = os.path.exists("Downloads/tarGz")
    if not isExist:
        # Create a new directory because it does not exist
        os.makedirs("Downloads/tarGz")
    response = requests.get(url)
    fileTitle = re.sub(r'[\\/*?:"<>|]', "", title)
    file = open(f"Downloads/tarGz/{fileTitle}", "wb")
    file.write(response.content)
    file.close()


def PMCPDFLinkExtractor(pmcId):
    response = requests.get(f"https://www.ncbi.nlm.nih.gov/pmc/utils/oa/oa.fcgi?id=PMC{pmcId}")
    soup = BeautifulSoup(response.text, "html.parser")
    #if there is no pdf link, skip
    if soup.find('link', format='pdf') is None:
        return None
    link = soup.find('link', format='pdf')['href'].replace('ftp://', 'https://')
    return link
def PMCTARGZLinkExtractor(pmcId):
    response = requests.get(f"https://www.ncbi.nlm.nih.gov/pmc/utils/oa/oa.fcgi?id=PMC{pmcId}")
    soup = BeautifulSoup(response.text, "html.parser")
    # if there is no pdf link, skip
    if soup.find('link', format='tgz') is None:
        return None
    link = soup.find('link', format='tgz')['href'].replace('ftp://', 'https://')
    return link



def get_journal_pmcids(dateRange):
    base_url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi"
    parameters = {
        "db": "pmc",
        "term": '"J Nurs Scholarsh"[jour] AND open access[filter] AND ' + dateRange,
        "retmode": "json",
        "retmax": 100000,  # Adjust the value based on your requirements
        "usehistory": "y"
    }

    response = requests.get(base_url, params=parameters)
    response_json = response.json()

    if 'esearchresult' not in response_json or 'idlist' not in response_json['esearchresult']:
        print("Error: Invalid API response")
        return []

    webenv = response_json['esearchresult']['webenv']
    query_key = response_json['esearchresult']['querykey']

    pmcid_list = []
    retstart = 0
    retmax = 10000  # Adjust the value based on your requirements

    while retstart <= int(response_json['esearchresult']['count']):
        fetch_parameters = {
            "db": "pmc",
            "query_key": query_key,
            "WebEnv": webenv,
            "retmode": "json",
            "retstart": retstart,
            "retmax": retmax
        }

        fetch_response = requests.get(base_url, params=fetch_parameters)
        fetch_json = fetch_response.json()

        if 'esearchresult' in fetch_json and 'idlist' in fetch_json['esearchresult']:
            pmcid_list.extend(fetch_json['esearchresult']['idlist'])
        else:
            print("Error: Invalid fetch response")

        retstart += retmax

    return pmcid_list


def get_pmid_from_pmcid(pmcid):
    url = f"https://www.ncbi.nlm.nih.gov/pmc/utils/idconv/v1.0/?ids=PMC{pmcid}"

    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise an exception for non-2xx status codes
        soup = BeautifulSoup(response.content, "lxml-xml")

        records = soup.find_all("record")
        if len(records) > 0:
            record = records[0]
            pmid = record.get("pmid")
            return pmid
    except requests.exceptions.RequestException as e:
        print("Error occurred:", str(e))

    return None


def fetch_article_info(pmid):
    url = f"https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?db=pubmed&id={pmid}"
    response = requests.get(url)

    try:
        response.raise_for_status()  # Check if the request was successful
        json_data = response.json()

        # Extract article title and type
        article_title = json_data["PubmedArticle"][0]["MedlineCitation"]["Article"]["ArticleTitle"]
        article_type = \
        json_data["PubmedArticle"][0]["MedlineCitation"]["Article"]["PublicationTypeList"]["PublicationType"][0]["UI"]

        return article_title, article_type
    except (requests.RequestException, KeyError) as e:
        print(f"Error fetching article info for PMID {pmid}: {e}")
        print("Response content:")
        print(response.text)  # Print the response content for inspection
        return None, None


def write_summary_csv(pmid_list):
    with open("summary.csv", "w", newline="", encoding="utf-8") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["PMID", "Article Title", "Article Type"])

        for pmid in pmid_list:
            article_title, article_type = fetch_article_info(pmid)
            writer.writerow([pmid, article_title, article_type])
            print(f"Saved info for PMID {pmid} to summary.csv")
