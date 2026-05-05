import time
from db.queries import DBManager
from url_scheduler.healthservice import check_status
from concurrent.futures import ThreadPoolExecutor
import time
dbmanger = DBManager()

def process_url(url_id:int):
    s = dbmanger.get_session()
    session = next(s)

    try:
        dbmanger.check_and_updatestatusdb(url_id,session)
    finally:
        session.close()


def scheduler_data():
    print("Started the scheduler.....")

    while True:
        try:
            s = dbmanger.get_session()
            session = next(s)

            urlids = dbmanger.getallurlsids(session)

            #for ids in urlids:
            try:
                    #the below is the function that take every ids and run and update their status in db
                    #for speedint up this we use ThreadPoolExecutor 
                    #for network calls multiple threads GIL is realsed if waiting time is there so little parllel/concurent execution
                start = time.time()
                with ThreadPoolExecutor(max_workers=5) as executor:
                    executor.map(process_url,urlids)
                    # dbmanger.check_and_updatestatusdb(ids, session)
                end = time.time()
                print(f"Processsed {len(urlids)} in {end-start:.2f} sec...")
            except Exception as e:
                print("Error checking URL:", e)

        except Exception as e:
            print("Scheduler loop error:", e)

        finally:
            try:
                session.close()
            except:
                pass

        time.sleep(60)