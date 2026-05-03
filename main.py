from fastapi import FastAPI,status,HTTPException,Depends
from db.queries import DBManager
from contextlib import asynccontextmanager
from sqlmodel import Session
from DTO.usermodel import User_DTO
from DTO.urlmodel import Url_DTO
#FastApi is entry point class

dbmanager = DBManager()
#on startup create the tables if not exist
@asynccontextmanager
async def lifespan(app: FastAPI):
    dbmanager.create_db_tables()
    yield
    print("App shutting down")

app = FastAPI(lifespan=lifespan) 
#Here we are making an app obj for the FastApi clls
@app.get("/") #This is a decorator 
#it modifies the function given below
#app object now has different methods defined
#in that it has the get method
#the get method takes the below root function and modifies it like this
#root = get(root)
#then it will call the root
#that is what the decorator is
def root():
    return {"Message":"Hello World"}


#signup api endpoint
@app.post("/signup")
def signup(user: User_DTO,session:Session = Depends(dbmanager.get_session)):
    #create the user here
    try:
        message = dbmanager.create_user(user,session)
    except Exception as e:
        print("Some Exception Occured in creating the User...",e)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,detail="There is an issue in signup...")
    return {"message": message}

#signin api endpoint
@app.post("/signin")
def signin(user : User_DTO,session : Session = Depends(dbmanager.get_session)):
    try:
        message = dbmanager.get_user(user,session)
    except Exception as e:
        print("Some Exception Occured in Fetching the User Details...",e)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,detail="There is an issue in signin...")
    return {"message" : message}

#post urls 
@app.post("/urls")
def add_url(url:Url_DTO,session : Session = Depends(dbmanager.get_session)):
    try:
        message = dbmanager.create_url(url,session)
    except Exception as e:
        print("Some Exception occured in adding the url...",e)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,detail="There is an issue in adding the url ...")
    return {"message": message}

#get urls
@app.get("/urls")
def get_url(user_id:int,session : Session = Depends(dbmanager.get_session)):
    try:
        message = dbmanager.get_url(user_id,session)
    except Exception as e:
        print("Some Exception occured in fetching the url...",e)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,detail="There is an issue in fetching the urls ...")
    return message

#check the status of url and put it in the database
@app.post("/check/{url_id}")
def check_status_url(url_id:int ,session:Session = Depends(dbmanager.get_session)):
    try:
        message = dbmanager.check_and_updatestatusdb(url_id,session)
    except Exception as e:
        print("Some Exception occured in checking the url...",e)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,detail="There is an issue in updating the status of url ...")
    return message