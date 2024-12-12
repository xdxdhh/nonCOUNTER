import json
import pandas as pd
import argparse
from prompts import get_code_generation_format_wide
import jsonlines

#will tkae data description as jsonl
#will send it to LLM - format A = long, format B = wide
#LLM will give the code to transform it into format A/B
#this will prepare the jsonl file to use

def prepare_batch(input_file, output_file, folder, model):
    with open(input_file) as f: #could be made a util function/jsonlines abstraction class
        input_data = [json.loads(line) for line in f.readlines()]

    json_lines = []

    for record in input_data:
            id = record["id"]
            excel_file_path = f"{folder}/example{id}.xlsx"
            df = pd.read_excel(excel_file_path, sheet_name="input")

            csv_data = df.to_csv(index=False)
            df = df.head(100)

            json_line = {
                "custom_id": str(id),
                "method": "POST",
                "url": "/v1/chat/completions",
                "body": {
                    "model": f"{model}",
                    "messages": [
                        {"role": "system", "content": get_code_generation_format_wide(record)},
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
    parser.add_argument("--input", dest="input_file", required=True, help="Provide the path to input jsonl file with data description.")
    parser.add_argument("--output", dest="output_file", required=True, help="Provide the path to output the resulting jsonl file")
    parser.add_argument("--folder", dest="folder", required=True, help="Folder with the input data to send to the llm")
    parser.add_argument("--model",dest="model",required=False,default="gpt-4o-mini",choices=["gpt-4o-mini", "gpt-4o"],
        help="Select the model to use. Choices are: gpt-4o-mini, gpt-4o.",
    )

    args=parser.parse_args()

    prepare_batch(args.input_file, args.output_file, args.folder, args.model)