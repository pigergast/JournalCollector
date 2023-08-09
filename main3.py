import ScienceDirectFunctions
import CSVFunctions
import Article
# pip install certifi

if __name__ == '__main__':
    """ 
    # create a list of Article objects
    article_obj_list = []
    for i in range(len(issn_list)):
        article_obj_list.append(Article.Article(issn_list[i], pmid_list[i], doi_list[i]))
    
    print("The first Article object:", article_obj_list[0])
    print("The length of Article object list:", len(article_obj_list))
    """

    issn_list = CSVFunctions.extract_col_from_csv('master-list.csv', 0)
    pmid_list = CSVFunctions.extract_col_from_csv('master-list.csv', 1)
    doi_list = CSVFunctions.extract_col_from_csv('master-list.csv', 2)
    status_list = CSVFunctions.extract_col_from_csv('master-list.csv', 3)

    print("The first three ISSN:", issn_list[:3])
    print("The first three PMID:", pmid_list[:3])
    print("The first three DOI:", doi_list[:3])
    print("The first three status:", status_list[:3])

    pmcid_list = []
    progress = 0
    for pmid in pmid_list:
        progress += 1
        pmcid = ScienceDirectFunctions.convert_pmid_to_pmcid(pmid)

        print("Progress:", progress, "out of", len(pmid_list), "| PMID:", pmid)
        if pmcid is not None:
            pmcid_list.append(pmcid)
            # writing to csv file as generating
            CSVFunctions.add_to_csv_an_index_a_time(pmcid, 'pmcid-list.csv', 'PMC ID')
            print(pmcid)
        else:
            pmcid_list.append('None')
            CSVFunctions.write_array_to_csv('None', 'pmcid-list.csv', 'PMC ID')
            print('None')

    print("The first three PMCID:", pmcid_list[:3])
    print("Total number of PMCID:", len(pmcid_list))

    CSVFunctions.create_master_list(issn_list, pmid_list, doi_list, status_list, pmcid_list)




