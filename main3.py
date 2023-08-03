import ScienceDirectFunctions
import Article
# pip install certifi

if __name__ == '__main__':
    """ 
    csv_file = 'journal-list.csv'
    name_list = ScienceDirectFunctions.extract_journal_list_col(csv_file, 0)
    issn_list = ScienceDirectFunctions.extract_journal_list_col(csv_file, 2)
    print("The first three journal names:", name_list[:3])
    print("The first three ISSNs:", issn_list[:3])

    start_date = '2022/10/30'
    end_date = '2023/08/30'

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

    ScienceDirectFunctions.write_to_issn_pmid_list(issn_obj_list, pmid_list)

    csv_file = 'issn-pmid-list.csv'

    issn_list = ScienceDirectFunctions.extract_issn_pmid_list_col(csv_file, 0)
    pmid_list = ScienceDirectFunctions.extract_issn_pmid_list_col(csv_file, 1)

    print("The first two ISSNs:", issn_list[:2], "| Total number of ISSNs:", len(issn_list))
    print("The first two PMID:", pmid_list[:2], "| Total number of PMID:", len(pmid_list))

    doi_list = []
    progress = 0

    for pmid in pmid_list:
        progress += 1
        doi = ScienceDirectFunctions.pmid_to_doi(pmid)
        print("Progress:", progress, "out of", len(pmid_list), "| PMID:", pmid)
        if doi is not None:
            doi_list.append(doi)
            # writing to csv file as generating
            ScienceDirectFunctions.add_doi_to_csv(doi)
            print(doi)
        else:
            doi_list.append('None')
            ScienceDirectFunctions.add_doi_to_csv('None')
            print('None')

    print("The first three DOIs:", doi_list[:3])
    print("Total number of DOIs:", len(doi_list))
    
     # writing to article-obj-list.csv file as completed
    ScienceDirectFunctions.write_obj_list_report(issn_list, pmid_list, doi_list)
    """

    issn_list = ScienceDirectFunctions.extract_article_obj_list_col('article-obj-list.csv', 0)
    pmid_list = ScienceDirectFunctions.extract_article_obj_list_col('article-obj-list.csv', 1)
    doi_list = ScienceDirectFunctions.extract_article_obj_list_col('article-obj-list.csv', 2)

    print("The length of ISSN list:", len(issn_list))
    print("The length of PMID list:", len(pmid_list))
    print("The length of DOI list:", len(doi_list))

    print("---------------------------------")

    # create a list of Article objects
    article_obj_list = []
    for i in range(len(issn_list)):
        article_obj_list.append(Article.Article(issn_list[i], pmid_list[i], doi_list[i]))

    print("The first Article object:", article_obj_list[0])
    print("The length of Article object list:", len(article_obj_list))

    # CheckScienceDirectDoi('10.1016/j.profnurs.2023.05.006', '1d7b5a634d98e470780d362c4373e718')
