import Functions2
from multiprocessing import Pool

csv_file = 'journal-list.csv'
journal_list = Functions2.extract_journal_names(csv_file)
print("The number of journals in the list:", len(journal_list))
"""
start_date = "2022/10/30"
end_date = "2023/07/01"

pmid_list = []
progress = 0
for journal_name in journal_list:
    progress += 1
    pmids = Functions2.get_pmids_from_journal(journal_name, start_date, end_date)
    pmid_list.extend(pmids)
    if progress % 10 == 0:
        print(f"Progress: {progress}/{len(journal_list)}")

print("The number of PMIDs found:", len(pmid_list))
print("The first 10 PMIDs:", pmid_list[:10])

Functions2.write_array_to_csv(pmid_list)
"""
pmid_list = Functions2.extract_pmids_from_csv('metadata.csv')
print("The number of PMIDs found:", len(pmid_list))

pmcid_list = []
progress2 = 0
for pmid in pmid_list:
    progress2 += 1
    pmcid = Functions2.get_pmcid(pmid)
    if pmcid:
        print(pmcid)
        pmcid_list.append(pmcid)
    if progress2 % 100 == 0:
        print(f"Progress: {progress2}/{len(pmid_list)}")


Functions2.write_pmcid_to_csv(pmcid_list)