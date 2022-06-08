from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session, query

from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from .. import schemas, database, models, oauth2
from typing import List
from ..database import get_db
from sqlalchemy import func

router = APIRouter(
    prefix="/notes",
    tags=['Notes']
)



@router.get("/",  response_model=List[schemas.NotesOut])
def get_bugs(db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):

    notes = db.query(models.Notes).all()

    return notes



@router.post("/", status_code=status.HTTP_201_CREATED)
def note(notes: schemas.Notes, db: Session = Depends(database.get_db), current_user: int = Depends(oauth2.get_current_user)):

    project = db.query(models.Project).filter(models.Project.id == notes.project_id).first()
    #print(post)

    if not project:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Project with id: {notes.project_id} does not exist")

    note_query = db.query(models.Notes).filter(models.Notes.project_id == notes.project_id, models.Notes.user_id == current_user.id, models.Notes.bug_id == notes.bug_id)

    found_note = note_query.first()
  
    if (notes.dir == 1):
        if found_note:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                                detail=f"user {current_user.id} has already written on project {notes.project_id}")
        # elif project.owner_id == current_user.id:
        #     raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
        #                         detail=f"user {current_user.id} cannot write on your own note")                       
        new_note = models.Notes(project_id=notes.project_id, user_id=current_user.id, bug_id = notes.bug_id, note = notes.note)
        db.add(new_note)
        print("Done")
        db.commit()
        return {"message": "successfully added note"}
    else:
        if not found_note:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Note does not exist")

        note_query.delete(synchronize_session=False)
        db.commit()

        return {"message": "successfully deleted note"}