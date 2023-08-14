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
    progress = 8653
    # start from the index 8654 to the end of the pmid_list
    for i in range(8654, len(pmid_list)):
        progress += 1
        pmcid = ScienceDirectFunctions.convert_pmid_to_pmcid(pmid_list[i])

        print("Progress:", progress - 1, "out of", len(pmid_list), "| PMID:", pmid_list[i])

        if pmcid is not None:
            pmcid_list.append(pmcid)
            CSVFunctions.add_single_item_to_csv(pmcid, 'pmcid-list2.csv', 'PMCID')
            print(pmcid)
        else:
            pmcid_list.append('None')
            CSVFunctions.add_single_item_to_csv('None', 'pmcid-list2.csv', 'PMCID')
            print('None')

    print("The first three PMCID:", pmcid_list[:3])
    print("The length of PMCID list:", len(pmcid_list))






