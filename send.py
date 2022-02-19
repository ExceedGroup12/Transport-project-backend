from datetime import datetime
from fastapi import FastAPI
from pymongo import MongoClient
from pydantic import BaseModel

client = MongoClient('mongodb://localhost:27017/')

mydb = client["robot"]
collection = mydb["myrobot"]
app = FastAPI()

class ss(BaseModel):
    ff : int
    gg : int

@app.post("/update/location")
def update_val(ms : ss):
    my_query = {}
    new_query = {"$set": {"f_location":  ms.ff,"t_location": ms.gg,"moving":False , "collected_package":False }}
    collection.update_one(my_query,new_query)