from .. import redis_store
from ..service.utils import encode_to_base62


def test_create_short_lint(client):
    counter = redis_store.get('counter')
    if counter:
        counter = int(counter.decode('utf-8'))
    else:
        # In case app was never run and tests executed for the first time
        counter = 1e7
    code = encode_to_base62(counter)
    data= {
        'fullUrl': 'http://example.com'
    }
    response = client.post('/full-url', json=data)
    short_code_response = response.get_data().decode('utf-8').split('/')[-1]
    assert response.status_code == 200
    assert short_code_response == code


def test_redirect(client):
    # First create short url
    data= {
        'fullUrl': 'http://example.com'
    }
    response = client.post('/full-url', json=data)
    short_code_response = response.get_data().decode('utf-8').split('/')[-1]
    response = client.get(f'/{short_code_response}')
    assert response.status_code == 302
    assert data['fullUrl'] in response.get_data().decode('utf-8')
