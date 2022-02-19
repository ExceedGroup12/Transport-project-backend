from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from controller import ControlRobot
from control_page import ControlPage
from send import update_val

app = FastAPI()
c = ControlRobot()
p = ControlPage()

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
@app.post("update/location")
def up_date():
    return update_val()

@app.get("/get-status")
def check_status():
    return c.get_status()

@app.post("/back-to-start")
def go_back():
    c.return_to_start()
    return c.return_to_start()

@app.post("/reached")
def reach():
    c.reached()

@app.post("/reset")
def reset():
    return c.reset_robot()

@app.get("/get-station/{id}")
def get_station_detail(id):
    return p.station_detail(int(id))

@app.get("/get-robot-status")
def get_robot_status_for_frontend():
    return p.get_robot_status()
