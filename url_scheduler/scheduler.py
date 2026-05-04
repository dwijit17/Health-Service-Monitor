import time
from db.queries import DBManager
from url_scheduler.healthservice import check_status
dbmanger = DBManager()
def scheduler_data():
    print("Started the scheduler.....")
    s = dbmanger.get_session()
    session = next(s)
    while True:
        #get all the urls
        urlids = dbmanger.getallurlsids()
        for ids in urlids:
            #check its status
            dbmanger.check_and_updatestatusdb(ids,session)
            #this updates data sequentially
        time.sleep(60)