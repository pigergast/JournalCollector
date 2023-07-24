from ScienceDirectFunctions import CheckScienceDirectDoi
import ScienceDirectFunctions

if __name__ == '__main__':

    csv_file = 'journal-list.csv'
    name_list = ScienceDirectFunctions.extract_journal_list_col(csv_file, 0)
    issn_list = ScienceDirectFunctions.extract_journal_list_col(csv_file, 2)
    print("The first three journal names:", name_list[:3])
    print("The first three ISSNs:", issn_list[:3])

    start_date = '2022/10/30'
    end_date = '2023/07/22'

    # Get the PMID from PubMed
    pmid_list = []
    issn_obj_list = []
    progress = 0
    for issn in issn_list:
        progress += 1
        temp_list = ScienceDirectFunctions.get_journal_pmids(issn, start_date, end_date)

        if temp_list is not None:
            pmid_list.extend(temp_list)

            for i in range(len(temp_list)):
                issn_obj_list.append(issn)

        if progress % 10 == 0:
            print("Progress:", progress, "out of", len(name_list))

    print("The first three PMID:", pmid_list[:3])
    print("Total number of PMID:", len(pmid_list))
    print("The first three ISSNs for obj:", issn_obj_list[:3])
    print("Total number of ISSNs for obj:", len(issn_obj_list))
    
    doi_list = []
    progress = 0

    for pmid in pmid_list:
        progress += 1
        doi = ScienceDirectFunctions.get_doi_from_pmid(pmid)

        if doi is not None:
            doi_list.append(doi)
        else:
            doi_list.append('None')

        if progress % 10 == 0:
            print("Progress:", progress, "out of", len(pmid_list))

    print("The first three DOIs:", doi_list[:3])
    print("Total number of DOIs:", len(doi_list))

    ScienceDirectFunctions.write_obj_list_report(issn_obj_list, pmid_list, doi_list)


    # CheckScienceDirectDoi('10.1016/j.profnurs.2023.05.006', '1d7b5a634d98e470780d362c4373e718')








