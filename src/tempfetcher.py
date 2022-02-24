import requests
import json
from os import path
import os
from apscheduler.schedulers.blocking import BlockingScheduler
from datetime import datetime, timedelta
import pymongo
import pytz

sched = BlockingScheduler()


@sched.scheduled_job('interval', minutes=15)
def tempmonitor():
    #get environment variables
    username = os.environ['MONGO_INITDB_ROOT_USERNAME']
    password = os.environ['MONGO_INITDB_ROOT_PASSWORD']
    URL = os.environ['SENSOR_API_URL']

    page = requests.get(URL)

    #print(page.text)

    #parse JSON
    jsondata = json.loads(page.text)
   
    #parse ISO 8601 format data to datetime
    formatted_time = datetime.fromisoformat(str(jsondata['timestamp']))
    
    #formatted_time = pytz.timezone('Europe/Helsinki').localize(formatted_time)
  
    #formatted_time += timedelta(hours=3)
    # values = [str(formatted_time),str(jsondata['temperature']),str(jsondata['humidity'])]
    # values = ",".join(values)
    
    myclient = pymongo.MongoClient(f"mongodb://{username}:{password}@mongodb:27017/")
    db = myclient['database']
    coll = db['tempcollection']

    #insert the fetched record to database
    tempRecord = {
        "timestamp" : formatted_time,
        "temperature": jsondata['temperature'], 
        "humidity": jsondata['humidity']
        }

    coll.insert_one(tempRecord)

sched.start()
