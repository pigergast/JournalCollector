import Functions2

csv_file = 'journal-list.csv'
journal_list = Functions2.extract_journal_issn(csv_file)
print("The number of journals in the list:", len(journal_list))
print("The first 10 journals:", journal_list[:10])

start_date = '2022/10/30'
end_date = '2023/07/01'

pmcid_list = []
progress = 0
for journal in journal_list:
    progress += 1
    pmcid_list.extend(Functions2.get_journal_pmcids(journal, start_date, end_date))
    if progress % 10 == 0:
        print(f"Progress: {progress}/{len(journal_list)}")

Functions2.write_pmcids_to_csv(pmcid_list)

print("The number of PMCIDs found from the PMC Open Access Subset:", len(pmcid_list))
print("The first 10 PMCIDs:", pmcid_list[:10])
