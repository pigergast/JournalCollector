class Article:
    def __init__(self, issn, doi, pmid):
        self.issn = issn
        self.doi = doi
        self.pmid = pmid

    def __str__(self):
        return f"ISSN: {self.issn}, DOI: {self.doi}, PMID: {self.pmid}."


