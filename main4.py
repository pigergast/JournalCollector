# from LibgenFunctions import checkLibgen
# import CSVFunctions
#
# if __name__ == '__main__':
#
#     issn_list = CSVFunctions.extract_col_from_csv('master-list4.csv', 0)
#     pmid_list = CSVFunctions.extract_col_from_csv('master-list4.csv', 1)
#     doi_list = CSVFunctions.extract_col_from_csv('master-list4.csv', 2)
#     sciencedirect_list = CSVFunctions.extract_col_from_csv('master-list4.csv', 3)
#     pubmedcentral_list = CSVFunctions.extract_col_from_csv('master-list4.csv', 4)
#     libgen_list = CSVFunctions.extract_col_from_csv('master-list4.csv', 5)
#
#
#     counter = 0
#     progress = -1
#     for libgen in libgen_list:
#         progress += 1
#         if libgen == "http://176.119.25.72/scimag/24707/Adoptive%20immunotherapy%20for%20nonsmall%20cell%20lung%20carcinoma_%20A%20fourth%20treatment%20modality%2C%20complicated%20radiation%20sensitizer%2C%20or%20none%20of%20the%20above%20%28Cancer%2C%20vol.%2078%2C%20issue%202%29%20%281996%29.pdf":
#             print("Found")
#             counter += 1
#             print(counter)
#             print(libgen)
#             libgen_list[progress] = "None"
#
#
#
#
#
#     # libGenList = []
#     # progress = 0
#     #
#     # # start from 12373 to the end
#     # for doi in doi_list:
#     #     progress += 1
#     #     print("Progress:", progress - 1, "out of", len(doi_list), "| DOI:", doi)
#     #     temp_check = checkLibgen(doi)
#     #     if temp_check is not None:
#     #         libGenList.append(temp_check[0])
#     #         CSVFunctions.add_single_item_to_csv(temp_check[0], 'libgen-list5.csv', 'LibGen')
#     #         print(temp_check)
#     #     else:
#     #         libGenList.append('None')
#     #         CSVFunctions.add_single_item_to_csv('None', 'libgen-list5.csv', 'LibGen')
#     #         print('None')
#     #
#     # print("The length of LibGen list:", len(libGenList))
#
#
#
#     # combine which master-list
#     CSVFunctions.create_master_list(issn_list, pmid_list, doi_list, sciencedirect_list, pubmedcentral_list, libgen_list)
#
#
#
#
#
