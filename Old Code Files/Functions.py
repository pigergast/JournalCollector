from bs4 import BeautifulSoup
import requests, re, os, csv, json
import urllib.parse
import tarfile
import shutil


def downloadPdf(url, title, path):
    response = requests.get(url)
    fileTitle = re.sub(r'[\\/*?:"<>|]', "", title)
    file = open(f"{path}/{fileTitle}", "wb")
    file.write(response.content)
    file.close()

def downloadTarGz(url, title):
    isExist = os.path.exists("../Downloads/tarGz")
    if not isExist:
        # Create a new directory because it does not exist
        os.makedirs("../Downloads/tarGz")
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


# not used yet but might be good in the future
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


def get_doi_from_pmcid(pmcid):
    url = f"https://www.ncbi.nlm.nih.gov/pmc/utils/idconv/v1.0/?ids=PMC{pmcid}"

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


import requests

def get_article_info(doi_list):
    article_types = []
    article_journals = []
    article_published_dates = []

    for doi in doi_list:
        api_url = f"https://api.crossref.org/v1/works/{doi}"
        response = requests.get(api_url)

        if response.status_code == 200:
            data = response.json()
            article_type = data['message']['type']
            article_journal = data['message']['short-container-title']
            article_journal = str(article_journal)
            article_journal = article_journal.replace("['", "")
            article_journal = article_journal.replace("']", "")

            # Extracting the timestamp from the license in the message part
            message_license = data['message'].get('license', [])
            license_timestamp = None
            if message_license:
                date_time = message_license[0].get('start', {}).get('date-time')
                if date_time:
                    license_timestamp = date_time[:10]
            if license_timestamp:
                article_published_date = license_timestamp

            article_types.append(article_type)
            article_journals.append(article_journal)
            article_published_dates.append(article_published_date)
        else:
            article_types.append(None)
            article_journals.append(None)
            article_published_dates.append(None)

    return article_types, article_journals, article_published_dates


def write_to_csv(dois, data_types, pmcids, types, journals, published_dates):
    with open('summary.csv', 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['DOI', 'PMCID', 'Published Journal', 'Published Date' ,'Article Type'])  # Write header

        for doi, data_type, pmcids, types, journals, published_dates in zip(dois, data_types, pmcids, types, journals, published_dates):
            writer.writerow([doi,pmcids,journals,published_dates, data_type])


def download_json_files(pmcid_list):
    output_folder = "JSON Files"

    # Create the output folder if it doesn't exist
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    jsonNum = 0

    for pmcid in pmcid_list:
        url = f"https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?db=pmc&id=PMC{pmcid}&retmode=json"
        response = requests.get(url)

        if response.status_code == 200:
            file_path = os.path.join(output_folder, f"{pmcid}.json")
            with open(file_path, "wb") as file:
                file.write(response.content)
            print(f"Downloaded {pmcid}.json")
            jsonNum += 1
        else:
            print(f"Failed to download {pmcid}.json")

    print(f"Downloaded {jsonNum} JSON files")


def downloadPdfFromPMCIDList(PMCIDList, folderName):
    # download PDFs
    print("-------------------")
    print("Downloading PDFs...")
    isExist = os.path.exists("../Downloads")
    if not isExist:
        # Create a new directory because it does not exist
        os.makedirs("../Downloads")
    # create folder if not exist
    isExist = os.path.exists(f"Downloads/{folderName}")
    if not isExist:
        # Create a new directory because it does not exist
        os.makedirs(f"Downloads/{folderName}")
    # go through each PMCIDs and get the PDFs
    # count number of successful and unsuccessful downloads
    successful = 0
    unsuccessful = 0
    download_records = []  # List to store download records for CSV report

    for pmcid in PMCIDList:
        print("Processing PMC" + pmcid)
        link = PMCPDFLinkExtractor(pmcid)
        if link is None:
            link = PMCTARGZLinkExtractor(pmcid)
            if link is None:
                print("No PDF/TAR.GZ link for PMC" + pmcid)
                unsuccessful += 1
                download_records.append([pmcid, "Unsuccessful"])  # Add record to download_records list
                continue
            else:
                successful += 1
                downloadTarGz(link, "PMC" + pmcid + ".tar.gz")
                tar = tarfile.open("Downloads/tarGz/PMC" + pmcid + ".tar.gz", "r:gz")
                # extract PDF from tar.gz
                for tarinfo in tar:
                    if tarinfo.name.endswith(".pdf"):
                        pdf_file = tar.extractfile(tarinfo.path)
                        with open(f"Downloads/{folderName}/PMC" + pmcid + ".pdf", "wb") as output_file:
                            shutil.copyfileobj(pdf_file, output_file)
                        break
                tar.close()
                download_records.append([pmcid, "Successful"])  # Add record to download_records list
                continue
        downloadPdf(link, "PMC" + pmcid + ".pdf", f"Downloads/{folderName}")
        successful += 1
        download_records.append([pmcid, "Successful"])  # Add record to download_records list

    print("-------------------")
    print("SUMMARY:")
    print("Number of successful downloads: " + str(successful))
    print("Number of unsuccessful downloads: " + str(unsuccessful))

    # Generate CSV report
    report_filename = f"Downloads/{folderName}/download_report.csv"
    with open(report_filename, "w", newline="") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["PMCID", "Status"])  # Write header
        writer.writerows(download_records)  # Write download records

    print("Download report generated: " + report_filename)