from multiprocessing.dummy import Array
from typing import List
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql.expression import text
from sqlalchemy.sql.sqltypes import TIMESTAMP
from .database import Base


class Project(Base):
    __tablename__ = 'projects'

    id = Column(Integer, primary_key=True, nullable=False)
    name= Column(String, nullable=False)
    description = Column(String, nullable=False)
    owner_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default= text('NOW()'))
    owner = relationship("User")



class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, nullable=False)
    email = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default= text('NOW()'))

class Member(Base):
    __tablename__ = 'members'

    user_id =Column(Integer, ForeignKey(
        "users.id", ondelete = "CASCADE"), primary_key=True)
    project_id =Column(Integer, ForeignKey(
        "projects.id", ondelete="CASCADE"), primary_key=True)
    joined_at=Column(TIMESTAMP(timezone=True), nullable=False, server_default= text('NOW()'))

class Bug(Base):
    __tablename__='bugs'
    id = Column(Integer, primary_key=True, nullable=False)
    title=Column(String, nullable=False)
    description=Column(String, nullable=False)
    priority=Column(String, nullable=False)
    status = Column(String, nullable=False)
    project_id =Column(Integer, ForeignKey(
        "projects.id", ondelete="CASCADE"))
    user_id =Column(Integer, ForeignKey(
        "users.id", ondelete="CASCADE"))
    openedbyId = Column(Integer, ForeignKey("users.id", ondelete = "CASCADE"), nullable=True)
    opened_at = Column(TIMESTAMP(timezone=True), nullable=True, server_default= text('NOW()'))
    closedbyId =  Column(Integer, ForeignKey("users.id", ondelete = "CASCADE"), nullable=True)
    closed_at =  Column(TIMESTAMP(timezone=True), nullable=False, server_default= text('NOW()'))
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default= text('NOW()'))
    isResolved = Column(Boolean, nullable=False, server_default=text('false'))
    project = relationship("Project")
    
class Notes(Base):
    __tablename__ = 'notes'
    note = Column(String, nullable=False)
    bug_id = Column(Integer, ForeignKey(
        "bugs.id", ondelete = "CASCADE"), primary_key=True)
    user_id = Column(Integer, ForeignKey(
        "users.id", ondelete = "CASCADE"), primary_key=True)
    project_id = Column(Integer, ForeignKey(
        "projects.id", ondelete = "CASCADE"), primary_key=True)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default= text('NOW()'))
    updated_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default= text('NOW()'))
    bug = relationship("Bug")

   


