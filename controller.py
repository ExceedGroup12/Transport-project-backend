from manage_database import Database

db = Database()

class ControlRobot():
    
    def reset_robot(self):
        res = self.calculate_station(db.get_current(), 1, 0)
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
        return self.calculate_station(db.get_current(), f_location, db.get_direction())
    
    def calculate_move(self):
        route = db.get_route()
        status = db.get_status()
        current = db.get_current()
        direction = db.get_direction()
        if not status["collected_package"]:
            f_location = route["f_location"]
            return self.calculate_station(current, f_location, direction)
        else:
            t_location = route["t_location"]
            return self.calculate_station(current, t_location, direction)
        
    def reached(self):
        db.update_moving_status(False)

    def get_status(self):
        moving = db.get_status()["moving"]
        if not moving:
            res = self.calculate_move()
            if res["move"] != 0:
                db.update_moving_status(True)
            return res

    
    def calculate_station(self, current, t_location, direction):
        track_size = db.get_track_size()
        if current == t_location:
            return {
                "move":0,
                "direction":direction
            }
        if current > t_location:
            diff = t_location - current + track_size
        else:
            diff = t_location - current
        if diff <= track_size//2:
            move = diff
            direction = 0
        else:
            move = track_size - diff
            direction = 1
        c_move = move
        if direction == 1:
            c_move *= -1
        location = db.get_current() + c_move
        if location < 0:
            location += track_size
        db.update_location(location)
        return {
            "move":move,
            "direction":direction
        }
