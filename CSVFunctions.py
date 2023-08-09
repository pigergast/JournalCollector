import csv

# FUnction to extract the journal list from the CSV file
def extract_journal_list_col(csv_file, col):
    journal_list = []

    with open(csv_file, newline='') as file:
        reader = csv.reader(file, delimiter=';')
        next(reader)  # Skip the header row

        for row in reader:
            journal_name = row[col]
            journal_list.append(journal_name)

    return journal_list

def extract_issn_pmid_list_col(csv_file, col):
    journal_list = []

    with open(csv_file, newline='') as file:
        reader = csv.reader(file, delimiter=',')
        next(reader)  # Skip the header row

        for row in reader:
            journal_name = row[col]
            journal_list.append(journal_name)

    return journal_list
def extract_article_obj_list_col(csv_file, col):
    journal_list = []

    with open(csv_file, newline='') as file:
        reader = csv.reader(file, delimiter=',')
        next(reader)  # Skip the header row

        for row in reader:
            journal_name = row[col]
            journal_list.append(journal_name)

    return journal_list

def get_status_array(filename):
    status_array = []

    try:
        with open(filename, 'r') as csv_file:
            csv_reader = csv.DictReader(csv_file)
            for row in csv_reader:
                if 'Status' in row:
                    status_array.append(row['Status'])
    except FileNotFoundError:
        print(f"File '{filename}' not found.")

    return status_array


def create_master_list(list1, list2, list3, list4, filename='master-list.csv'):
    # Prepare the data as rows
    rows = zip(list1, list2, list3, list4)

    # Define the column names
    column_names = ['ISSN', 'PMID', 'DOI', 'Available on ScienceDirect']

    # Open the file in write mode
    with open(filename, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)

        # Write the column names as the first row
        writer.writerow(column_names)

        # Write the data rows
        writer.writerows(rows)

    print("Status report generated successfully!")


def write_to_issn_pmid_list(list1, list2):
    # Prepare the data as rows
    rows = zip(list1, list2)

    # Define the column names
    column_names = ['ISSN', 'PMID']

    # Open the file in write mode
    with open('Old Code Files/issn-pmid-list.csv', 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)

        # Write the column names as the first row
        writer.writerow(column_names)

        # Write the data rows
        writer.writerows(rows)

    print("Report object list generated successfully!")


def write_obj_list_report(list1, list2, list3):
    # Prepare the data as rows
    rows = zip(list1, list2, list3)

    # Define the column names
    column_names = ['ISSN', 'DOI', 'Status']

    # Open the file in write mode
    with open('Old Code Files/status-report.csv', 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)

        # Write the column names as the first row
        writer.writerow(column_names)

        # Write the data rows
        writer.writerows(rows)

    print("Status report generated successfully!")


def add_doi_to_csv(doi, file_path='doi-list2.csv'):
    # Create a new CSV file if it doesn't exist
    with open(file_path, 'a', newline='') as csvfile:
        # Define the header of the CSV file if it's empty
        if csvfile.tell() == 0:
            fieldnames = ['DOI']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()

        # Append the DOI to the CSV file
        writer = csv.writer(csvfile)
        writer.writerow([doi])


def add_status_to_csv(status, file_path='status-list.csv'):
    # Create a new CSV file if it doesn't exist
    with open(file_path, 'a', newline='') as csvfile:
        # Define the header of the CSV file if it's empty
        if csvfile.tell() == 0:
            fieldnames = ['Status']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()

        writer = csv.writer(csvfile)
        writer.writerow([status])
