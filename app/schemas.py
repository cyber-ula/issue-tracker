from typing import List, Optional
from pydantic import BaseModel, EmailStr
from datetime import datetime

from pydantic.types import conint
from sqlalchemy import Enum

# class Post(BaseModel):
#     title: str
#     content: str
#     published: bool = True
    # rating: Optional[int] = None

class ProjectBase(BaseModel):
    name: str
    description: str

class ProjectCreate(ProjectBase):
    pass

class UserOut(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime

    #Config -- convert the sql alchemy model on dictionary:
    class Config:
        orm_mode = True
        
class Project(ProjectBase):
    id: int
    created_at: datetime
    owner_id: int
    owner: UserOut
    
    class Config:
        orm_mode = True


class ProjectOut(BaseModel):
    Project: Project
    members: int

    class Config:
        orm_mode = True

class ProjectOutBug(BaseModel):
    Project: Project
    bugs: int

    class Config:
        orm_mode = True

class UserCreate(BaseModel):
    email: EmailStr
    password: str



class UserLogin(BaseModel):
    email: EmailStr
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    id: Optional[str] = None


class Member(BaseModel):
    project_id: int
    user_id: Optional[int] = None
    #dir: conint(le=1) 
    
class BugCreate(BaseModel):
    title:str
    description: str
    priority: str
    status: str
    project_id: int

    class Config:
        orm_mode = True

class Bug(BaseModel):
    id: int 
    title:str
    description: str
    priority: str
    status: str
    project_id: int
    user_id:int
    openedbyId: int = None
    opened_at: datetime
    created_at: datetime
    isResolved: bool
    project: Project

    class Config:
        orm_mode = True

class Notes(BaseModel):
    note: str
    project_id: int
    bug_id: int
    dir: conint(le=1) 
    

    class Config:
        orm_mode = True

class NotesOut(BaseModel):
    note: str
    project_id: int
    user_id: int
    bug_id: int
    created_at: datetime
    updated_at: datetime
    bug: Bug
    

    class Config:
        orm_mode = True

#less or equal 1 ---> result: 0 or 1 only


