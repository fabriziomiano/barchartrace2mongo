import os

NATIONAL_DATA_FILE = "dpc-covid19-ita-andamento-nazionale.json"
REGIONAL_DATA_FILE = "dpc-covid19-ita-regioni.json"
PROVINCIAL_DATE_FILE = "dpc-covid19-ita-province.json"
BASE_URL_DATA = (
    "https://raw.githubusercontent.com"
    "/pcm-dpc/COVID-19/master/dati-json/"
)
URL_NATIONAL_DATA = os.path.join(BASE_URL_DATA, NATIONAL_DATA_FILE)
URL_REGIONAL_DATA = os.path.join(BASE_URL_DATA, REGIONAL_DATA_FILE)
URL_PROVINCIAL_DATA = os.path.join(BASE_URL_DATA, PROVINCIAL_DATE_FILE)
PCM_DATE_KEY = "data"
BARCHART_RACE_QUERY = {"name": ""}
MONGO_URI = os.environ["MONGO_URI"]
DB_NAME = os.environ["DB_NAME"]
COLLECTION_NAME = os.environ["COLLECTION_NAME"]
VARS_MAP = {
    'ricoverati_con_sintomi': {
        'title': 'Hospitalized With Symptoms'
    },
    'terapia_intensiva': {
        'title': 'Intensive Care Unit'
    },
    'totale_ospedalizzati': {
        'title': 'Total Hospitalized'
    },
    'isolamento_domiciliare': {
        'title': 'Self Isolation'
    },
    'totale_positivi': {
        'title': 'Total Positive'
    },
    'variazione_totale_positivi': {
        'title': 'Total Positive Variation'
    },
    'nuovi_positivi': {
        'title': 'New Positive'
    },
    'dimessi_guariti': {
        'title': 'Total Healed'
    },
    'deceduti': {
        'title': 'Total Deaths'
    },
    'totale_casi': {
        'title': 'Total Cases'
    },
    'tamponi': {
        'title': 'Total Swabs'
    },
    'tamponi_giornalieri': {
        'title': 'Daily Swabs'
    },
    'deceduti_giornalieri': {
        'title': 'Daily Deaths'
    },
    'casi_da_sospetto_diagnostico': {
        'title': 'Positive Suspected Case'
    },
    'casi_da_screening': {
        'title': 'Positive From Screening'
    },
    'casi_testati': {
        'title': 'Total Tested'
    }
}
PERIOD_LABEL = {
    'x': .99,
    'y': .25,
    'ha': 'right',
    'va': 'center'
}
PCM_DATE_FMT = "%Y-%m-%dT%H:%M:%S"
CHART_DATE_FMT = "%d %b"
