import requests
import csv


def extract_journal_names(csv_file):
    journal_list = []

    with open(csv_file, newline='') as file:
        reader = csv.reader(file, delimiter=';')
        next(reader)  # Skip the header row

        for row in reader:
            journal_name = row[0]
            journal_list.append(journal_name)

    return journal_list


def get_pmids_from_journal(journal_name, start_date, end_date):
    base_url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi"
    query = f"{journal_name} AND ({start_date}[Date - Publication] : {end_date}[Date - Publication]) AND Free Full " \
            f"Text[filter]"
    params = {
        "db": "pubmed",
        "term": query,
        "retmax": 100000,  # Adjust as per your requirement (maximum is 100,000)
        "retmode": "json"
    }

    response = requests.get(base_url, params=params)
    data = response.json()

    if "error" in data:
        print(f"Error: {data['error']}")
        return []

    pmids = data["esearchresult"].get("idlist", [])
    return pmids


