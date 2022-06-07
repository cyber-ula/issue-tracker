import pytest
from app import  schemas


def test_get_all_projects(authorized_client, test_projects):
    res = authorized_client.get("/projects/")
    def validate(project):
        return schemas.ProjectOut(**project)

    projects_map = map(validate, res.json())
    projects_list = list(projects_map)
    print(list(projects_list))
    assert len(res.json()) == len(test_projects)
    assert res.status_code == 200

def test_unauthorized_user_get_all_projects(client):
    res = client.get("/projects/")
    assert res.status_code == 401

def test_unauthorized_user_get_one_project(client, test_projects):
    res = client.get(f"/projects/{test_projects[0].id}")
    assert res.status_code == 401

def test_get_one_project_not_exist(authorized_client):
    res = authorized_client.get(f"/projects/88888")
    assert res.status_code == 404

def test_get_one_project(authorized_client, test_projects):
    res = authorized_client.get(f"/projects/{test_projects[0].id}")
    project = schemas.ProjectOut(**res.json()) #unpack res, we have pydantic model
    assert project.Project.id == test_projects[0].id

@pytest.mark.parametrize("name, description",[
    ("awesome new title", "awesome new content"),
    ("favourite new pizza", "I love pepperoni"),
    ("fastapi title", "awesome new api")

])
def test_create_project(authorized_client, test_user, test_projects, name, description):
    res = authorized_client.post("/projects/", json = {"name": name, "description": description})
    created_post = schemas.Project(**res.json())

    assert res.status_code == 201
    assert created_post.name == name
    assert created_post.description == description
    assert created_post.owner_id == test_user['id']

def test_unauthorized_user_create_project(client, test_user, test_projects):
    res = client.post("/projects/", json = {"name": "arbitrary name", "description": "hdkakjdjj"}) 
    assert res.status_code == 401

def test_authorized_user_delete_post(client, test_user, test_projects):
    res = client.delete(f"/projects/{test_projects[0].id}") 
    assert res.status_code == 401

def test_delete_post_success(authorized_client, test_user, test_projects):
    res = authorized_client.delete(f"/projects/{test_projects[0].id}") 
    assert res.status_code == 204

def test_delete_not_exist(authorized_client, test_user, test_projects):
    res = authorized_client.delete(f"/projects/897990333") 
    assert res.status_code == 404

def test_delete_other_user_project(authorized_client, test_user, test_projects):
    res = authorized_client.delete(f"/projects/{test_projects[3].id}") 
    assert res.status_code == 403

def test_update_project(authorized_client, test_user, test_projects):
    data = {
        "name":"updated name",
        "description":"updated description",
        "id":test_projects[0].id

    }

    res = authorized_client.put(f"/projects/{test_projects[0].id}", json = data)
    updated_post = schemas.Project(**res.json())
    assert res.status_code == 200
    assert updated_post.name == data['name']
    assert updated_post.description == data['description']

def test_update_other_user_project(authorized_client, test_user, test_user2, test_projects):
    data = {
        "name":"updated title",
        "description":"updated content",
        "id":test_projects[3].id
    }
    res = authorized_client.put(f"/projects/{test_projects[3].id}", json = data)
    assert res.status_code == 403

def test_authorized_user_update_project(client, test_user, test_projects):
    res = client.put(f"/projects/{test_projects[0].id}") 
    assert res.status_code == 401

def test_update_not_exist(authorized_client, test_user, test_projects):
    data = {
        "name":"updated name",
        "description":"updated description",
        "id":test_projects[3].id
    }
    res = authorized_client.put(f"/projects/897990333", json = data) 
    assert res.status_code == 404
