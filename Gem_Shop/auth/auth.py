import datetime
from datetime import timezone,timedelta
from fastapi import HTTPException, Security
from fastapi.security import HTTPBearer,HTTPAuthorizationCredentials
import starlette
from starlette import status
 #Bearer token is used to authenticate the user


from passlib.context import CryptContext 
import jwt

from repos.user_repos import find_user # type: ignore


class AuthHandler:
    security=HTTPBearer()
    pwd_context=CryptContext(schemes=["bcrypt"])
    secret='supersecret'

    def get_password_hash(self,password):
        return self.pwd_context.hash(password)
    
    def verify_password(self,pwd,hashed_pwd):
        return self.pwd_context.verify(pwd,hashed_pwd)

    def encode_token(self, user_id):
        payload = {
            'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=8),
            'iat': datetime.datetime.utcnow(),
            'sub': user_id
        }
        return jwt.encode(payload, self.secret, algorithm='HS256')


    def decode_token(self,token):
        try:
            payload=jwt.decode(token,self.secret,algorithms=['HS256'])
            return payload['sub']
        except jwt.ExpiredSignatureError:
            raise HTTPException(status_code=401,detail='Signature has expired')
        except jwt.InvalidTokenError:
            raise HTTPException(status_code=401,detail='Invalid token')
    
    def auth_wrapper(self,auth:HTTPAuthorizationCredentials=Security(security)):
        return self.decode_token(auth.credentials)
        #Wrapper is used to wrap the function and add some functionality to it, here we are adding authentication to the function


    def get_current_user(self,auth:HTTPAuthorizationCredentials=Security(security)):
        credentials_exception=HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Could not validate credentials'
        )
        username = self.decode_token(auth.credentials)
        if username is None:
            raise credentials_exception
        
        user = find_user(username)
        if user is None:
            raise credentials_exception
        return user