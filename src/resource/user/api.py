from fastapi import Depends,HTTPException,APIRouter,Security
from sqlalchemy.orm import Session
from src.resource.user.schema import UserCreateSchema,UserLoginSchema
from src.functionality.user import Create_User,Login_User,admin_access_all_user_view,admin_access_to_user_delete
from src.database.database import get_db
from fastapi.security import HTTPAuthorizationCredentials,HTTPBearer
from src.utils.utils import create_access_token
from datetime import timedelta
from jose import jwt
from src.config import Config

ALO = Config.ALGO
SEC = Config.SEC_KEY
ACCESS = Config.ACCESS_TOKEN_EXPIRE
REFRESH = Config.REFRESH_TOKEN_EXPIRE

security = HTTPBearer()
user_router = APIRouter()

@user_router.post("/create/user/",tags=["User"])
def reg_user(user:UserCreateSchema,db:Session= Depends(get_db)):
    try:
        user = Create_User(user=user,db=db)
        return user
    except Exception as e:
        raise HTTPException(status_code=500,detail=str(e))
    
@user_router.post("/user/login/",tags=["User"])
def log_user(user:UserLoginSchema,db:Session= Depends(get_db)):
    try:
        user = Login_User(user=user,db=db)
        return user
    except Exception as e:
        raise HTTPException(status_code=500,detail=str(e))
        
@user_router.post("/refresh/",tags=["Token"])
def new_access_token(refresh_token:HTTPAuthorizationCredentials=Security(security)):
    token = refresh_token.credentials

    payload = jwt.decode(token,SEC,ALO)

    new_access_token = create_access_token(
        data={"sub":payload["sub"]},
        expires_delta= timedelta(minutes=ACCESS)
    )
    return{"access_token":new_access_token}

@user_router.get("/admin/access/",tags=["Admin"])
def adm_acc_all_user_show(user_id:int, db:Session=Depends(get_db)):
    try:
        user = admin_access_all_user_view(user_id=user_id,db=db)
        return user
    except Exception as e:
        raise HTTPException(status_code=500,detail=str(e))

@user_router.get("/admin/delete/",tags=["Admin"])
def adm_acc_user_del(user:int,db:Session=Depends(get_db)):
    try:
        user = admin_access_to_user_delete(user=user,db=db)
        return user
    except Exception as e:
        raise HTTPException(status_code=500,detail=str(e))


