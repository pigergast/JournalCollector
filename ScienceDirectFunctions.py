import requests

def CheckScienceDirectDoi(doi, apiKey):
    apiUrl = "https://api.elsevier.com/content/article/doi/";
    headers = {'X-ELS-APIKey': apiKey,
               'Accept': 'application/json'}
    try:
        response = requests.get(f"{apiUrl}{doi}", headers=headers)
        print(response.status_code)
        return 'originalText' in response.json()['full-text-retrieval-response']
    except:
        return False