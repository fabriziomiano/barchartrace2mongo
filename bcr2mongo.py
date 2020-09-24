import argparse
import datetime as dt

import bar_chart_race as bcr
import pandas as pd
import pymongo

from config import (
   BARCHART_RACE_QUERY, MONGO_URI, DB_NAME, COLLECTION_NAME, VARS_MAP
)
from data_utils import get_regional_data


def replace_video_tag_content(string_to_replace):
    """
    Replace <video> tag content with
    <video width="100%" height="auto" controls autoplay>
    :param string_to_replace: str
    :return: str
    """
    start = string_to_replace.find(">") + 1
    to = '<video width="100%" height="auto" controls autoplay>'
    return to + string_to_replace[start:]


def barchartrace_to_html(var_to_bcr):
    """
    Generate HTML files of the bar-chart races of all the relevant
    variables defined in the config
    :param: var_to_bcr: str
    :return: str
    """
    data = get_regional_data()["regional"]
    dates = sorted(set([d["data"] for d in data]))
    dates = [
        dt.datetime.strptime(d, "%Y-%m-%dT%H:%M:%S").strftime("%d %b")
        for d in dates
    ]
    bcr_data = {}
    print("Doing {}".format(var_to_bcr))
    for d in data:
        region = d["denominazione_regione"]
        if region not in bcr_data:
            bcr_data[region] = [d[var_to_bcr]]
        else:
            bcr_data[region].append(d[var_to_bcr])
    df = pd.DataFrame.from_dict(bcr_data, orient='index', columns=dates)
    df = df.transpose()
    bcr_html = bcr.bar_chart_race(
        df=df,
        title=VARS_MAP[var_to_bcr]["title"],
        period_summary_func=lambda v, r: {
            'x': .99,
            'y': .18,
            's': f'Tot: {v.nlargest(6).sum():,.0f}',
            'ha': 'right',
            'size': 12
        },
        period_label={
            'x': .99,
            'y': .25,
            'ha': 'right',
            'va': 'center'
        },
        period_length=150,
        dpi=240
    )
    bcr_html = replace_video_tag_content(bcr_html)
    return bcr_html


def barchartrace_to_mongo(var_to_bcr):
    """
    Create, or update, an item on mongodb like the following
    {
        "name": "barchart_race",
        "ts": dt.datetime.now(),
        "html_str": "<video ....."
    }
    :param: var_to_bcr: str
    :return: None
    """
    bcr_html = barchartrace_to_html(var_to_bcr)
    client = pymongo.MongoClient(MONGO_URI)
    db = client[DB_NAME]
    collection = db[COLLECTION_NAME]
    new_data = {
        "$set": {
            "name": var_to_bcr,
            "html_str": bcr_html,
            "ts": dt.datetime.now()
        }
    }
    BARCHART_RACE_QUERY["name"] = var_to_bcr
    collection.update_one(BARCHART_RACE_QUERY, new_data, upsert=True)


if __name__ == "__main__":
    PARSER_DESCRIPTION = (
        "Make a bar chart race of a given variable in the PC dataset"
        " e.g. 'totale_positivi'"
    )
    parser = argparse.ArgumentParser(description=PARSER_DESCRIPTION)
    parser.add_argument(
        '-v', '--var',
        help='provide the var name as per the PC dataset',
        required=True
    )
    args = parser.parse_args()
    VAR_TO_BCR = args.var
    barchartrace_to_mongo(VAR_TO_BCR)
