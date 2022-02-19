from pymongo import MongoClient
client = MongoClient('mongodb://localhost', 27017)

# route database
db = client["robot"]
menu_collection = db["myrobot"]
user = db["user"]

track_collection = db["track"]

class Database:
    
    def update_route(self, f_location, t_location):
        menu_collection.update_one({},{"$set":{"f_location":f_location, "t_location":t_location}})
    
    def update_location(self, current):
        menu_collection.update_one({},{"$set":{"current":current}})
        
    def update_collected_status(self, status):
        menu_collection.update_one({},{"$set":{"collected_package":status}})
    
    def update_moving_status(self, status):
        menu_collection.update_one({},{"$set":{"moving":status}})
        
    def get_route(self):
        res = menu_collection.find_one({}, {"_id":0, "current":0})
        return res
    
    def get_status(self):
        res = menu_collection.find_one({}, {"_id":0,"moving": 1, "collected_package": 1})
        return res
        
    def get_current(self)->int:
        res = menu_collection.find_one({}, {"_id":0, "current":1})
        return res["current"]
    
    def get_track_size(self):
        # res = track_collection.find({})
        return 4
        # return len(list(res))
        
    def get_station_detail(self, station_id):
        res = track_collection.find_one({"station_id":station_id}, {"_id":0})
        return res
    
class UserDB:
    
    def get_user_detail(self, username):
        res = user.find_one({"username":username}, {"_id":0 ,"hashed_password":0})
        return res
    
    def get_hashed_password(self, username):
        res = user.find_one({"username":username}, {"_id":0 ,"hashed_password":1})
        return res["hashed_password"]