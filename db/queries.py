from sqlmodel import SQLModel,create_engine,Session
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
    
