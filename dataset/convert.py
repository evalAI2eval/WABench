import csv
import json

# Input CSV file path
csv_file_path = 'first_task.csv'
# Output JSON file path
json_file_path = 'output.json'

# Read the CSV file
with open(csv_file_path, mode='r') as csv_file:
    csv_reader = csv.DictReader(csv_file)
    data = []

    # Iterate over each row in the CSV
    for row in csv_reader:
        log_details = {}

        # Add the 'log' key and include all columns except 'Label' and 'Attack'
        for key, value in row.items():
            if key not in ['Label', 'Attack']:
                log_details[key] = value

        # Structure the final output with 'log' and include 'Label' and 'Attack' outside 'log'
        result = {
            'log': log_details,
            'label': row['Label'],
            'attack': row['Attack']
        }

        data.append(result)

# Write the result to a JSON file
with open(json_file_path, mode='w') as json_file:
    json.dump(data, json_file, indent=4)

