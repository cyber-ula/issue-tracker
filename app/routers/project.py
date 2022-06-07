
from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session

from sqlalchemy import func
from typing import List, Optional

from app import oauth2

from .. import models, schemas, oauth2

from ..database import get_db

router = APIRouter(
    prefix="/projects",
    tags=['Projects']
)
#routers allow to clean code and put in different folder to be more clean

@router.get("/",  response_model=List[schemas.ProjectOut])
def get_projects(db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user), 
            limit: int =10, skip: int=0, search: Optional[str] = ""):

   
    #by default join is left join outer
    projects = db.query(models.Project, func.count(models.Member.project_id).label("members")).join(
        models.Member, models.Member.project_id == models.Project.id, isouter = True).group_by(
            models.Project.id).filter(models.Project.name.contains(search)).limit(limit).offset(skip).all()
    #print(results)

    return projects

@router.post("/", status_code = status.HTTP_201_CREATED, response_model=schemas.Project)
def create_projects(post: schemas.ProjectCreate, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):

    
    new_project = models.Project(owner_id = current_user.id, **post.dict())
    db.add(new_project)
    db.commit()
    db.refresh(new_project)

    return new_project

#id --- path parameter

@router.get("/{id}", response_model=schemas.ProjectOut)
def get_project(id: int, response: Response, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):


    project = db.query(models.Project, func.count(models.Member.project_id).label("members"), func.count(models.Bug.project_id).label("bugs")).join(
        models.Member, models.Member.project_id == models.Project.id, isouter = True).filter(models.Project.id ==id).group_by(
            models.Project.id).first()
    
    if not project:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                detail=  f"Project with id: {id} was not found")
        
    # if project[0].owner_id!= current_user.id:
    #      raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to perform requested action")

    return project

@router.delete("/{id}", status_code = status.HTTP_204_NO_CONTENT)
def delete_project(id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):

    

    project_query = db.query(models.Project).filter(models.Project.id == id)
    project=project_query.first()

    if project == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail = f"Project with id: {id} does not exist")

    if project.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to perform requested action")

    project_query.delete(synchronize_session=False)
    db.commit()
    return Response(status_code = status.HTTP_204_NO_CONTENT)

@router.put("/{id}", response_model=schemas.Project)
def update_project(id: int, updated_post: schemas.ProjectCreate, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):

    

    project_query = db.query(models.Project).filter(models.Project.id == id)
    project = project_query.first()
    if project == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail = f"project with id: {id} does not exist")

    if project.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to perform requested action")

    project_query.update(updated_post.dict(), synchronize_session=False)
    db.commit()

  

    return project_query.first()