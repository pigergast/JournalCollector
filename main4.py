from LibgenFunctions import checkLibgen
import CSVFunctions

if __name__ == '__main__':

    issn_list = CSVFunctions.extract_col_from_csv('master-list2.csv', 0)
    pmid_list = CSVFunctions.extract_col_from_csv('master-list2.csv', 1)
    doi_list = CSVFunctions.extract_col_from_csv('master-list2.csv', 2)
    sciencedirect_list = CSVFunctions.extract_col_from_csv('master-list2.csv', 3)
    pubmedcentral_list = CSVFunctions.extract_col_from_csv('master-list2.csv', 4)

    # libGenList = []
    # progress = 0
    #
    # # start from 12373 to the end
    # for doi in doi_list:
    #     progress += 1
    #     print("Progress:", progress - 1, "out of", len(doi_list), "| DOI:", doi)
    #     temp_check = checkLibgen(doi)
    #     if temp_check is not None:
    #         libGenList.append(temp_check[0])
    #         CSVFunctions.add_single_item_to_csv(temp_check[0], 'libgen-list5.csv', 'LibGen')
    #         print(temp_check)
    #     else:
    #         libGenList.append('None')
    #         CSVFunctions.add_single_item_to_csv('None', 'libgen-list5.csv', 'LibGen')
    #         print('None')
    #
    # print("The length of LibGen list:", len(libGenList))

    libgen_list = CSVFunctions.extract_col_from_csv('libgen-list.csv', 0)

    # combine which master-list
    CSVFunctions.create_master_list(issn_list, pmid_list, doi_list, sciencedirect_list, pubmedcentral_list, libgen_list)





