import Functions
import requests
import csv


if __name__ == '__main__':
    year = input("Enter the chosen year: ")  # e.g: 2016
    dois = Functions.getListOfDoiByYear(year)
    print("Number of DOIs found: " + str(len(dois)))

    with open('summary.csv', 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['DOI', 'Status'])

        # loop through the first five dois and download the pdfs
        i = 0

        for doi in dois:

            if i == 5:
                break

            i += 1

            if Functions.getPDF(doi):
                writer.writerow([doi, 'Success'])
            else:
                writer.writerow([doi, 'Failed'])



