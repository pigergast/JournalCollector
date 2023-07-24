import requests
import csv
from urllib.parse import quote
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


def write_doi_download_report(doi_list, download_status_list):
    # Prepare the data as rows
    rows = zip(doi_list, download_status_list)

    # Define the column names
    column_names = ['DOI', 'Download Status']

    # Open the file in write mode
    with open('doi-download-report.csv', 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)

        # Write the column names as the first row
        writer.writerow(column_names)

        # Write the data rows
        writer.writerows(rows)

    print("Doi Download Report generated successfully!")


def write_journal_list_report(name_list, issn_list, pmid_per_journal, pmcid_per_journal):
    # Prepare the data as rows
    rows = zip(name_list, issn_list, pmid_per_journal, pmcid_per_journal)

    # Define the column names
    column_names = ['Journal Name', 'ISSN', 'PMID Per Journal', 'PMCID Per Journal']

    # Open the file in write mode
    with open('journal-list-report.csv', 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)

        # Write the column names as the first row
        writer.writerow(column_names)

        # Write the data rows
        writer.writerows(rows)

    print("Report generated successfully!")


def get_doi_from_pmid(pmid):
    url = f"https://www.ncbi.nlm.nih.gov/pmc/utils/idconv/v1.0/?tool=my_tool&email=my_email@example.com&ids={pmid}"
    response = requests.get(url)
    data = response.json()

    try:
        records = data['records']
        if len(records) > 0 and 'doi' in records[0]:
            doi = records[0]['doi']
            return doi
        else:
            return None
    except (KeyError, IndexError):
        return None