import argparse
import datetime as dt
import logging
import sys

import pymongo

from utils import get_logger, barchartrace_to_html, mongo_connected
from utils.config import (
    MONGO_URI, DB_NAME, COLLECTION_NAME, ENV, BARCHART_DB_KEY
)

CLIENT = pymongo.MongoClient(MONGO_URI)
DB = CLIENT[DB_NAME]
COLLECTION = DB[COLLECTION_NAME]


def barchartrace_to_mongo(var_to_bcr):
    """
    Create, or update, an item on mongodb like the following
    {
        "_id": "barchart_race",
        "ts": dt.datetime.now(),
        "html_str": "<video ....."
    }
    :param: var_to_bcr: str
    :return: None
    """
    bcr_html = barchartrace_to_html(var_to_bcr)
    new_data = {
        "$set": {
            BARCHART_DB_KEY: var_to_bcr,
            "html_str": bcr_html,
            "ts": dt.datetime.now()
        }
    }
    main_logger.info(
        "Writing {} bcr to collection {}".format(var_to_bcr, COLLECTION_NAME)
    )
    COLLECTION.update_one({BARCHART_DB_KEY: var_to_bcr}, new_data, upsert=True)


if __name__ == "__main__":
    main_logger = get_logger(name="main")
    main_logger.setLevel(logging.INFO)
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
    main_logger.info("=" * 20)
    if ENV is not None:
        main_logger.info("ENVIRONMENT: {}".format(ENV))
    main_logger.info("Doing {}".format(VAR_TO_BCR))
    if not mongo_connected(client=CLIENT):
        main_logger.error("Check mongo connection")
        sys.exit(1)
    barchartrace_to_mongo(VAR_TO_BCR)
    main_logger.info("Done")
    main_logger.info("=" * 20)
