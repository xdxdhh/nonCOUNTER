# batch eval -> 24h eval
from openai import OpenAI
from dotenv import load_dotenv
import pandas as pd
from prompts import get_test_prompt
import json
import argparse
import time
import jsonlines


load_dotenv()

client = OpenAI()

# TODO docstring
#will create input jsonl file

def get_data_description(folder, n: int, model, output_file):
    # Dictionary to store responses with example numbers as keys
    json_lines = []

    # Iterate through example files
    for num in range(1, n + 1):
        print(num)
        # Load the Excel file and get the "input" sheet
        excel_file_path = f"{folder}/example{num}.xlsx"
        df = pd.read_excel(excel_file_path, sheet_name="input")

        df = df.head(100)
        # Convert the DataFrame to a CSV-format string (keeping line breaks and commas intact)
        csv_data = df.to_csv(index=False)

        json_line = {
            "custom_id": f"{num}",
            "method": "POST",
            "url": "/v1/chat/completions",
            "body": {
                "model": f"{model}",
                "response_format": {"type": "json_object"},
                "messages": [
                    {"role": "system", "content": get_test_prompt()},
                    {"role": "user", "content": csv_data},
                ],
            },
        }

        json_lines.append(json_line)

    with jsonlines.open(output_file, mode="w") as writer:
        for json_line in json_lines:
            writer.write(json_line)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--folder", dest="folder", required=True, help="Path to folder with CSVs."
    )
    parser.add_argument(
        "--limit",
        dest="n",
        required=True,
        type=int,
        help="Use only examples up to n-th.",
    )  # TODO Make this optional
    parser.add_argument(
        "--model",
        dest="model",
        required=False,
        default="gpt-4o-mini",
        choices=["gpt-4o-mini", "gpt-4o"],
        help="Select the model to use. Choices are: gpt-4o-mini, gpt-4o.",
    )

    #TODO add argument for the name of the file.
    parser.add_argument(
        "--output",
        dest="output_file",
        required = True
    )

    # Iterate all if optional
    args = parser.parse_args()

    get_data_description(args.folder, args.n, args.model, args.output_file)
