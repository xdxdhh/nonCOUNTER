def get_test_prompt():
    prompt = """
        You are data analyst helping in libraries. Librarian will give you CSV file, with usage statistics from certian platform, which he received. Your goal is to describe this file and return the description in a JSON format.
---------------------------------------
This is example output JSON:
  {
        "begin_month": "07-21",
        "end_month": "06-22",
        "metrics": [
            "Title Playbacks"
        ],
        "multiple_titles": 1,
        "title_identifiers": null,
        "english": 1,
        "granularity": "monthly",
        "metadata": [
            "Content Provider",
            "YOP",
            "Platform"
        ]
    },
---------------------------
You are to fill the keys accordingly:
- begin_month: The first month for which are usage statistics included, in format MM-YY.
- end_month: The last month for which are usage statistics included, in format MM-YY.
- metrics: Different usage statistics that are described in the report, they are different in each csv, for example: Hits, Page Views, Visitors. Include them as they are in the report.
- multiple_titles: 1 if the report includes data about multiple titles(e.g. it has names of books, resources), 0 if its only summary usage data.
- title_identifiers: If the report has titles (so multiple_titles = 1) and not only summary information, this should be list of all title identifiers used in the usage statistics, choices are: DOI, ISBN, Print_ISSN, Online_ISSN, Proprietary, URI.
- english: 1 if the statistics are in english, 0 if they are in different language.
- granularity: The usage data granularity, options are: daily, monthly, quaterly, yearly, other.
- metadata: If there are titles included in the usage statistics, there may be more information associated with them (this information will be provided for all titles) (usually e.g. Publisher, Year of publishing), metadata should include list of all those.
------------------
Keep in mind that there may be many irrelevant information in the csv, which are neither metrics not metadata.

Return only 1 JSON.

"""
    return prompt
