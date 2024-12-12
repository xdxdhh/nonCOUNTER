import json
import pandas as pd
import argparse
import numpy as np

# This will only run all the code and save outputs to some folder
# Then there will be different script that will evaluate the outputs

def pokus(folder, num):
    excel_file_path = "dataset/example1.xlsx"

    function_string = """
def process_data(excel_file_path):
    
    df = pd.read_excel(excel_file_path, sheet_name="input")
    print('defining')
    # Define month mapping
    months = [
        ("2022-01-01", "2022-01-31"), ("2022-02-01", "2022-02-28"), 
        ("2022-03-01", "2022-03-31"), ("2022-04-01", "2022-04-30"),
        ("2022-05-01", "2022-05-31"), ("2022-06-01", "2022-06-30"), 
        ("2022-07-01", "2022-07-31"), ("2022-08-01", "2022-08-31"), 
        ("2022-09-01", "2022-09-30"), ("2022-10-01", "2022-10-31"),
        ("2022-11-01", "2022-11-30"), ("2022-12-01", "2022-12-31")
    ]

    # Prepare an empty list for transformed rows
    processed_rows = []

    for _, row in df.iterrows():
        title = row["Title"]
        publisher = row["Publisher"]
        publisher_id = row["Publisher_ID"]

        for i, (start_date, end_date) in enumerate(months):
            month_value = row.iloc[4 + i]  # Metrics start from the 5th column
            processed_rows.append({
                "begin": start_date,
                "end": end_date,
                "titles": title,
                "Pages": month_value,
                "Publisher": publisher,
                "Publisher_ID": publisher_id
            })

    # Create the processed DataFrame
    processed_df = pd.DataFrame(processed_rows)

    # Save the processed DataFrame to a CSV file
    return processed_df.to_csv('filepath.csv', index=False)
"""

    local_vars = {}
    exec(function_string, globals(), local_vars)
    #exec(function_string)
    # Access the dynamically created function
    process_data = local_vars['process_data']

    # Call the function
    process_data(excel_file_path)


def call_function(string_function, input, output):
    local_vars = {}
    exec(string_function, globals(), local_vars)
    process_data = local_vars['process_data']
    process_data(input, output)

def evaluate_csvs(file, folder, output_folder):  # file with results from GPT, folder with true outputs
    with open(file) as f:
        results_data = [json.loads(line) for line in f.readlines()]

    for record in results_data:
        id = record[
            "custom_id"
        ]  # also could create universal util function that would do this, get the body and only the response
        print(f"id: {id}")
        try:
            code_string = record["response"]["body"]["choices"][0]["message"]["content"]
            if code_string.startswith("```python"):
                code_string = code_string[9:]  # Remove ```python
            if code_string.endswith("```"):
                code_string = code_string[:-3]  # Remove ```
            excel_file_path = f"{folder}/example{id}.xlsx"
            output_file_path = f"{output_folder}/output{id}.csv"
            call_function(code_string, excel_file_path, output_file_path)
        except Exception as e:
            print(f"Error: {e}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="todo", formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument(
        "--input",
        dest="input_file",
        required=True,
        help="Provide the path to the obtained results as jsonl.",
    )
    parser.add_argument("--folder", dest="folder", required=True, help="Pro")

    parser.add_argument("--output-folder", dest="output_folder", required=True, help="Folder to save the generated CSV files to.")

    args = parser.parse_args()

    evaluate_csvs(args.input_file, args.folder, args.output_folder)
