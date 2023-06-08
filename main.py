import requests
from bs4 import BeautifulSoup

import Functions
from datetime import datetime

if __name__ == '__main__':
    # modify the startDate and endDate to get the PMCIDs from the PMC Open Access Subset
    startDate = "2022/09/01"  # the format is YYYY/MM/DD
    endDate = "2023/06/08"
    dateRange = '(' + startDate + '[PubDate] : ' + endDate + '[PubDate])'
    pmcids = Functions.get_journal_pmcids(dateRange)
    print("PMCIDs from the PMC Open Access Subset:")
    print("Number of PMCIDs: " + str(len(pmcids)))
    print(pmcids)
    #go through each PMCIDs and get the PDFs
    #count number of sucessful and unsuccessful downloads
    successful = 0
    unsuccessful = 0
    for pmcid in pmcids:
        print("Processing PMC" + pmcid)
        link = Functions.PMCLinkExtractor(pmcid)
        if(link is None):
            print("No PDF link for PMC" + pmcid)
            unsuccessful += 1
            continue
        Functions.downloadPdf(link, "PMC" + pmcid + ".pdf")
        successful += 1
    print("Number of successful downloads: " + str(successful))
    print("Number of unsuccessful downloads: " + str(unsuccessful))





