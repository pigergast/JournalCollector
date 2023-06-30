import Functions2

csv_file = 'journal-list.csv'
journal_list = Functions2.extract_journal_names(csv_file)
print("The number of journals in the list:", len(journal_list))

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

