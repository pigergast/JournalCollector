import requests
import CSVFunctions
from bs4 import BeautifulSoup
from xml.etree import ElementTree as ET
import requests


def create_pmid_list():
    csv_file = 'journal-list.csv'
    name_list = CSVFunctions.extract_col_from_csv(csv_file, 1)
    issn_list = CSVFunctions.extract_col_from_csv(csv_file, 2)
    print("The first three journal names:", name_list[:3])
    print("The first three ISSNs:", issn_list[:3])

    start_date = '2022/10/30'
    end_date = '2023/08/30'

    pmid_list = []
    issn_obj_list = []
    progress = 0
    for issn in issn_list:
        progress += 1
        temp_list = get_journal_pmids(issn, start_date, end_date)

        if temp_list is not None:
            pmid_list.extend(temp_list)

            for i in range(len(temp_list)):
                issn_obj_list.append(issn)

        if progress % 10 == 0:
            print("Progress:", progress, "out of", len(name_list))

    print("The first three PMID:", pmid_list[:3])
    print("Total number of PMID:", len(pmid_list))
    print("The first three ISSNs for obj:", issn_obj_list[:3])
    print("Total number of ISSNs for obj:", len(issn_obj_list))

    return pmid_list, issn_obj_list

def create_doi_list():
    csv_file = 'issn-pmid-list.csv'

    issn_list = CSVFunctions.extract_col_from_csv(csv_file, 0)
    pmid_list = CSVFunctions.extract_col_from_csv(csv_file, 1)

    print("The first two ISSNs:", issn_list[:2], "| Total number of ISSNs:", len(issn_list))
    print("The first two PMID:", pmid_list[:2], "| Total number of PMID:", len(pmid_list))

    doi_list = []
    progress = 0

    for pmid in pmid_list:
        progress += 1
        doi = pmid_to_doi(pmid)
        print("Progress:", progress, "out of", len(pmid_list), "| PMID:", pmid)
        if doi is not None:
            doi_list.append(doi)
            # writing to csv file as generating
            CSVFunctions.write_array_to_csv([doi], 'doi-list.csv')
            print(doi)
        else:
            doi_list.append('None')
            CSVFunctions.write_array_to_csv(['None'], 'doi-list.csv')
            print('None')

    print("The first three DOIs:", doi_list[:3])
    print("Total number of DOIs:", len(doi_list))

    return doi_list


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


def create_journal_availability_list_sd():
    # create a status list
    instToken = 'a3869e2826f13c74d9c2f79f601f6607'
    apiKey = '1d7b5a634d98e470780d362c4373e718'

    doi_list = CSVFunctions.extract_col_from_csv('master-list.csv', 2)

    status_list = []
    progress = 0
    true = 0
    false = 0

    for doi in doi_list:
        progress += 1
        print("Progress:", progress, "out of", len(doi_list), "| DOI:", doi)

        status = CheckScienceDirectDoi(doi, apiKey, instToken)

        if status is True:
            status_list.append(status)
            print(status)
            true += 1
        else:
            status_list.append(status)
            print(status)
            false += 1

    print("The number of True:", true)
    print("The number of False:", false)
    print("The length of status list:", len(status_list))
    print("The first three status:", status_list[:3])

    return status_list


def convert_pmid_to_pmcid(pmid):
    base_url = "https://www.ncbi.nlm.nih.gov/pmc/utils/idconv/v1.0/"
    params = {"ids": pmid}

    response = requests.get(base_url, params=params)
    if response.status_code == 200:
        root = ET.fromstring(response.text)
        record = root.find(".//record")

        if record is not None:
            pmcid = record.get("pmcid")
            return pmcid
        else:
            return None
    else:
        print("Error:", response.status_code)
        return None




