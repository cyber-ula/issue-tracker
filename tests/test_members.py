import pytest
from app import models

@pytest.fixture()
def test_member(test_projects, session, test_user):
    new_vote = models.Member(project_id=test_projects[3].id, user_id=test_user['id'])
    session.add(new_vote)
    session.commit()

    assert new_vote.status_code == 201


def test_member_project_non_exist(authorized_client, test_projects):
    res = authorized_client.post(
        "/member/", json = {"project_id": 88})
    
    assert res.status_code == 404

def test_member_post_unauthorized_user(client, test_projects):
    res = client.post(
        "/member/", json = {"project_id": test_projects[3].id})
    
    assert res.status_code == 401