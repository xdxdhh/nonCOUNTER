import pandas as pd
import json
import argparse
import jsonlines

# takes input jsonl file and enriches it
# it adds number of rows, number of columns

#output->jsonl file
#could also be used to get the delimtier

def enrich(input_file, output_file, folder):
    with open(input_file) as f:
        data = [json.loads(line) for line in f.readlines()]

    enriched_records = []
    for record in data:
        id = record["custom_id"]
        excel_file_path = f"{folder}/example{id}.xlsx"
        df = pd.read_excel(excel_file_path, sheet_name="input", header=None)
        rows, cols = df.shape
        print(id, rows, cols)

        data = json.loads(record["response"]["body"]["choices"][0]['message']['content'])
        data["rows"] = rows
        data["cols"] = cols
        data["id"] = id

        enriched_records.append(data)

    with jsonlines.open(output_file, mode="w") as writer:
        for json_line in enriched_records:
            writer.write(json_line)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", dest="input_file", required=True, help="todo.")
    parser.add_argument("--output", dest="output_file", required=True, help="Provide the path where to store the enriched jsonl.")
    parser.add_argument("--folder", dest="folder", required=True, help="folder with the data excels")

    # Iterate all if optional
    args = parser.parse_args()

    enrich(args.input_file, args.output_file, args.folder)