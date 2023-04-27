from flask import Blueprint, jsonify, request
from requests import get
from . import db_session
from .users import User

blueprint = Blueprint(
    'weather_api',
    __name__,
    template_folder='templates'
)


@blueprint.route('/api')
def api():
    params = {
        'city': request.args.get('city'),
        'apikey': request.args.get('apikey')
    }
    db_sess = db_session.create_session()
    if params['apikey']:
        for user in db_sess.query(User).all():
            if params['apikey'] == user.apikey:
                if params['city']:
                    response = get(f'https://wttr.in/{params["city"]}?0&T').text
                    res = []
                    for i in response.split('\n'):
                        if i != '':
                            res.append(i[15:].strip())
                    return jsonify({
                        params['city']: res[2:-2]
                    })
                return jsonify({
                    'error': 'write city to get info'
                })
    return jsonify({'error': 'write apikey to use API'})
