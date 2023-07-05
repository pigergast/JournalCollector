import requests
import csv
from urllib.parse import quote
from bs4 import BeautifulSoup


def extract_journal_issn(csv_file):
    journal_list = []

    with open(csv_file, newline='') as file:
        reader = csv.reader(file, delimiter=';')
        next(reader)  # Skip the header row

        for row in reader:
            journal_name = row[2]
            journal_list.append(journal_name)

    return journal_list


def get_journal_pmcids(issn, start_date, end_date):
    base_url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi"
    parameters = {
        "db": "pmc",
        "term": f'"{issn}"[jour] AND ("{start_date}"[PubDate] : "{end_date}"[PubDate])',
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
            print("Error: Invalid fetch response of ", issn)


        retstart += retmax

    return pmcid_list


def write_pmcids_to_csv(array):
    # Prepare the data to be written
    data = [{'pmcid': item} for item in array]

    # Define the fieldnames (column names) for the CSV file
    fieldnames = ['pmcid']

    # Write the data to the CSV file
    with open('metadata.csv', 'w', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(data)
