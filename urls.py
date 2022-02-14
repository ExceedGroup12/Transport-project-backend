from fastapi import FastAPI
from controller import ControlRobot

app = FastAPI()
c = ControlRobot()


@app.get("/check-station")
def check_status():
    return c.update_location()

@app.post("/back-to-start")
def go_back():
    c.return_to_start()
    return c.update_location()