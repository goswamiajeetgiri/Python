from fastapi import HTTPException, Request,status
from sqlalchemy.orm import Session
from src.user.dtos import UserSchema,LoginSchema
from src.user.models import UserModel
from pwdlib import PasswordHash
import jwt
from src.utils.settings import settings
from datetime import datetime,timedelta,timezone
from jwt.exceptions import InvalidTokenError,ExpiredSignatureError

password_hash = PasswordHash.recommended()


def get_password_hash(password):
    return password_hash.hash(password)
def verify_password(plain_password, hashed_password):
    return password_hash.verify(plain_password, hashed_password)

def register(body: UserSchema, db: Session):
    # check existing user
    is_user = db.query(UserModel).filter(UserModel.email == body.email).first()
    if is_user:
        raise HTTPException(status_code=400, detail="User already exists.")

    # hash password
    hash_password = get_password_hash(body.password)

    # create new user
    new_user = UserModel(
        fname=body.fname,
        lname=body.lname,
        email=body.email,
        hash_password=hash_password,
        createdBy=body.createdBy,
        isActive=body.isActive
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user

def login(body:LoginSchema,db:Session):
    is_user=db.query(UserModel).filter(UserModel.email==body.username).first()
    if not is_user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="This username is not exits!")
    if not verify_password(body.password, is_user.hash_password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="You have entered worng password!")
    
    exp_time = datetime.now(timezone.utc) + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)

    token=jwt.encode(
        {"id": is_user.id, "exp": exp_time},
        settings.SECRET_KEY,
        algorithm=settings.ALGORITHM
        )
    return {"token:":token}

def isAuthorized(request:Request,db:Session):
    try:
        
        token=request.headers.get("authorization")
        if not token:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="You are unauthorized!")
        token=token.split(' ')[-1]
        print(token)
        data = jwt.decode(
            token,
            settings.SECRET_KEY,
            algorithms=[settings.ALGORITHM]
        )

        user_id=data.get("id")
        user=db.query(UserModel).filter(UserModel.id==user_id).first()
        if not user:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="You are unauthorized!")
        return user
    except ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token expired")

    except InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid token")
