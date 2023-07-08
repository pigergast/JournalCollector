import Functions2

csv_file = 'journal-list.csv'
name_list = Functions2.extract_journal_list_col(csv_file, 1)
issn_list = Functions2.extract_journal_list_col(csv_file, 2)
print("The first three journal names:", name_list[:3])
print("The first three ISSNs:", issn_list[:3])

start_date = '2022/10/30'
end_date = '2023/07/10'

# Get the PMCID from PubMed Central

pmcid_list = []
pmcid_per_journal = []
progress = 0

for issn in issn_list:
    progress += 1
    temp_list = Functions2.get_journal_pmcids(issn, start_date, end_date)

    if temp_list is None:
        pmcid_per_journal.append(0)
    else:
        pmcid_list.extend(temp_list)
        pmcid_per_journal.append(len(temp_list))

    if progress % 10 == 0:
        print("Progress:", progress, "out of", len(issn_list))

print("The first three PMCID:", pmcid_list[:3])
print("The first three PMCID per journal:", pmcid_per_journal[:3])
print("Total number of PMCID:", len(pmcid_list))

# Get the PMID from PubMed

pmid_list = []
pmid_per_journal = []
progress = 0
for issn in issn_list:
    progress += 1
    temp_list = Functions2.get_journal_pmids(issn, start_date, end_date)

    if temp_list is None:
        pmid_per_journal.append(0)
    else:
        pmid_list.extend(temp_list)
        pmid_per_journal.append(len(temp_list))

    if progress % 10 == 0:
        print("Progress:", progress, "out of", len(name_list))

print("The first three PMID:", pmid_list[:3])
print("The first three PMID per journal:", pmid_per_journal[:3])
print("Total number of PMID:", len(pmid_list))

# Save to journal-list-report.csv
Functions2.write_journal_list_report(name_list, issn_list, pmid_per_journal, pmcid_per_journal)










