import urllib
import requests
import CSVFunctions
import WileyFunctions as wf

if __name__ == '__main__':
    # token = "7787c853-8908-4946-8107-050bcf22971a"
    # apiUrl = "https://api.wiley.com/onlinelibrary/tdm/v1/articles/"
    # headers = {'Wiley-TDM-Client-Token': token}
    # doi = "10.1111/1467-923X.12168"
    # #encode doi
    # doi = urllib.parse.quote(doi, safe='')
    # print(doi)
    # response = requests.get(f"{apiUrl}{doi}", headers=headers)
    # print(response.status_code)

    # extract doi from master-list
    doi_list = CSVFunctions.extract_col_from_csv('master-list100.csv', 2)

    # encoding doi list
    wiley_list = []
    progress = 10234

    for doi in doi_list[10234:]:
        progress += 1
        print("Progress:", progress - 1, "out of", len(doi_list), "| DOI:", doi)
        if doi != 'None':
            temp = wf.checkWiley(doi)

            if temp is True:
                wiley_list.append('True')
                CSVFunctions.add_single_item_to_csv('True', 'wiley-list2.csv', 'Wiley')
                print('True')
            else:
                wiley_list.append('None')
                CSVFunctions.add_single_item_to_csv('None', 'wiley-list2.csv', 'Wiley')
                print('None')
        else:
            wiley_list.append('None')
            CSVFunctions.add_single_item_to_csv('None', 'wiley-list2.csv', 'Wiley')
            print('None')

    print("The length of Wiley list:", len(wiley_list))
    CSVFunctions.write_array_to_csv(wiley_list, 'wiley-list-total.csv', 'Wiley')





