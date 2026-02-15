from fastapi import HTTPException
from sqlalchemy.orm import Session
from src.user.dtos import UserSchema
from src.user.models import UserModel
from pwdlib import PasswordHash


password_hash = PasswordHash.recommended()


def get_password_hash(password):
    return password_hash.hash(password)


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
        password=hash_password,
        createdBy=body.createdBy,
        isActive=body.isActive
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return {"status": "success", "msg": "Registered successfully"}
