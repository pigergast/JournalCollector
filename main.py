import Functions
from datetime import datetime

if __name__ == '__main__':
    pmcids = Functions.get_journal_pmcids()
    print("PMCIDs from the PMC Open Access Subset:")
    print("Number of PMCIDs: " + str(len(pmcids)))
    print(pmcids)





