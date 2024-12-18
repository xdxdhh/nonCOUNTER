#will get jsonl file and process all csvs that are "small neough"import argparse
#will prepare jsonl file for batch procesing again
import json
import pandas as pd
import argparse
from prompts import get_simple_csv_prompt
import jsonlines


def prepare_batch(input_file, output_file, folder, model):
    with open(input_file) as f: #could be made a util function/jsonlines abstraction class
        input_data = [json.loads(line) for line in f.readlines()]

    json_lines = []

    for record in input_data:
        rows = record["rows"]
        cols = record["cols"]
        if rows < 20 and cols < 20: #TODO experimentally devise these numbers
            #maybe sum would be better as it would take very wides and also very long
            #get the input
            id = record["id"]
            excel_file_path = f"{folder}/example{id}.xlsx"
            df = pd.read_excel(excel_file_path, sheet_name="input")

            csv_data = df.to_csv(index=False)

            json_line = {
                "custom_id": id,
                "method": "POST",
                "url": "/v1/chat/completions",
                "body": {
                    "model": f"{model}",
                    "messages": [
                        {"role": "system", "content": get_simple_csv_prompt()},
                        {"role": "user", "content": csv_data},
                    ],
                },
            }

            json_lines.append(json_line)

    with jsonlines.open(output_file, mode="w") as writer:
        for json_line in json_lines:
            writer.write(json_line)


if __name__ == '__main__':
    parser=argparse.ArgumentParser(description='todo', formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--input", dest="input_file", required=True, help="Provide the path to the obtained results as jsonl.")
    parser.add_argument("--output", dest="output_file", required=True, help="Provide the path to output the resulting jsonl file")
    parser.add_argument("--folder", dest="folder", required=True, help="Pro")
    parser.add_argument("--model",dest="model",required=False,default="gpt-4o-mini",choices=["gpt-4o-mini", "gpt-4o"],
        help="Select the model to use. Choices are: gpt-4o-mini, gpt-4o.",
    )

    args=parser.parse_args()

    prepare_batch(args.input_file, args.output_file, args.folder, args.model)