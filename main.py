import tarfile
import Functions
from datetime import datetime

if __name__ == '__main__':
    # get PMCIDs
    # modify the startDate and endDate to get the PMCIDs from the PMC Open Access Subset
    startDate = "2022/09/01"  # the format is YYYY/MM/DD
    endDate = "2023/06/08"
    dateRange = '(' + startDate + '[PubDate] : ' + endDate + '[PubDate])'
    pmcids = Functions.get_journal_pmcids(dateRange)
    print("Number of PMCIDs found from the PMC Open Access Subset: " + str(len(pmcids)))
    print(pmcids)

    # download PDFs
    print("-------------------")
    print("Downloading PDFs...")
    #go through each PMCIDs and get the PDFs
    #count number of sucessful and unsuccessful downloads
    successful = 0
    unsuccessful = 0
    for pmcid in pmcids:
        print("Processing PMC" + pmcid)
        link = Functions.PMCPDFLinkExtractor(pmcid)
        if(link is None):
            link = Functions.PMCTARGZLinkExtractor(pmcid)
            if (link is None):
                print("No PDF/TAR.GZ link for PMC" + pmcid)
                unsuccessful += 1
                continue
            else:
                successful += 1
                Functions.downloadTarGz(link, "PMC" + pmcid + ".tar.gz")
                tar = tarfile.open("Downloads/tarGz/PMC" + pmcid + ".tar.gz", "r:gz")
                #extract PDF from tar.gz
                for tarinfo in tar:
                    if tarinfo.name.endswith(".pdf"):
                        tar.extract(tarinfo, path="Downloads")
                        break
                tar.close()
                continue
        Functions.downloadPdf(link, "PMC" + pmcid + ".pdf")
        successful += 1
    print("-------------------")
    print("SUMMARY:")
    print("Number of successful downloads: " + str(successful))
    print("Number of unsuccessful downloads: " + str(unsuccessful))

    # get doi from pmcid
    doi_list = []
    for pmcid in pmcids:
        doi = Functions.get_doi_from_pmcid(pmcid)
        doi_list.append(doi)
    print(len(doi_list))
    print(doi_list)
    # get metadata from doi using https://api.crossref.org/v1/works/
    types, journals, published_dates = Functions.get_article_info(doi_list)
    # write to csv
    Functions.write_to_csv(doi_list, types, pmcids, types, journals, published_dates)
    # download json files
    Functions.download_json_files(pmcids)








