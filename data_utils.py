import json

import requests

from config import URL_REGIONAL_DATA, PCM_DATE_KEY, REGIONAL_DATA_FILE


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
    return data
