import Functions
import requests
import csv


if __name__ == '__main__':
    year = input("Enter the chosen year: ")  # e.g: 2016
    dois = Functions.getListOfDoiByYear(year)
    print("Number of DOIs found: " + str(len(dois)))

    with open('summary.csv', 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['DOI', 'Article Name', 'Status'])

        # loop through the first five dois and download the pdfs
        i = 0

        for doi in dois:

            if i == 5:
                break

            i += 1

            # check if the doi can be used to download or not
            check = Functions.getPDF(doi)

            # take the name of the article from the doi
            articleName = check[1]

            if check[0]:
                writer.writerow([doi, articleName,'Success'])
            else:
                writer.writerow([doi,articleName , 'Failed'])



