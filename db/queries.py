from sqlmodel import SQLModel,create_engine,Session,select,func
from db.models import Url,User,UserUrl,HealthLog,Status
from DTO.usermodel import *
from DTO.urlmodel import *
from dotenv import load_dotenv
import os
from url_scheduler.healthservice import check_status
from datetime import datetime,timezone
from auth.auth import Auth
load_dotenv()
authobj = Auth()
class DBManager:
    def __init__(self):
        #get the connection here
        self.url_db = None
        if os.getenv("PROD","False") == "True":
            self.url_db = (
            f"postgresql://{os.getenv("POSTGRES_USER")}:"
            f"{os.getenv('POSTGRES_PASSWORD')}"
            f"@localhost:8100/{os.getenv("POSTGRES_DB")}"
        )
        else:
            self.url_db = os.getenv("POSTGRES_URL")
        print("**************",self.url_db)
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
            #stored hashed password
            hashed_pwd = authobj.hash_password(user.password)
            new_user = User(email=user.email,password_hash=hashed_pwd)
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
            statement = select(User).where(User.email == user.email)
            result = session.exec(statement).first()
            if not result:
                return {"message": False, "user_id":None}
            #here success mean we need to send the token
            #get the userid for this user
            verification = authobj.verify_password(user.password,result.password_hash)
            if verification:
                return {"message" : True , "user_id" : result.id}
            return {"message": False, "user_id":None}
        except Exception as e:
            session.rollback()
            print("There is some exception occured in fetching the user",e)
            raise
    
    def create_url(self,url:Url_DTO,session:Session,user_id:int):
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
            check_stmt = select(UserUrl).where(UserUrl.url_id == url_id,UserUrl.user_id==user_id)
            check_result = session.exec(check_stmt).first()
            if check_result:
                return "url already added"
            new_user_url = UserUrl(user_id = user_id ,url_id = url_id,url_name=url.url_name)
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
                return {"message":False,"detail":"Invalid url id"}
            link = result.url_link
            #call the check status function
            t0 = datetime.now(timezone.utc)
            response = check_status(link)
            #the above line here is a blocking call
            #update the result in the postgres db
            rms = response[1]*1000 if response[1] else None
            health_data = HealthLog(url_id=url_id,status=response[0],response_time_ms=rms,checked_at=t0)
            session.add(health_data)
            session.commit()
            session.refresh(health_data)
            return {"message":True,"url_id": url_id,"url_link":link,"response_time_ms":health_data.response_time_ms,"status":health_data.status,"checked_at":health_data.checked_at}
        except Exception as e:
            session.rollback()
            print("There is some error in either fetching or updating the health data..",e)
            raise
    
    def geturlstats(self,url_id:int,session:Session):
        try:
            statement0 = select(HealthLog).where(HealthLog.url_id == url_id).order_by(HealthLog.checked_at.desc())
            result = session.exec(statement0)
            final_res =  result.all()
            total_rows = len(final_res)
            if total_rows==0: #I think both are same
                return {"message":"No Data Exist Yet for the url_id"}
            statement1 = select(func.count()).select_from(HealthLog).where(HealthLog.url_id == url_id,HealthLog.status == Status.up)
            up_count = session.exec(statement1).one()
            down_count = total_rows - up_count
            recent = []
            for data in final_res:
                recent.append({"status":data.status,"response_time_ms":data.response_time_ms,"checked_at":data.checked_at})

            response = {"url_id": url_id,"total_checks":total_rows,"up_count":up_count,"down_count":down_count,"recent":recent[:10]}
            return response
        except Exception as e:
            session.rollback()
            print("There is some error in either gettting the health data..",e)
            raise

    def getallurlsids(self,session:Session):
        try:
            # s = self.get_session() 
            # session = next(s)
            statement = select(Url.id).select_from(Url)
            result = session.exec(statement).all()
            return list(result)
        except Exception as e:
            print("There is some error in getting all the list of urls..",e)
            raise
    
    def check_ownership(self,session:Session,user_id:int | None, url_id : int):
        try:
            #check if the user_id really be access to this url_id
            statement1 = select(UserUrl).where(UserUrl.user_id == user_id , UserUrl.url_id == url_id)
            result1 = session.exec(statement1).first()
            if not result1:
                return {"message":False,"detail":"unauthorized"}
            return {"message":True,"detail":"authorized"}
        except Exception as e:
            print("There is some error in checking the ownership.",e)
            raise

