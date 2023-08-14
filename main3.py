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





