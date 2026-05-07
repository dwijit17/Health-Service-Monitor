import jwt
from dotenv import load_dotenv
import os
from passlib.context import CryptContext
load_dotenv()
SECRET_KEY = os.getenv("SECRET_KEY")
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
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
        try:
            token = authorization.split(" ")[1]
            payload = self.verify_jwt(token)
            user_id = payload["user_id"]
            return user_id
        except Exception as e:
            raise
    
    def hash_password(self,password: str):
        return pwd_context.hash(password)
    
    def verify_password(self, plain_password: str, hashed_password: str):
        return pwd_context.verify(plain_password, hashed_password)
    