import time
from db.queries import DBManager
from url_scheduler.healthservice import check_status
dbmanger = DBManager()
def scheduler_data():
    print("Started the scheduler.....")

    while True:
        try:
            s = dbmanger.get_session()
            session = next(s)

            urlids = dbmanger.getallurlsids(session)

            for ids in urlids:
                try:
                    dbmanger.check_and_updatestatusdb(ids, session)
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