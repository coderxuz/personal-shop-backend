from pydantic import BaseModel

from datetime import datetime

from app.models import UserRole, Gender

class signUp(BaseModel):
    fio: str
    login: str
    password: str
    birthday: datetime  # Default value is set at the database level
    gender: Gender
    address: str
    role: UserRole
    phone:str

class TokenResponse(BaseModel):
    accessToken: str
    refreshToken: str
    role: UserRole

class LoginData(BaseModel):
    login:str
    password:str