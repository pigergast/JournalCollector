import requests
import csv
from bs4 import BeautifulSoup



def extract_journal_list_col(csv_file, col):
    journal_list = []

    with open(csv_file, newline='') as file:
        reader = csv.reader(file, delimiter=';')
        next(reader)  # Skip the header row

        for row in reader:
            journal_name = row[col]
            journal_list.append(journal_name)

    return journal_list


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


def get_doi_from_pmid(pmid):
    url = f"https://www.ncbi.nlm.nih.gov/pmc/utils/idconv/v1.0/?ids={pmid}"

    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise an exception for non-2xx status codes
        soup = BeautifulSoup(response.content, "lxml-xml")

        records = soup.find_all("record")
        if len(records) > 0:
            record = records[0]
            doi = record.get("doi")
            return doi
    except requests.exceptions.RequestException as e:
        print("Error occurred:", str(e))

    return None


def CheckScienceDirectDoi(doi, apiKey):
    apiUrl = "https://api.elsevier.com/content/article/doi/";
    headers = {'X-ELS-APIKey': apiKey,
               'Accept': 'application/json'}
    try:
        response = requests.get(f"{apiUrl}{doi}", headers=headers)
        print(response.status_code)
        return 'originalText' in response.json()['full-text-retrieval-response']
    except:
        return False


def write_obj_list_report(list1, list2, list3):
    # Prepare the data as rows
    rows = zip(list1, list2, list3)

    # Define the column names
    column_names = ['ISSN', 'PMID', 'DOI']

    # Open the file in write mode
    with open('journal-obj-list.csv', 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)

        # Write the column names as the first row
        writer.writerow(column_names)

        # Write the data rows
        writer.writerows(rows)

    print("Report object list generated successfully!")