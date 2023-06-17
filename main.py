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
        Functions.downloadPdf(link, "PMC" + pmcid + ".pdf")
        successful += 1

    print("SUMMARY:")
    print("Number of successful downloads: " + str(successful))
    print("Number of unsuccessful downloads: " + str(unsuccessful))

    # get metadata and create summary.csv
    # first get pmid from pmcid
    pmid_list = []
    for pmcid in pmcids:
        pmid = Functions.get_pmid_from_pmcid(pmcid)
        pmid_list.append(pmid)
    print("Numbers of PMID found from the PMC Open Access Subset: " + str(len(pmid_list)))
    print(pmid_list)
    # second get metadata from pmid
    # Functions.write_summary_csv(pmid_list)







