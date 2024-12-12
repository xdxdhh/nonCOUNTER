from typing import Dict

def get_test_prompt():
    prompt = """
        You are a data analyst helping libraries. A librarian will provide you with a CSV file containing usage statistics from a specific platform that they received. Your goal is to describe this file and return the description in a JSON format.
---------------------------------------
This is example output JSON:
  {
        "begin_month": "07-21",
        "end_month": "06-22",
        "metrics": [
            "Title Playbacks",
            "Views"
        ],
        "titles": 1,
        "title_identifiers": ["ISBN"],
        "english": 1,
        "granularity": "monthly",
        "metadata": [
            "Content Provider",
            "Year of Publishing",
            "Platform"
        ],
        "simple" : 0,
    },
---------------------------
You are to fill the keys accordingly:
- begin_month: The first month for which usage statistics are included, in the format MM-YY.
- end_month: The last month for which usage statistics are included, in the format MM-YY.
- metrics: Different usage statistics described in the report, such as Hits, Page Views, or Visitors. Include them exactly as they appear in the report. If there are none, this should be an empty list.
- titles: 1 if the report includes granular usage statistics about multiple titles (e.g., books, magazines, audiobooks), or 0 if it only includes summary data (i.e., combined for all titles).
- titles_identifiers: If titles is 1, this should be a list of all identifiers used to define the titles. Choices include: DOI, ISBN, Print_ISSN, Online_ISSN, URI, and Proprietary (for any other identifiers). If there are no identifiers, this should be an empty list.
- english: 1 if the statistics are in English, or 0 if they are in another language.
- granularity: The time granularity of the usage data. Options are: daily, monthly, quarterly, yearly, or other.
- metadata: If the report contains per-title data, this should list additional metadata fields provided for each title (e.g., Publisher, Year of Publishing). If there is no metadata, this should be an empty list.
- simple: Should be either 0 or 1. It should be 1 if the CSV file does not include anything unnecessary except the neccesary fields, it does not have any empty rows or columns, and can be easily parsed.
------------------

The CSV may contain irrelevant information that is neither metrics nor metadata. Ignore such fields.
The structure of the CSV may be non-standard; for example, the first row might not be a header.
Return only one JSON object as the output.

"""
    return prompt


def get_simple_csv_prompt():
    prompt = """
    You are a librarian assistant, and you help librarians with understanding usage statistics. Unfortunately, many platforms do not provide their usage statistics in COUNTER compliant format and users are confused.
You are given a csv with usage data from one such platform. Your goal is to transform the data and output a different, COUNTER compliant csv.
More specific instructions:

The output CSV file should include the following seven columns: start, end, title, metric, other, title_ids, value.
In the columns, the following information should be provided:
start = start of month, in YYYY-MM-DD format;
end = end of month, in YYYY-MM-DD format;
title = title of the publication (e.g. book title, video name) for which is the metric reported, can be empty;
metric = the reported metric, should never be empty;
other= metadata of the given record, in format Metadata1:Value1|Metadata2:Value2, can be empty;
title_ids = identifiers of the given title in format TitleID1:Value1|TitleIID2:Value 2, can be empty;
value = value of the metric, should never be empty, if it is empty in the input transform it to 0;

You can see 3 examples here:
--------------
This is an example input CSV:

Title,Metric,Publisher,Success,Jan 2021,Feb 2021
Irish History,Sessions,Brepolis,Success,11,12
Medieval Bibliography,Sessions,Brepolis,Success,17,18

And this is the expected output:
start;end;title;metric;other;title_ids;value
2021-01-01;2021-01-31;Irish History;Sessions;Publisher:Brepolis;;11
2021-02-01;2021-02-30;Irish History,Sessions;Publisher:Brepolis;;12
2021-01-01;2021-01-31;Medieval Bibliography;Sessions;Publisher:Brepolis;;17
2021-02-01;2021-02-30;Medieval Bibliography;Irish History;Sessions;Publisher:Brepolis;;18
--------------
input CSV:

SciFinder Web,,,,,
Site Name,Category,Class,JAN 2022,FEB 2022,MAR 2022
Org1,SEARCHES,COMMERCIAL SOURCE,9,4,2
Org1,SEARCHES,REACTION,125,107,45
Org1,SEARCHES,REFERENCE,73,50,49
Org1,SEARCHES,Result,207,161,96

expected output:
start;end;title;metric;other;title_ids;value
2022-01-01;2021-01-31;;COMMERCIAL SOURCE;;;9
2021-02-01;2021-02-28;,COMMERCIAL SOURCE;;;4
2021-03-01;2021-03-31;;COMMERCIAL SOURCE;;;2
2022-01-01;2021-01-31;;REACTION;;;125
2021-02-01;2021-02-28;,REACTION;;;107
2021-03-01;2021-03-31;;REACTION;;;45
2022-01-01;2021-01-31;;REFERENCE;;;73
2021-02-01;2021-02-28;,REFERENCE;;;50
2021-03-01;2021-03-31;;REFERENCE;;;49
--------------

If there is one metric that is only a different version of another metric (e.g. absolute value and percent value) or one metric which is just a sum of other metrics, do not include it.
Only output the output CSV, without any comments or code. Use ; as the csv delimiter.

"""
    return prompt

def get_simple_csv_prompt_no_titles(): #TODO make this without titles
    prompt = """
    You are a librarian assistant, and you help librarians with understanding usage statistics. Unfortunately, many platforms do not provide their usage statistics in COUNTER compliant format and users are confused.
You are given a csv with usage data from one such platform. Your goal is to transform the data and output a different, COUNTER compliant csv.
More specific instructions:

The output CSV file should include the following seven columns: start, end, title, metric, other, title_ids, value.
In the columns, the following information should be provided:
start = start of month, in YYYY-MM-DD format;
end = end of month, in YYYY-MM-DD format;
title = title of the publication for which is the metric reported, can be empty;
metric = the reported metric, should never be empty;
other= metadata of the given record, in format Metadata1:Value1|Metadata2:Value2, can be empty;
title_ids = identifiers of the given title in format TitleID1:Value1|TitleIID2:Value 2, can be empty;
value = value of the metric, should never be empty;
--------------
This is an example input CSV:

Title,Metric,Publisher,Success,Jan 2021,Feb 2021
Irish History,Sessions,Brepolis,Success,11,12
Medieval Bibliography,Sessions,Brepolis,Success,17,18

And this is the expected output:
start;end;title;metric;other;title_ids;value
2021-01-01;2021-01-31;Irish History;Sessions;Publisher:Brepolis;;11
2021-02-01;2021-02-30;Irish History,Sessions;Publisher:Brepolis;;12
2021-01-01;2021-01-31;Medieval Bibliography;Sessions;Publisher:Brepolis;;17
2021-02-01;2021-02-30;Medieval Bibliography;Irish History;Sessions;Publisher:Brepolis;;18
--------------

Only output the output CSV, without any comments or code. Use ; as the csv delimiter.

"""
    return prompt



def get_csv_generation_format_wide(data_description : Dict) -> str:
    prompt = ""
    return prompt


def get_code_generation_format_wide(data_description : Dict) -> str:
    #todo for not monthly granular do something different
    #todo for not english ones do something different

    #TODO Pak toto zkusit i pro csv generation
    prompt = """
    User will give you CSV data about usage statistics from e-resources, and your goal is to generate python code to transform the data into standardized format.
    The csv should have the following columns: begin, end, """
    if data_description["titles"] != 0:
        prompt += "titles, "
        for identifier in data_description["title_identifiers"]:
            prompt += f"{identifier}, "

    for metric in data_description["metrics"]:
        prompt += f"{metric}, "
 
    for metadata in data_description["metadata"]:
        prompt += f"{metadata}, "

    prompt += f""". \n Begin and end should have the beginning of month and end of month in YYYY-MM-DD format, so e.g. 2020-12-01(begin) and 2020-12-31(end).
    There should be one row for every month, with the first month being {data_description['begin_month']} and the last month being {data_description['end_month']}.
    Please keep in mind that if the csv is longer than 100 rows, user will only give you first 100 rows, but the code should process all of them.

    Fill in the following template and return only the code, assum that pandas is already imported as pd and numpy as np:
    -----------------------
    def process_data(excel_file_path, output_file_path):
        df = pd.read_excel(excel_file_path, sheet_name="input")

        # Your code goes here.
        # Your goal is to create processed_df which will store the output

        return processed_df.to_csv(output_file_path)
    ---------------------------
    """


    return prompt
