from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from controller import ControlRobot
from control_page import ControlPage
from auth import LoginModel, UserOut, login, get_current_user
from fastapi import Depends
from send import update_val, ss, send,register,User

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

@app.post("/register")
def my_register(mu : User):
    return register(mu)

@app.post("/update/location")
def up_date(ms:ss, current_user: UserOut = Depends(get_current_user)):
    return update_val(ms)

@app.post("/send")
def up_date():
    send()
    return {
        "State": "continue moving"
    }

@app.get("/get-status")
def check_status():
    return c.get_status()

@app.post("/back-to-start")
def go_back(current_user: UserOut = Depends(get_current_user)):
    c.return_to_start()
    return c.return_to_start()

@app.post("/reached")
def reach():
    c.reached()

@app.post("/reset")
def reset(current_user: UserOut = Depends(get_current_user)):
    return c.reset_robot()

@app.get("/get-station/{id}")
def get_station_detail(id):
    return p.station_detail(int(id))

@app.get("/get-robot-status")
def get_robot_status_for_frontend():
    return p.get_robot_status()

@app.post("/token")
async def get_token(request: LoginModel):
    return login(request)

@app.get("/users/me/", response_model=UserOut)
def read_users_me(current_user: UserOut = Depends(get_current_user)):
    return current_user