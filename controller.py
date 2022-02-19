from manage_database import Database

db = Database()

class ControlRobot():
    
    def reset_robot(self):
        res = self.calculate_station(db.get_current(), 1)
        db.update_location(1)
        db.update_route(1, 1)
        db.update_collected_status(False)
        db.update_moving_status(False)
        return res
    
    def return_to_start(self):
        route = db.get_route()
        f_location = route["f_location"]
        t_location = route["t_location"]
        db.update_route(t_location, f_location)
        return self.calculate_station(db.get_current(), f_location)
    
    def calculate_move(self):
        route = db.get_route()
        status = db.get_status()
        current = db.get_current()
        if not status["collected_package"]:
            f_location = route["f_location"]
            return self.calculate_station(current, f_location)
        else:
            t_location = route["t_location"]
            return self.calculate_station(current, t_location)
        
    def reached(self):
        db.update_moving_status(False)

    def get_status(self):
        moving = db.get_status()["moving"]
        if not moving:
            res = self.calculate_move()
            if res["move"] != 0:
                db.update_moving_status(True)
            return res

    
    def calculate_station(self, current, t_location):
        track_size = db.get_track_size()
        if current == t_location:
            return {
                "move":0,
            }
        move = t_location - current
        if move < 0:
            move += track_size
        db.update_location(t_location)
        return {
            "move":move,
        }
