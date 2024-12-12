#evaluate output csv - compare it to the correct csv
import json
import pandas as pd
import argparse
import jsonlines
import io


def compare_csvs(data, gold):
    pass


def evaluate_csvs(file, folder): #file with results from GPT, folder with true outputs
    with open(file) as f:
        results_data = [json.loads(line) for line in f.readlines()]

    for record in results_data:
        id = record["custom_id"] #also could create universal util function that would do this, get the body and only the response
        print(f"id: {id}")
        csv_string = record["response"]["body"]["choices"][0]['message']['content']
        csv_file = io.StringIO(csv_string)

        #reader = csv.DictReader(csv_file)
        #data = [row for row in reader]
        try:
            df = pd.read_csv(csv_file, index_col=None,sep=';')
            print(df.columns)
            print(df)
            print(len(df))
        except pd.errors.ParserError:
            print('Impossible to parse id ', id)



if __name__ == '__main__':
    parser=argparse.ArgumentParser(description='todo', formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--input", dest="input_file", required=True, help="Provide the path to the obtained results as jsonl.")
    parser.add_argument("--folder", dest="folder", required=True, help="Pro")

    args=parser.parse_args()

    evaluate_csvs(args.input_file, args.folder)