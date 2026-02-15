from sqlalchemy import Column, String, Integer, Boolean, DateTime
from datetime import datetime
from src.utils.db import Base


class UserModel(Base):
    __tablename__ = "tbl_user"

    id = Column(Integer, primary_key=True, index=True)

    fname = Column(String(100), nullable=False)
    lname = Column(String(100), nullable=False)

    email = Column(String(150), nullable=False, unique=True, index=True)
    hash_password = Column(String(255), nullable=False)

    createdBy = Column(Integer)
    createdOn = Column(DateTime, default=datetime.utcnow)

    modifiedBy = Column(Integer)
    modifiedOn = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    isActive = Column(Boolean, default=True)

    def __repr__(self):
        return f"<User {self.email}>"

