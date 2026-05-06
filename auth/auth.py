import jwt
from dotenv import load_dotenv
import os
load_dotenv()
SECRET_KEY = os.getenv("SECRET_KEY")
class Auth:

    def __init__(self):
        pass

    def generate_jwt(self,payload):
        try:
            token = jwt.encode(payload,SECRET_KEY,algorithm="HS256")
            return token
        except Exception as e:
            print("There was some error in generating the jwt token")
            raise

    def verify_jwt(self,token):
        try:
            payload = jwt.decode(token,SECRET_KEY,algorithms=["HS256"])
            return payload
        except jwt.ExpiredSignatureError:
            print("Token Expired..")
            raise
        except jwt.InvalidTokenError:
            print("Access Denied token tampered or Invalid...")
            raise
        except Exception as e:
            print("Some error in verifying the token")
            raise
    
    def get_userid(self,authorization:str):
        token = authorization.split(" ")[1]
        payload = self.verify_jwt(token)
        user_id = payload["user_id"]
        return user_id