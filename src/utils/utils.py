from fastapi import HTTPException
from passlib.context import CryptContext 
from jose import jwt
from datetime import datetime,timedelta
from src.config import Config

ALO = Config.ALGO
SEC = Config.SEC_KEY
ACCESS = Config.ACCESS_TOKEN_EXPIRE
REFRESH = Config.REFRESH_TOKEN_EXPIRE

pwd_context = CryptContext(schemes=["bcrypt"],deprecated="auto")

def hash_password(password:str):
    return pwd_context.hash(password)

def verify_password(pain_password,hashed_password):
    return pwd_context.verify(pain_password,hashed_password)

def verify_token(token:str):
    try:
        payload = jwt.decode(token,SEC,algorithms=ALO)
        return payload
    except Exception as e:
        raise HTTPException(status_code=400,detail=str(e))

def create_access_token(data:dict,expires_delta:timedelta = None):
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=ACCESS))
    to_encode.update({"exp":expire})
    return jwt.encode(to_encode,SEC,ALO)

def create_refresh_token(data:dict,expires_delta:timedelta = None):
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=REFRESH))
    to_encode.update({"exp":expire})
    return jwt.encode(to_encode,SEC,ALO)
