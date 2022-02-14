from turtle import update
from manage_database import Database

db = Database()

class ControlRobot():
    
    def return_to_start(self):
        route = db.get_route()
        f_location = route["f_location"]
        t_location = route["t_location"]
        db.update_route(t_location, f_location)
    
    def is_end(self, current, end):
        return current == end
    
    def move_one_station(self, current):
        print(current)
        current = (current%db.get_track_size()) + 1
        print(current)
        db.update_location(current)
    
    def update_location(self):
        current = db.get_current()
        print(current)
        t_location = db.get_route()["t_location"]
        if self.is_end(current, t_location):
            return {
                "status": "stop"
            }
        else:
            self.move_one_station(current)
            return {
                "status": "continue"
            }
            
            
c = ControlRobot()
print(c.update_location())