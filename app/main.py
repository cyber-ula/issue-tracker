from fastapi import FastAPI 
from .config import settings
from . import models
from .database import engine
from .routers import auth,project,member,user,bug
from fastapi.middleware.cors import CORSMiddleware



print(settings.database_name)
models.Base.metadata.create_all(bind=engine)
app = FastAPI()

origins = ['*'] # '*' means every single domain can communicate with us:)

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins, #we can specify here what domain can talk to our api
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(project.router)
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(member.router)
app.include_router(bug.router)


@app.get("/")
def root():
    return {"message": "Issue Tracker"}