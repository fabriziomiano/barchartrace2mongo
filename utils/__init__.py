import datetime as dt
import json
import logging

import bar_chart_race as bcr
import pandas as pd
import requests
from pymongo import errors

from utils.config import (
    PCM_DATE_FMT, CHART_DATE_FMT, VARS_MAP, PERIOD_LABEL, URL_REGIONAL_DATA,
    PCM_DATE_KEY, REGIONAL_DATA_FILE, MONGO_URI
)


def get_logger(name):
    """
    Return a logger object of a given name
    :param name: str: logger name
    :return: logging.Logger object
    """
    logger = logging.getLogger(name)
    if not logger.handlers:
        logger.propagate = 1  # propagate to parent
        console = logging.StreamHandler()
        logger.addHandler(console)
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - [%(levelname)s] - %(message)s')
        console.setFormatter(formatter)
    return logger


UTILS_LOGGER = get_logger("Utils")
UTILS_LOGGER.setLevel(logging.INFO)


def mongo_connected(client):
    """
    Return True if mongo client is connected else False
    :param client: pymongo.MongoClient
    :return: bool
    """
    try:
        client.server_info()
        is_connected = True
    except errors.ServerSelectionTimeoutError as e:
        UTILS_LOGGER.error("{}".format(e))
        is_connected = False
    return is_connected


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
        dt.datetime.strptime(d, PCM_DATE_FMT).strftime(CHART_DATE_FMT)
        for d in dates
    ]
    bcr_data = {}
    for d in data:
        region = d["denominazione_regione"]
        if region not in bcr_data:
            bcr_data[region] = [d[var_to_bcr]]
        else:
            bcr_data[region].append(d[var_to_bcr])
    df = pd.DataFrame.from_dict(bcr_data, orient='index', columns=dates)
    df = df.transpose()
    UTILS_LOGGER.info("Making BCR")
    bcr_html = bcr.bar_chart_race(
        df=df,
        title=VARS_MAP[var_to_bcr]["title"],
        period_summary_func=my_period_summary_func(),
        period_label=PERIOD_LABEL,
        period_length=150,
        dpi=240
    )
    UTILS_LOGGER.info("Done making BCR")
    bcr_html = replace_video_tag_content(bcr_html)
    return bcr_html


def cache_data(data, data_filepath):
    """
    Save JSON-serialized object to file
    :param data:
    :param data_filepath:
    :return: None
    """
    with open(data_filepath, 'w') as data_file:
        json.dump(data, data_file)


def read_cached_data(data_filepath):
    """
    Read .json file
    :param data_filepath:
    :return: JSON-serialised object
    """
    with open(data_filepath, 'r') as data_file:
        data = json.load(data_file)
    return data


def get_regional_data():
    """
    Return the regional data from the "Protezione Civile" repository
    :return: dict
    """
    UTILS_LOGGER.info("Getting Data")
    data = {}
    try:
        response = requests.get(URL_REGIONAL_DATA, timeout=5)
        status = response.status_code
        if status == 200:
            regional_data = response.json()
            data["regional"] = sorted(
                regional_data, key=lambda x: x[PCM_DATE_KEY]
            )
            cache_data(data["regional"], REGIONAL_DATA_FILE)
        else:
            print("Could not get data: ERROR {}".format(status))
            data["regional"] = read_cached_data(REGIONAL_DATA_FILE)
    except Exception as e:
        print("Request Error {}".format(e))
        data["regional"] = read_cached_data(REGIONAL_DATA_FILE)
    UTILS_LOGGER.info("Done getting data")
    return data


def my_period_summary_func():
    """
    A user-defined function to add custom text to the axes each period.
    It must return a dictionary
    containing at a minimum the keys "x", "y", and "s" which will be
    passed to the matplotlib `text` method.
    :return: function
    """
    return lambda v, r: {
        'x': .99,
        'y': .18,
        's': f'Tot: {v.nlargest(6).sum():,.0f}',
        'ha': 'right',
        'size': 12
    }
