from flask import redirect, render_template, request, make_response
import validators

from .. import redis_store
from .utils import encode_to_base62
from . import bp



@bp.route('/<short_code>')
def redirect_to_full_url(short_code):
    """ get full url from redis cache and return redirect """
    full_url = redis_store.get(short_code)
    return redirect(full_url, code=302)


@bp.route('/full-url', methods=['POST'])
def get_short_link():
    """ shorten url by incrementing links counter and encoding it """
    full_url = request.json.get('fullUrl')

    # Validate url
    if not full_url:
        return make_response('No url data', 400)
    if len(full_url.split('.')) < 2:
        return make_response('Please provide valid url', 400)
    if full_url.split('://')[0] not in ('http', 'https'):
        full_url = 'http://' + full_url

    counter = redis_store.get('counter')
    short_code = encode_to_base62(int(counter))
    redis_store.set(short_code, full_url)
    redis_store.set('counter', int(counter) + 1)
    return f'http://localhost/{short_code}'
