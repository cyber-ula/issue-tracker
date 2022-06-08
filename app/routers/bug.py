
from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session

from sqlalchemy import func
from typing import List, Optional

from app import oauth2

from .. import models, schemas, oauth2

from ..database import get_db

router = APIRouter(
    prefix="/bugs",
    tags=['Bugs']
)


@router.get("/count",  response_model=List[schemas.ProjectOutBug])
def get_number_bugs(db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user), 
            limit: int =10, skip: int=0, search: Optional[str] = ""):

   
    #by default join is left join outer
    projects = db.query(models.Project, func.count(models.Bug.project_id).label("bugs")).join(
        models.Bug, models.Bug.project_id == models.Project.id, isouter = True).group_by(
            models.Project.id).all()
    #print(results)

    return projects



@router.get("/",  response_model=List[schemas.Bug])
def get_bugs(db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):

    bugs = db.query(models.Bug).all()

    return bugs

@router.get("/{id}", response_model=schemas.Bug)
def get_bug(id: int, response: Response, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):


    bug = db.query(models.Bug).filter(models.Bug.id ==id).first()
    
    if not bug:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                detail=  f"Bug with id: {id} was not found")
        
    # if project[0].owner_id!= current_user.id:
    #      raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to perform requested action")

    return bug


@router.post("/", status_code = status.HTTP_201_CREATED, response_model=schemas.Bug)
def create_bug(bug: schemas.BugCreate, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):

    
    new_bug = models.Bug(openedbyId=current_user.id, user_id =current_user.id, **bug.dict())
    print(new_bug)
    db.add(new_bug)
    db.commit()
    db.refresh(new_bug)
    

    return new_bug

@router.delete("/{id}", status_code = status.HTTP_204_NO_CONTENT)
def delete_bug(id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):

    

    bug_query = db.query(models.Bug).filter(models.Bug.id == id)
    bug=bug_query.first()

    if bug == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail = f"Bug with id: {id} does not exist")

    
    bug_query.delete(synchronize_session=False)
    db.commit()
    return Response(status_code = status.HTTP_204_NO_CONTENT)

@router.put("/{id}", response_model=schemas.Bug)
def update_bug(id: int, updated_bug: schemas.BugCreate, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):

    

    bug_query = db.query(models.Bug).filter(models.Bug.id == id)
    bug = bug_query.first()
    if bug == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail = f"bug with id: {id} does not exist")

    # if project[0].owner_id != current_user.id:
    #     raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to perform requested action")

    bug_query.update(updated_bug.dict(), synchronize_session=False)
    db.commit()

  

    return bug_query.first()