import csv


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
