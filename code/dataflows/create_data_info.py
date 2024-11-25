import pandas as pd
import json
import numpy as np


# Script that iterates the folder with all examples and create a summarization JSON

nums = list(range(1,23))
print(nums)

data_info_list = []

for num in nums:
    df = pd.read_excel(f"dataset/example{num}.xlsx", sheet_name="info") #TODO parametrize
    first_row = df.iloc[0].replace({np.nan: None}).to_dict()  # Convert the first row to a dictionary
    
    # Ensure 'metrics' field is a list (empty if missing or null)
    metrics_list = []
    if "metrics" in first_row and first_row["metrics"]:
        # Split by commas, strip whitespace, and remove duplicates
        metrics_list = list(dict.fromkeys([m.strip() for m in first_row["metrics"].split(",")]))
    first_row["metrics"] = metrics_list  # Update the metrics field with the list

    # Ensure 'metadata' field is a list (empty if missing or null)
    metadata_list = []
    if "metadata" in first_row and first_row["metadata"]:
        metadata_list = list(dict.fromkeys([m.strip() for m in first_row["metadata"].split(",")]))
    first_row["metadata"] = metadata_list  # Update the metadata field with the list

    # Ensure 'title_identifiers' field is a list (empty if missing or null)
    title_identifiers_list = []
    if "title_identifiers" in first_row and first_row["title_identifiers"]:
        title_identifiers_list = list(dict.fromkeys([m.strip() for m in first_row["title_identifiers"].split(",")]))
    first_row["title_identifiers"] = title_identifiers_list  # Update the title_identifiers field with the list

    data_info_list.append(first_row)


# Convert the list of dictionaries to a JSON string
jsonfile = json.dumps(data_info_list, indent=4)  # indent=4 for better readability

#print(jsonfile)

# TODO parametrize
with open("data_info.json", "w") as outfile:
    outfile.write(jsonfile)