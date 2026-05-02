from sqlmodel import SQLModel,create_engine,Session,select
from db.models import Status,Url,User,HealthLog
from dotenv import load_dotenv
import os
load_dotenv()
class DBManager:
    def __init__(self):
        #get the connection here
        self.url_db = os.getenv("POSTGRES_URL")
        self.engine = None
        # print(self.url_db)
        try:
            self.engine = create_engine(self.url_db)
        except Exception as e:
            print("There is some Error with the Database Connection..",e)
    
    def create_db_tables(self):
        SQLModel.metadata.create_all(self.engine)

    def get_session(self):
        with Session(self.engine) as session:
            yield session
    
    def create_user(self,user:User,session:Session):
        #need to check if the user existed before if not then only add it
        try:
            statement = select(User).where(User.email == user.email)
            result = session.exec(statement).first()
            user_out = result.all() if result  else None
            if user_out:
                return {"message" : "User already Exist"}
            session.add(user)
            session.commit()
            session.refresh(user)
            return "success"
        except Exception as e:
            session.rollback()
            print("Some Exception Occured in DB creating the User...",e)
            return  "Internal Server Error"
        