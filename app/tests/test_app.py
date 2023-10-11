import pytest


def test_working_test(client):
    assert 1 == 1


def test_users_me(client):
    response = client.get('api/users/me')
    assert response.json['user']['name'] == 'Andrey Sorokin'


@pytest.mark.parametrize('route', ['api/users/me',
                                   'api/users/1',
                                   'api/tweets'])
def test_get_response(client, route):
    response = client.get(route)
    assert response.status_code == 200


def test_add_like(client):
    response = client.post('/api/tweets/1/likes')
    assert response.json['result'] == 'true'


def test_get_tweets(client):
    response = client.get('/api/tweets')
    data = response.json
    assert data['result'] == 'true'
    assert len(data['tweets']) == 41
