from .. import redis_store
from ..service.utils import encode_to_base62


class TestCreateShortUrl:
    def test_ok(self, client):
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
    
    def test_not_url(self, client):
        counter = redis_store.get('counter')
        if counter:
            counter = int(counter.decode('utf-8'))
        else:
            # In case app was never run and tests executed for the first time
            counter = 1e7
        code = encode_to_base62(counter)
        data= {
            'fullUrl': 'string'
        }
        response = client.post('/full-url', json=data)
        assert response.status_code == 400
        assert response.get_data().decode('utf-8') == 'Please provide valid url'
    
    def test_no_request_data(self, client):
        counter = redis_store.get('counter')
        if counter:
            counter = int(counter.decode('utf-8'))
        else:
            # In case app was never run and tests executed for the first time
            counter = 1e7
        code = encode_to_base62(counter)
        data= dict()
        response = client.post('/full-url', json=data)
        assert response.status_code == 400
        assert response.get_data().decode('utf-8') == 'No url data'

    def test_http_added(self, client):
        data= {
            'fullUrl': 'example.com'
        }
        response = client.post('/full-url', json=data)
        short_code_response = response.get_data().decode('utf-8').split('/')[-1]
        assert response.status_code == 200
        assert redis_store.get(short_code_response).decode('utf-8') == 'http://example.com'


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
