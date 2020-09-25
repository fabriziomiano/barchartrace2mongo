# BCR2Mongo

## What is this?
A simple script that reads the data from the [CPD dataset](https://github.com/pcm-dpc/COVID-19)
and, for a given variable name, creates video-tagged HTML str that is dumped to 
a given mongodb collection. 

## How to use  

The script needs a running instance of mongoDB and the relative environment
variables need to be set.

### Setup 
* create and activate a virtual environment by following [this](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)
* install the requirements in `requirements.txt`
* create a `.env` file in the root directory of the repo and add the following
variables (needed):
    - `MONGO_URI=<uri>`
    - `DB_NAME=<db_name>`
    - `COLLECTION_NAME=<coll_name>`
    
Additionally, `ENV` and `COLLECTION_NAME-DEV` to keep development environments
isolated. 

**N.B.:** The environment variables are needed by the script to write the HTML string 
to the DB, that will be read by [COVIDashIT](https://github.com/fabriziomiano/covidashit): 

### Run

Once the `.env` has been prepared, in a shell with an active virtual environment  

```(venv)$ python bcr2mongo.py --var <variable-name-as-per-DPC-dataset>```


#### Expected Output

If all goes down well, the output of, e.g.

```(venv)$ python bcr2mongo.py --var totale_positivi```
 
will be 

```
2020-09-25 09:19:34,694 - main - [INFO] - ====================
2020-09-25 09:19:34,694 - main - [INFO] - ENVIRONMENT: dev
2020-09-25 09:19:34,694 - main - [INFO] - Doing totale_positivi
2020-09-25 09:19:34,694 - Utils - [INFO] - Getting Data
2020-09-25 09:19:35,148 - Utils - [INFO] - Done getting data
2020-09-25 09:19:35,167 - Utils - [INFO] - Making BCR
2020-09-25 09:21:55,855 - Utils - [INFO] - Done making BCR
2020-09-25 09:21:55,979 - main - [INFO] - Writing to DB to collection barcharts-dev
2020-09-25 09:22:00,013 - main - [INFO] - Done
2020-09-25 09:22:00,014 - main - [INFO] - ====================
```

and a new entry on the db will be created

![alt_text](https://raw.githubusercontent.com/fabriziomiano/barchartrace2mongo/master/imgs/example-doc.png)
