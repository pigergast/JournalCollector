import Functions2
import Article

csv_file = 'journal-list.csv'
name_list = Functions2.extract_journal_list_col(csv_file, 0)
issn_list = Functions2.extract_journal_list_col(csv_file, 2)
print("The first three journal names:", name_list[:3])
print("The first three ISSNs:", issn_list[:3])

start_date = '2022/10/30'
end_date = '2023/07/22'

# Get the PMID from PubMed
pmid_list = []
progress = 0
for issn in issn_list:
    progress += 1
    temp_list = Functions2.get_journal_pmids(issn, start_date, end_date)
    pmid_list.extend(temp_list)

    if progress % 10 == 0:
        print("Progress:", progress, "out of", len(name_list))

print("The first three PMID:", pmid_list[:3])
print("Total number of PMID:", len(pmid_list))

doi_list = []
progress = 0

for pmid in pmid_list:
    progress += 1
    temp_list = Functions2.get_doi_from_pmid(pmid)
    doi_list.extend(temp_list)

    if progress % 10 == 0:
        print("Progress:", progress, "out of", len(pmid_list))

print("The first three DOIs:", doi_list[:3])
print("Total number of DOIs:", len(doi_list))












