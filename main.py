from datetime import datetime, timedelta
from typing import Optional
from pymongo import MongoClient
from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from passlib.context import CryptContext
from pydantic import BaseModel

# to get a string like this run:
# openssl rand -hex 32
SECRET_KEY = "c95c58c792bcbd48518d8654fc3d44d2cc3db64eecbeb6ba3cc947edb3261102"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

client = MongoClient('mongodb://localhost:27017/')

mydb = client["robot"]
collection = mydb["user"]
robots= mydb["myrobot"]

class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: Optional[str] = None


class User(BaseModel):
    username: str
    email: Optional[str] = None
    full_name: Optional[str] = None
    disabled: Optional[bool] = None
    password: Optional[str] = None

class UserInDB(User):
    hashed_password: str


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


app = FastAPI()

def get_user_from_db() :
    result = collection.find({},{"_id":0})
    #print(result)
    dic = {}
    for r in result:
        dic[ r['username'] ] = r
    return dic

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    return pwd_context.hash(password)


def get_user(db, username: str):
    if username in db:
        user_dict = db[username]
        return UserInDB(**user_dict)

def authenticate_user(fake_db, username: str, password: str):
    user = get_user(fake_db, username)
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        print(username)
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except JWTError:
        raise credentials_exception
    fake_db = get_user_from_db()
    user = get_user(fake_db, username=token_data.username)
    if user is None:
        raise credentials_exception
    return user


async def get_current_active_user(current_user: User = Depends(get_current_user)):
    if current_user.disabled:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user

class state(BaseModel):
    ff: str
    gg: str

@app.post("/level")
async def level(form_data: OAuth2PasswordRequestForm = Depends(get_current_user() ) ):
    mydict = {"from": form_data.ff, "hashed_password": form_data.gg}
    collection2 = mydb["command"]
    collection2.insert_one(mydict)

@app.post("/register")
async def login_for_access_token(form_data: User):
    #print(form_data.username)
    #print(form_data.password)
    mydict = { "username" :  form_data.username ,"hashed_password" : get_password_hash(form_data.password) }
    res = collection.find_one({"username":form_data.username})
    if(res != None):
        return {
            "username":"already use"
        }
    collection.insert_one(mydict)

@app.post("/token", response_model=Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    fake_db = get_user_from_db()
    user = authenticate_user(fake_db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

class fg(BaseModel):
    ff: int
    gg: int
'''
@app.post("/station/")
def read_users_me(current_user: User = Depends(get_current_user) , a : fg  ):
    result = robots.find_one({"_id": "620f618c8ae69a135949b291"})
    ans = result['t_location']
    return { ans }'''

@app.get("/users/me/", response_model=User)
def read_users_me(current_user: User = Depends(get_current_active_user)):
    return current_user

@app.get("/users/me/items/")
def read_own_items(current_user: User = Depends(get_current_user)):
    return [{"item_id": "Foo", "owner": current_user.username}]
