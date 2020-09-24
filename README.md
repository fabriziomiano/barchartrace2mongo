# BCR2Mongo

## What is this?
A simple script that reads the data from the [CPD dataset](https://github.com/pcm-dpc/COVID-19)
and, for a given variable name, creates video-tagged HTML str that is dumped to 
a given mongodb collection. 

## How to use  

### Setup a local version
* create and activate a virtual environment by following [this](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)
* install the requirements in requirements.txt

### How to run 
First, set the environment variables needed by the script to write the HTML string 
to the DB, that will be read by [COVIDashIT](https://github.com/fabriziomiano/covidashit): 
`MONGO_URI`, `DB_NAME`, `COLLECTION_NAME`, by running in a new shell 

```export <VAR_NAME>=<VAR_VALUE>```

e.g.

```export DB_NAME=myCoolDB```

for the variables mentioned above. Then, in the same shell run 

```python bcr2mongo.py --var <variable-name-as-per-DPC-dataset>```

e.g.

```python bcr2mongo.py --var totale_positivi```
