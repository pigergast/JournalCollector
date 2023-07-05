import Functions2

csv_file = 'journal-list.csv'
journal_list = Functions2.extract_journal_issn(csv_file)
print("The number of journals in the list:", len(journal_list))
print("The first 10 journals:", journal_list[:10])
