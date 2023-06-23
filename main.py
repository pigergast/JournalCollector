import tarfile
import Functions
import shutil
if __name__ == '__main__':
    # get PMCIDs
    # modify the startDate and endDate to get the PMCIDs from the PMC Open Access Subset
    startDate = "2022/09/01"  # the format is YYYY/MM/DD
    endDate = "2023/06/08"
    dateRange = '(' + startDate + '[PubDate] : ' + endDate + '[PubDate])'
    pmcids = Functions.get_journal_pmcids(dateRange)
    print("Number of PMCIDs found from the PMC Open Access Subset: " + str(len(pmcids)))
    print(pmcids)

    Functions.downloadPdfFromPMCIDList(pmcids, "pdfs")
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








