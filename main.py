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





