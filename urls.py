from fastapi import FastAPI
from controller import ControlRobot

app = FastAPI()
c = ControlRobot()


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