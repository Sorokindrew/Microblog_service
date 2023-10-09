def test_working_test(client):
    assert 1 == 1


def test_users_me(client):
    response = client.get('api/users/me')
    print(response.json['user']['name'])
    assert response.status_code == 200