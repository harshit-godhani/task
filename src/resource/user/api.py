from fastapi import Depends,HTTPException,APIRouter,Security
from sqlalchemy.orm import Session
from src.resource.user.schema import UserCreateSchema,UserLoginSchema
from src.functionality.user import Create_User,Login_User,admin_access_all_task_view
from src.database.database import get_db
from fastapi.security import HTTPAuthorizationCredentials,HTTPBearer
from src.utils.utils import SECRET_KEY,ALGORITHM,ACCESS_TOKEN_EXPIRE_MINUTES,create_access_token
from datetime import timedelta
import jwt


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

    payload = jwt.decode(token,SECRET_KEY,algorithm=ALGORITHM)

    new_access_token = create_access_token(
        data={"sub":payload["sub"]},
        expires_delta= timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    )
    return{"access_token":new_access_token}

@user_router.get("admin/access/",tags=["Admin"])
def adm_acc_all_task_show(user_id:int,db:Session=Depends(get_db)):
    try:
        user = admin_access_all_task_view(user_id=user_id,db=db)
        return user
    except Exception as e:
        raise HTTPException(status_code=500,detail=str(e))


