import requests
import csv
from bs4 import BeautifulSoup
from xml.etree import ElementTree as ET


# Function to get the PMID from PubMed
def get_journal_pmids(issn, start_date, end_date):
    base_url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi"
    parameters = {
        "db": "pubmed",
        "term": f'{issn} AND ("{start_date}"[Date - Publication] : "{end_date}"[Date - Publication])',
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

    pmid_list = []
    retstart = 0
    retmax = 10000  # Adjust the value based on your requirements

    while retstart <= int(response_json['esearchresult']['count']):
        fetch_parameters = {
            "db": "pubmed",
            "query_key": query_key,
            "WebEnv": webenv,
            "retmode": "json",
            "retstart": retstart,
            "retmax": retmax
        }

        fetch_response = requests.get(base_url, params=fetch_parameters)
        fetch_json = fetch_response.json()

        if 'esearchresult' in fetch_json and 'idlist' in fetch_json['esearchresult']:
            pmid_list.extend(fetch_json['esearchresult']['idlist'])
        else:
            print("Error: Invalid fetch response for", issn)
            return None

        retstart += retmax

    return pmid_list

# Function to get the DOI from the PMID
def pmid_to_doi(pmid):
    base_url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esummary.fcgi"
    params = {
        "db": "pubmed",
        "id": pmid,
    }

    try:
        response = requests.get(base_url, params=params)
        if response.status_code == 200:
            root = ET.fromstring(response.content)
            doi_item = root.find(".//Item[@Name='doi']")
            if doi_item is not None:
                return doi_item.text
            else:
                return None
        else:
            print(f"Error: Unable to retrieve DOI for PMID {pmid}. Status Code: {response.status_code}")
            return None
    except Exception as e:
        print(f"Error: An error occurred while processing the request: {str(e)}")
        return None


def CheckScienceDirectDoi(doi, apiKey, token):
    apiUrl = "https://api.elsevier.com/content/article/doi/";
    headers = {'X-ELS-APIKey': apiKey,
               'X-ELS-Insttoken': token,
               'Accept': 'application/json'}
    try:
        response = requests.get(f"{apiUrl}{doi}", headers=headers)
        print(response.status_code)
        return 'originalText' in response.json()['full-text-retrieval-response']
    except:
        return False

