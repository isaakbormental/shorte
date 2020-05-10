from flask import redirect, render_template, request

from app import app, redis_store
from app.utils import encode_to_base62


@app.route('/')
def index():
    """ return html with main site content """
    return render_template('index.html', title='Shorte')


@app.route('/sh/<short_code>')
def redirect_to_full_url(short_code):
    """ get full url from redis cache and return redirect """
    full_url = redis_store.get(short_code)
    return redirect(full_url, code=302)


@app.route('/full-url', methods=['POST'])
def get_short_link():
    """ shorten url by incrementing links counter and encoding it """
    full_url = request.json.get('fullUrl')
    counter = redis_store.get('counter')
    short_code = encode_to_base62(int(counter))
    redis_store.set(short_code, full_url)
    redis_store.set('counter', int(counter) + 1)
    return f'http://localhost:5000/sh/{short_code}'
