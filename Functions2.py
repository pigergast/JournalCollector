import requests
import csv
from bs4 import BeautifulSoup


def extract_journal_issn(csv_file):
    journal_list = []

    with open(csv_file, newline='') as file:
        reader = csv.reader(file, delimiter=';')
        next(reader)  # Skip the header row

        for row in reader:
            journal_name = row[2]
            journal_list.append(journal_name)

    return journal_list

