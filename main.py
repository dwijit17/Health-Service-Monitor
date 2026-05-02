from fastapi import FastAPI
from db.queries import DBManager
from db.models import Status,Url,User,HealthLog
from contextlib import asynccontextmanager
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
async def root():
    return {"Message":"Hello World"}