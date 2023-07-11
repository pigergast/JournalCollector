# JournalCollector

### PubMed: 

Number of PMID found: 12669 pmids.

Query Format: issn number + time range.

Example: `1527-6546 AND ("2022/10/30"[Date - Publication] : "2023/07/10"[Date - Publication]) `

Result: The above query returns 124 articles. However, most of the articles are not open access. 
If we want to get only open-access articles, we need to add the following filter to the query: ` AND "Free Full Text"[filter]`
Then, it will return 31 open-access articles.

List of ISSN with no item found during the time range: 
- 1043-4542, 0813-0531, 0103-2100.

### PubMed Central:

Number of PMCID found: 1336 pmcids.

Query Format: issn number + time range 

Example: `"1527-6546"[jour] AND ("2022/10/30"[PubDate] : "2023/07/10"[PubDate])`

Result: this query returns 10 open-access articles.

List of ISSN with no item found during the time range: 
- 0730-7659, 1320-7881, 0893-2190, 1682-3141, 0148-4834, 0031-5990, 0279-5442, 0161-9268. 
- 1037-6178, 1043-4542, 0190-535X, 1466-7681,0161-2840, N/A, 1940-4921, 1755-6678,0278-4807.
- 0899-5885, 0279-3695, 1012-5302, 1539-0136, 1092-1095, 2005-3673, 0887-9311, 2640-5237, 0813-0531. 
- 556-3693, 2047-3087, 0022-0124, 0103-2100, 0744-6020, 0737-0016, 1526-744X, 0001-2092, 1592-5986, 1541-6577.

### How to download the articles:

1. To download the pdf version of an article, we need its PMCID.
2. Then, use this API link: https://www.ncbi.nlm.nih.gov/pmc/utils/oa/oa.fcgi?id=PMC5334499
3. Put the PMCID in the id parameter. And get the downloaded part: `ftp.ncbi.nlm.nih.gov/pub/pmc/oa_pdf/8e/71/WJR-9-27.PMC5334499.pdf`
4. Add it with `https://` + `ftp.ncbi.nlm.nih.gov/pub/pmc/oa_pdf/8e/71/WJR-9-27.PMC5334499.pdf` to create a downloaded link.
5. The complete link: https://ftp.ncbi.nlm.nih.gov/pub/pmc/oa_pdf/8e/71/WJR-9-27.PMC5334499.pdf
5. Then, we can download the pdf file.