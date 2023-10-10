import urllib
import requests


def checkWiley(inputDoi):
    token = "7787c853-8908-4946-8107-050bcf22971a"
    apiUrl = "https://api.wiley.com/onlinelibrary/tdm/v1/articles/"
    headers = {'Wiley-TDM-Client-Token': token}
    doi = inputDoi
    # encode doi
    doi = urllib.parse.quote(doi, safe='')
    print("Encoded DOI:", doi)
    response = requests.get(f"{apiUrl}{doi}", headers=headers)
    if response.status_code == 200:
        return True
    else:
        return False