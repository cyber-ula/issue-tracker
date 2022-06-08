from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session, query

from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from .. import schemas, database, models, oauth2


router = APIRouter(
    prefix="/member",
    tags=['Member']
)


@router.post("/", status_code=status.HTTP_201_CREATED)
def member(member: schemas.Member, db: Session = Depends(database.get_db), current_user: int = Depends(oauth2.get_current_user)):

    project = db.query(models.Project).filter(models.Project.id == member.project_id).first()
    #print(post)

    if not project:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Project with id: {member.project_id} does not exist")

    user = db.query(models.Member).filter(models.Member.user_id == current_user.id).first()
    print(user)

    if user:
         raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail =f'You cannot be member twice')
    new_member = models.Member(project_id=member.project_id, user_id=current_user.id)
    db.add(new_member)
    print("Done")
    db.commit()
    return {"message": "successfully added member to project"}
    
       