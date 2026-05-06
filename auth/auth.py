import jwt
from dotenv import load_dotenv
import os
load_dotenv()
SECRET_KEY = os.getenv("SECRET_KEY")
class Auth:

    def __init__(self):
        pass

    def generate_jwt(self,payload):
        token = jwt.encode(payload,SECRET_KEY,algorithm="HS256")
        return token
    
    def verify_jwt(self,token):
        payload = jwt.decode(token,SECRET_KEY,algorithms=["HS256"])
