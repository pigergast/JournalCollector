import csv


def extract_col_from_csv(csv_file, col):
    journal_list = []

    with open(csv_file, newline='') as file:
        reader = csv.reader(file, delimiter=',')
        next(reader)  # Skip the header row

        for row in reader:
            journal_name = row[col]
            journal_list.append(journal_name)

    return journal_list


def create_master_list(list1, list2, list3, list4, list5, filename='master-list2.csv'):
    # Prepare the data as rows
    rows = zip(list1, list2, list3, list4, list5)

    # Define the column names
    column_names = ['ISSN', 'PMID', 'DOI', 'Available on ScienceDirect', 'Available on PubMed Central']

    # Open the file in write mode
    with open(filename, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)

        # Write the column names as the first row
        writer.writerow(column_names)

        # Write the data rows
        writer.writerows(rows)

    print("Status report generated successfully!")


def write_multi_array_to_csv(list1, list2, filename, col1_name, col2_name):
    # Prepare the data as rows
    rows = zip(list1, list2)

    # Define the column names
    column_names = [col1_name, col2_name]

    # Open the file in write mode
    with open(filename, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)

        # Write the column names as the first row
        writer.writerow(column_names)

        # Write the data rows
        writer.writerows(rows)

    print("Report object list generated successfully!")


def write_array_to_csv(arr, file_path, col_name):
    # Create a new CSV file if it doesn't exist
    with open(file_path, 'a', newline='') as csvfile:
        # Define the header of the CSV file if it's empty
        if csvfile.tell() == 0:
            fieldnames = [col_name]
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()

        # Append the DOI to the CSV file
        writer = csv.writer(csvfile)
        writer.writerow([arr])

def add_to_csv_an_index_a_time(item, file_path, col_name):
    # Create a new CSV file if it doesn't exist
    with open(file_path, 'a', newline='') as csvfile:
        # Define the header of the CSV file if it's empty
        if csvfile.tell() == 0:
            fieldnames = [col_name]
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()

        # Append the DOI to the CSV file
        writer = csv.writer(csvfile)
        writer.writerow([item])


