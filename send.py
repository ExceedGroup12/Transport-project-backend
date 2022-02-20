from typing import Optional
from fastapi import FastAPI
from pymongo import MongoClient
from pydantic import BaseModel
from passlib.context import CryptContext

client = MongoClient('mongodb://localhost:27017/')

mydb = client["robot"]
collection = mydb["myrobot"]
userdb = mydb["user"]
app = FastAPI()

class ss(BaseModel):
    ff : int
    gg : int

@app.post("/update/location")
def update_val(ms : ss):
    my_query = {}
    new_query = {"$set": {"f_location":  ms.ff,"t_location": ms.gg,"moving":False , "collected_package":False }}
    collection.update_one(my_query,new_query)

@app.post("/send")
def send():
    my_query = {}
    new_query = {"$set": {"collected_package": True}}
    collection.update_one(my_query, new_query)

class User(BaseModel):
    username: str
    full_name: Optional[str] = None
    email: Optional[str] = None
    hashed_password: str
    disabled: Optional[bool] = None

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
def get_password_hash(password):
    return pwd_context.hash(password)

@app.post("/register")
def register(mu : User):
    mu.hashed_password = get_password_hash(mu.hashed_password)
    #print(mu.hashed_password)
    #print(get_password_hash(mu.hashed_password))
    mydict = {"username": mu.username , "full_name":mu.full_name , "email": mu.email, "hashed_password": mu.hashed_password}
    userdb.insert_one(mydict)

