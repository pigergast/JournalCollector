import requests
import csv
from bs4 import BeautifulSoup


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


def get_pmcid(pmid):
    url = f"https://www.ncbi.nlm.nih.gov/pmc/utils/idconv/v1.0/?ids={pmid}"

    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise an exception for non-2xx status codes
        soup = BeautifulSoup(response.content, "lxml-xml")

        records = soup.find_all("record")
        if len(records) > 0:
            record = records[0]
            pmcid = record.get("pmcid")
            return pmcid
    except requests.exceptions.RequestException as e:
        print("Error occurred:", str(e))

    return None


def write_array_to_csv(array):
    # Prepare the data to be written
    data = [{'pmid': item} for item in array]

    # Define the fieldnames (column names) for the CSV file
    fieldnames = ['pmid']

    # Write the data to the CSV file
    with open('metadata.csv', 'w', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(data)


def extract_pmids_from_csv(filename):
    pmid_list = []

    with open(filename, 'r') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            pmid = row['pmid']
            pmid_list.append(pmid)

    return pmid_list


def write_pmcid_to_csv(pmcid_list):
    with open('metadata.csv', 'r', newline='') as file:
        reader = csv.DictReader(file)
        fieldnames = reader.fieldnames + ['pmcid']

        rows = []
        for row in reader:
            pmcid = pmcid_list.pop(0) if pmcid_list else ''
            row['pmcid'] = pmcid
            rows.append(row)

    with open('metadata.csv', 'w', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)



