import requests
from db.models import Status
# URL = "https://example.com"
def check_status(url:str):
    try:
        response = requests.get(url=url,timeout=10)
        if response.status_code >= 500:
            return (Status.down,None)
        else:
            return (Status.up,response.elapsed.total_seconds())
    except Exception as e:
        print("Some Exception occured in reaching the service..",e)
        return (Status.down,None)