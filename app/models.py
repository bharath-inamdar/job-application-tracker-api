from pydantic import BaseModel, EmailStr, Field
from typing import Literal


class JobApplication(BaseModel):
    company: str = Field(..., min_length=1, max_length=100)
    role: str = Field(..., min_length=1, max_length=100)
    status: Literal["Applied", "Interview", "Rejected", "Offer"]


# Pydantic models for user registration and login
class UserRegister(BaseModel):
    username: str
    email: EmailStr
    password: str = Field(..., min_length=8)


class UserLogin(BaseModel):
    email: EmailStr
    password: str = Field(..., min_length=8)


class ApplicationResponse(BaseModel):
    message: str
    id: int


class LoginResponse(BaseModel):
    access_token: str
    token_type: str


class UserRegisterResponse(BaseModel):
    message: str
    user_id: int
    username: str