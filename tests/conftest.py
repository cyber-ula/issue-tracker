"""
Special file for pytest, allows to define fixture, pytest uses in tests
"""

from fastapi.testclient import TestClient
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from app.main import app
from app.config import settings
from app.database import get_db, Base
from app.oauth2 import create_access_token
from app import models

SQLALCHEMY_DATABASE_URL = f'postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}_test'

engine = create_engine(SQLALCHEMY_DATABASE_URL)

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind = engine)

#Base.metadata.create_all(bind=engine)

#Base = declarative_base()

# Dependency
# def override_get_db():
#     db = TestingSessionLocal()
#     try:
#         yield db
#     finally:
#         db.close()



#client = TestClient(app)

@pytest.fixture()
def session():
    print("my session fixture run")
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)

    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()




@pytest.fixture()
def client(session):
    #run our code before we run our test

    def override_get_db():
        try:
            yield session
        finally:
            session.close()
    
    # Base.metadata.drop_all(bind=engine)
    # Base.metadata.create_all(bind=engine)
    #command.upgrade("head")
    app.dependency_overrides[get_db] = override_get_db

    yield  TestClient(app) #run test
    #command.downgrade("base")
    
    
    
    #run our code after our test finished
   # Base.metadata.drop_all(bind=engine)

# now we dont need to worry to duplicate our user
@pytest.fixture
def test_user2(client):
    user_data = {"email": "cyberula123@gmail.com",
                "password":"password123"}

    res = client.post("/users/", json = user_data)

    assert res.status_code == 201
    print(res.json())
    new_user = res.json()
    new_user['password'] = user_data['password']
    
    return new_user

@pytest.fixture
def test_user(client):
    user_data = {"email": "cyberula@gmail.com",
                "password":"password123"}

    res = client.post("/users/", json = user_data)

    assert res.status_code == 201
    print(res.json())
    new_user = res.json()
    new_user['password'] = user_data['password']
    
    return new_user


@pytest.fixture
def token(test_user):
    return create_access_token({"user_id": test_user['id']})


@pytest.fixture
def authorized_client(client, token):
    client.headers = {
        **client.headers,
        "Authorization": f"Bearer {token}"

    }

    return client

@pytest.fixture
def test_projects(test_user, session, test_user2):
    projects_data = [{
        "name": "first title",
        "description": "first content",
        "owner_id": test_user['id']
    }, {
        "name": "2nd title",
        "description": "2nd content",
        "owner_id": test_user['id']
    },
        {
        "name": "3rd title",
        "description": "3rd content",
        "owner_id": test_user['id']
    },
     {
        "name": "3rd title",
        "description": "3rd content",
        "owner_id": test_user2['id']
    }]

    def create_post_model(project):
        return models.Project(**project)

    project_map = map(create_post_model, projects_data)
    projects = list(project_map)

    session.add_all(projects)
    # session.add_all([models.Post(title="first title", content="first content", owner_id=test_user['id']),
    #                 models.Post(title="2nd title", content="2nd content", owner_id=test_user['id']), models.Post(title="3rd title", content="3rd content", owner_id=test_user['id'])])
    session.commit()

    project = session.query(models.Project).all()
    return project


@pytest.fixture
def test_bugs(test_user, session, test_user2, test_projects):
    bugs_data = [
        {
        "title": "first title",
        "description": "first content",
        "priority": "low",
        "status": "Open",
        "user_id": test_user['id'],
        "project_id": test_projects[0].id
    }, 
        {
        "title": "second title",
        "description": "second content",
        "priority": "high",
        "status": "Testing",
        "user_id": test_user['id'],
        "project_id": test_projects[1].id

    },
        {
        "title": "third title",
        "description": "third content",
        "priority": "medium",
        "status": "Open",
        "user_id": test_user['id'],
        "project_id": test_projects[2].id

    },
     {
       "title": "third title",
        "description": "third content",
        "priority": "medium",
        "status": "Open",
        "user_id": test_user2['id'],
         "project_id": test_projects[3].id

    }]

    def create_bug_model(bug):
        return models.Bug(**bug)

    bug_map = map(create_bug_model, bugs_data)
    bugs = list(bug_map)

    session.add_all(bugs)
    # session.add_all([models.Post(title="first title", content="first content", owner_id=test_user['id']),
    #                 models.Post(title="2nd title", content="2nd content", owner_id=test_user['id']), models.Post(title="3rd title", content="3rd content", owner_id=test_user['id'])])
    session.commit()

    bug = session.query(models.Bug).all()
    return bug