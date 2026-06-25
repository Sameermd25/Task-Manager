from pydantic import BaseModel, Field, EmailStr

class TaskCreate(BaseModel):
    title: str = Field(
        min_length=3,
        max_length=100
    )

    description: str = Field(
        min_length=5,
        max_length=500
    )

class UserCreate(BaseModel):
    username: str = Field(
        min_length=3,
        max_length=30
    )

    email: EmailStr

    password: str = Field(
        min_length=6,
        max_length=50
    )

class UserLogin(BaseModel):
    email: EmailStr

    password: str = Field(
        min_length=6,
        max_length=50
    )