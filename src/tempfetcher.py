import requests
import json
from apscheduler.schedulers.blocking import BlockingScheduler
from os import environ
import datetime
import pymongo


sched = BlockingScheduler()


@sched.scheduled_job('interval', minutes=20)
def tempmonitor():
    #get environment variables
    username = environ['MONGO_INITDB_ROOT_USERNAME']
    password = environ['MONGO_INITDB_ROOT_PASSWORD']
    URL = environ['SENSOR_API_URL']

    page = requests.get(URL)

    #print(page.text)

    #parse JSON
    jsondata = json.loads(page.text)
    
    #convert timestamp to dateobject
    try:
      formatted_time = datetime.datetime.strptime(jsondata['timestamp'], '%m/%d/%Y %H:%M:%S')
    except:
      print("API returned wrong format, fallign back to isoformat")
      try:
          formatted_time = datetime.datetime.fromisoformat(jsondata['timestamp'])
          
      except Exception as e:
          print(e)
          print("isoformat failed, giving up!")
    
    
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