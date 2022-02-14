from pymongo import MongoClient
client = MongoClient('mongodb://localhost', 37017)

# route database
db = client["transport"]
menu_collection = db["route"]

track_collection = db["track"]

class Database:
    
    def update_route(self, f_location, t_location):
        menu_collection.update_one({},{"$set":{"f_location":f_location, "t_location":t_location}})
    
    def update_location(self, current):
        menu_collection.update_one({},{"$set":{"current":current}})
        
    def get_route(self):
        res = menu_collection.find_one({}, {"_id":0, "current":0})
        return res
        
    def get_current(self)->int:
        res = menu_collection.find_one({}, {"_id":0, "f_location":0, "t_location":0})
        return res["current"]
    
    def get_track_size(self):
        res = track_collection.find({})
        return len(list(res))