from fastapi import Depends,HTTPException
from src.database.database import get_db
from sqlalchemy.orm import Session
from src.resource.user.model import UserModel
from src.resource.user.schema import UserCreateSchema,UserLoginSchema
from src.utils.utils import verify_password,create_access_token,create_refresh_token,pwd_context



def Create_User(user:UserCreateSchema,db:Session= Depends(get_db)):
    userdata = db.query(UserModel).filter(UserModel.username == user.username).first()
    if userdata:
        raise HTTPException(status_code=400,detail="User all ready exist!")
        
    usermail = db.query(UserModel).filter(UserModel.email == user.email).first()
    if usermail:
        raise HTTPException(status_code=400,detail="User email already exits!")
        
    hash_password = pwd_context.hash(user.password)
    user_db = UserModel(username=user.username,password=hash_password,email=user.email,role=user.role)

    db.add(user_db)
    db.commit()
    db.refresh(user_db)

    return{
        "Status": True,
        "massage": "User create successfully.",
        "username": user_db.username,
        "user_id": user_db.id
    }

def Login_User(user:UserLoginSchema,db: Session = Depends(get_db)):
    db_user = db.query(UserModel).filter(UserModel.email == user.email).first()

    if not db_user or not verify_password(user.password,db_user.password):
        raise HTTPException(status_code=400,detail="Incorect details...!")
    
    access_token = create_access_token(data={"sub": user.email,"id":db_user.id})
    refresh_token = create_refresh_token(data={"sub": user.email,"id":db_user.id})

    return{
        "massage":"Login Successfully!",
        "access_token": access_token,
        "refresh_token" : refresh_token,
        "token_type": "Bearer"
    }

def admin_access_all_user_view(user_id:int,db:Session=Depends(get_db)):
    try:
        admin = db.query(UserModel).filter(UserModel.id == user_id).first()

        if admin.role != "admin":
            raise HTTPException(status_code=400,detail="Admin not access to user data.")
    
        user_all = db.query(UserModel).all()

        return{"success":True,
           "user_all":user_all
           }
    except Exception as e:
        raise HTTPException(status_code=500,detail=str(e))

def admin_access_to_user_delete(user:int,db:Session=Depends(get_db)):
    try:
        user1 = db.query(UserModel).filter(UserModel.id == user).first()

        if user1.role != 'admin':
            raise HTTPException(status_code=403,detail="admin not found!")
        
        if user1.role != 'user':
            db.query(UserModel).delete()
            return{
                "massaeg":"all user are delete"
            }
        
        db.commit()
    except Exception as e:  
        raise HTTPException(status_code=400,detail=str(e))