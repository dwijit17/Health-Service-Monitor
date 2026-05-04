from sqlmodel import SQLModel,create_engine,Session,select
from db.models import Url,User,UserUrl,HealthLog
from DTO.usermodel import *
from DTO.urlmodel import *
from dotenv import load_dotenv
import os
from url_scheduler.healthservice import check_status
from datetime import datetime,timezone
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
    
    def create_user(self,user:User_DTO,session:Session):
        #need to check if the user existed before if not then only add it
        try:
            statement = select(User).where(User.email == user.email)
            result = session.exec(statement).first()
            if result:
                return "User already Exist"
            new_user = User(email=user.email,password_hash=user.password)
            session.add(new_user)
            session.commit()
            session.refresh(new_user)
            return "success"
        except Exception as e:
            session.rollback()
            print("Some Exception Occured in DB creating the User...",e)
            raise 

    def get_user(self,user:User_DTO,session:Session):
        try:
            statement = select(User).where(User.email == user.email , User.password_hash == user.password)
            result = session.exec(statement).first()
            if not result:
                return "Invalid Username or Password"
            return "success"
        except Exception as e:
            session.rollback()
            print("There is some exception occured in fetching the user",e)
            raise
    
    def create_url(self,url:Url_DTO,session:Session):
        #This will add the url in the Url table if url doesnt exist before
        #considering the url endpoints are differnet even with same domain name with differnt endpoints
        try:
            #The stament to check URL exist in db
            url_id = None
            created = False
            statement = select(Url).where(Url.url_link == str(url.url_link))
            result = session.exec(statement).first()
            if not result:
            #Add the url
            #if url doesnt exist here it will at to db
                new_url = Url(url_link=str(url.url_link))
                session.add(new_url)
                session.commit()
                session.refresh(new_url)
                url_id = new_url.id
                created = True
            #if url already exist it will come here or when its created new it will come here
            # result = session.exec(statement).first() 
            #if url already exist get that url_id and link it with this particular user
            #check before if that particular user has already added that url
            if not created:
                url_id = result.id
            check_stmt = select(UserUrl).where(UserUrl.url_id == url_id,UserUrl.user_id==url.user_id)
            check_result = session.exec(check_stmt).first()
            if check_result:
                return "url already added"
            new_user_url = UserUrl(user_id = url.user_id ,url_id = url_id,url_name=url.url_name)
            session.add(new_user_url)
            session.commit()
            session.refresh(new_user_url)
            return "success"
        except Exception as e:
            session.rollback()
            print("There is some error occured adding url into the database..",e)
            raise

    def get_url(self,user_id:int,session:Session):
        #fix if the userid doesnt exist it is coming no urls added yet -- fix this thing
        try:
            statement = select(UserUrl,Url).where(UserUrl.user_id==user_id).join(Url,UserUrl.url_id==Url.id)
            result = session.exec(statement)
            rows = result.all()
            if not rows:
                return "No urls added yet"
            data = []
            for (urlname,urllink) in rows:
                data.append({"url_id":urllink.id , "url_link" : urllink.url_link , "url_name" : urlname.url_name})
            return data
        except Exception as e:
            session.rollback()
            print("There is some error in fetching the urls ..",e)
            raise

    def check_and_updatestatusdb(self,url_id:int,session:Session):
        #this function gets the url_id 
        #it will get the acutal url from the url table
        #and will call the checkstatus function 
        #get the result and update that data in db and also send it as a response
        try:
            statement = select(Url).where(Url.id == url_id)
            result = session.exec(statement).first()
            if not result:
                return "Invalid url_id"

            link = result.url_link
            #call the check status function
            t0 = datetime.now(timezone.utc)
            print(t0)
            response = check_status(link)
            #the above line here is a blocking call
            #update the result in the postgres db
            health_data = HealthLog(url_id=url_id,status=response[0],response_time_ms=response[1]*1000,checked_at=t0)
            session.add(health_data)
            session.commit()
            session.refresh(health_data)
            return {"url_id": url_id,"url_link":link,"response_time_ms":health_data.response_time_ms,"status":health_data.status,"checked_at":health_data.checked_at}
        except Exception as e:
            session.rollback()
            print("There is some error in either fetching or updating the health data..",e)
            raise

