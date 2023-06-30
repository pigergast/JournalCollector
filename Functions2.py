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
    query = f"{journal_name} AND ({start_date}[Date - Publication] : {end_date}[Date - Publication])"
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


def get_pmcid_and_doi_from_pmid(pmid):
    base_url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi"
    params = {
        "db": "pubmed",
        "id": pmid,
        "retmode": "xml"
    }

    try:
        response = requests.get(base_url, params=params)
        response.raise_for_status()  # Raise an exception for non-2xx status codes
        xml_data = response.text

        pmcid = None
        doi = None

        if "<ArticleId IdType=\"pmc\">" in xml_data:
            pmcid_start_index = xml_data.index("<ArticleId IdType=\"pmc\">") + len("<ArticleId IdType=\"pmc\">")
            pmcid_end_index = xml_data.index("</ArticleId>", pmcid_start_index)
            pmcid = xml_data[pmcid_start_index:pmcid_end_index]

        if "<ArticleId IdType=\"doi\">" in xml_data:
            doi_start_index = xml_data.index("<ArticleId IdType=\"doi\">") + len("<ArticleId IdType=\"doi\">")
            doi_end_index = xml_data.index("</ArticleId>", doi_start_index)
            doi = xml_data[doi_start_index:doi_end_index]

        return pmcid, doi
    except requests.exceptions.RequestException as e:
        print("Error occurred:", str(e))

    return None, None