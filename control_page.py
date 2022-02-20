from manage_database import Database
db = Database()

class ControlPage:
    
    def station_detail(self, station_id):
        return db.get_station_detail(station_id)
    
    def get_robot_status(self):
        current = db.get_current()
        status = db.get_status()
        
        route = db.get_route()
        f_location = route["f_location"]
        t_location = route["t_location"]
        
        collected_package = status["collected_package"]
        moving = status["moving"]
        
        if moving == False and collected_package == False and current == f_location:
            return {
                "message":"Waiting for pacakage"
            }
        if moving == True and current == f_location:
            return {
                "message": f"moving to pick up package location (station {f_location})"
            }
        if moving == True and current == t_location and collected_package == True:
            return {
                "message": f"moving to drop package location (station {t_location})" 
            }
        if moving == False and t_location == current:
            return {
                "message": f"Reach the destination location (station {t_location})"
            }
        else:
            return {
                "message": f"waiting for command"
            }