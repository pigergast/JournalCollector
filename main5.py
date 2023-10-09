import urllib

import requests

if __name__ == '__main__':
    token = "7787c853-8908-4946-8107-050bcf22971a"
    apiUrl = "https://api.wiley.com/onlinelibrary/tdm/v1/articles/"
    headers = {'Wiley-TDM-Client-Token': token}
    doi = "10.1111/1467-923X.12168"
    #encode doi
    doi = urllib.parse.quote(doi, safe='')
    print(doi)
    response = requests.get(f"{apiUrl}{doi}", headers=headers)
    print(response.status_code)


