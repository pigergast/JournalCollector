import Functions
import requests
if __name__ == '__main__':
    year = input("Enter the chosen year: ")  # e.g: 2021
    dois = Functions.getListOfDoiByYear(year)
    print(dois)
    print(Functions.getPDF('10.1111/jnu.12551'))

