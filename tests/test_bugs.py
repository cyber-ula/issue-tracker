import pytest
from app import  schemas

def test_get_all_bugs(authorized_client, test_bugs):
    res = authorized_client.get("/bugs/")
    def validate(bug):
        return schemas.Bug(**bug)

    bugs_map = map(validate, res.json())
    bugs_list = list(bugs_map)
    print(list(bugs_list))
    assert len(res.json()) == len(test_bugs)
    assert res.status_code == 200

def test_unauthorized_user_get_all_bugs(client):
    res = client.get("/bugs/")
    assert res.status_code == 401

def test_unauthorized_user_get_one_bug(client, test_bugs):
    res = client.get(f"/bugs/{test_bugs[0].id}")
    assert res.status_code == 401

def test_get_one_project_not_exist(authorized_client):
    res = authorized_client.get(f"/bugs/88888")
    assert res.status_code == 404

def test_get_one_bug(authorized_client, test_bugs):
    res = authorized_client.get(f"/bugs/{test_bugs[0].id}")
    project = schemas.Bug(**res.json()) #unpack res, we have pydantic model
    assert project.project.id == test_bugs[0].id

@pytest.mark.parametrize("title, description, priority, status, project_id",[
    ("awesome new title", "awesome new content", "low", "Open", 1),
    ("favourite new pizza", "I love pepperoni", "medium", "Testing",2),
    ("fastapi title", "awesome new api", "high", "Development",3)

])
def test_create_project(authorized_client, test_user,test_projects, test_bugs, title, description, priority, status, user_id, project_id):
    res = authorized_client.post("/bugs/", json = {"title": title, "description": description, "priority": priority, "status": status, "project_id": project_id})
    created_post = schemas.BugCreate(**res.json())

    assert res.status_code == 201
    assert created_post.title == title
    assert created_post.description == description
    assert created_post.project_id == project_id

def test_unauthorized_user_create_bug(client, test_user, test_bugs, test_projects):
    res = client.post("/bugs/", json = {"title": "arbitrary title", "description": "hdkakjdjj", "priority": "low", "status": "Open", "user_id": test_user['id'], "project_id": test_projects[1].id}) 
    assert res.status_code == 401

def test_authorized_user_delete_bug(client, test_user, test_bugs):
    res = client.delete(f"/bugs/{test_bugs[0].id}") 
    assert res.status_code == 401

def test_delete_bug_success(authorized_client, test_user, test_bugs):
    res = authorized_client.delete(f"/bugs/{test_bugs[0].id}") 
    assert res.status_code == 204

def test_delete_not_exist(authorized_client, test_user, test_projects):
    res = authorized_client.delete(f"/bugs/897990333") 
    assert res.status_code == 404


def test_update_bug(authorized_client, test_user, test_projects, test_bugs):
    data = {
        "title":"updated name",
        "description":"updated description",
        "priority": "low",
        "status": "Open",
        "project_id":test_projects[0].id

    }

    res = authorized_client.put(f"/bugs/{test_bugs[0].id}", json = data)
    updated_bug = schemas.BugCreate(**res.json())
    assert res.status_code == 200
    assert updated_bug.title == data['title']
    assert updated_bug.description == data['description']
    assert updated_bug.priority == data['priority']


def test_authorized_user_update_project(client, test_user, test_bugs):
    res = client.put(f"/bugs/{test_bugs[0].id}") 
    assert res.status_code == 401

def test_update_not_exist(authorized_client, test_user, test_projects):
    data = {
        "title":"updated name",
        "description":"updated description",
        "priority": "low",
        "status": "Open",
        "project_id":test_projects[0].id

    }
    res = authorized_client.put(f"/bugs/897990333", json = data) 
    assert res.status_code == 404
