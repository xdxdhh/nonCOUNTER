#will get jsonl file and process all csvs that are "small neough"import argparse
#will prepare jsonl file for batch procesing again
import csv
import json
import pandas as pd
import numpy as np
import argparse


def prepare_batch(input_file, output_file):
    with open(input_file) as f: #could be made a util function/jsonlines abstraction class
        input_data = [json.loads(line) for line in f.readlines()]

    for record in input_data:
        rows = record["rows"]
        cols = record["cols"]




if __name__ == '__main__':
    parser=argparse.ArgumentParser(description='todo', formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--input", dest="input_file", required=True, help="Provide the path to the obtained results as jsonl.")
    parser.add_argument("--output", dest="output_file", required=True, help="Provide the path to output the resulting jsonl file")

    args=parser.parse_args()

    prepare_batch(args.input_file, args.output_file)