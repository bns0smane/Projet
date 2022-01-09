import sys
import pandas as pd
import pymongo
import json
import os



def DataBase():
    filepath = 'C:\\Users\\hixam\\Desktop\\scraped\\combined_csv.csv' 
    import_content(filepath)
def import_content(filepath):
    mng_client = pymongo.MongoClient('localhost:27017')
    mng_db = mng_client['BI_PROJECTS_DB']
    collection_name = 'ESPACENET' 
    db_cm = mng_db[collection_name]
    cdir = os.path.dirname(__file__)
    file_res = os.path.join(cdir, filepath)

    data = pd.read_csv(file_res)
    data_json = json.loads(data.to_json(orient='records'))
    db_cm.insert(data_json)
    print('Data saved well in the DataBase')
