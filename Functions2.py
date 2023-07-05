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


def write_pmcids_to_csv(arr, filename):
    column_name = "PMCID"
    formatted_string = column_name + ","

    for number in arr:
        formatted_string += "\n" + number + ","

    with open(filename, "w") as file:
        file.write(formatted_string)


def extract_pmcids_from_csv(filename):
    pmcids = []

    with open(filename, "r") as file:
        reader = csv.DictReader(file)
        for row in reader:
            number = row["PMCID"].strip()
            if number != "":
                pmcids.append(number)

    return pmcids
