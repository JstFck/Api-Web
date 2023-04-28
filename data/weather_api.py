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
        'apikey': request.args.get('apikey'),
        'um': request.args.get('um'),
        'lang': request.args.get('lang'),
        'days': request.args.get('days'),
        'wind': request.args.get('wind'),
    }
    db_sess = db_session.create_session()
    if params['apikey']:
        for user in db_sess.query(User).all():
            if params['apikey'] == user.apikey:
                if params['city']:
                    res = write_request(city=params['city'],
                                        days=params['days'] if params['days'] else '0',
                                        um=params['um'] if params['um'] else 'm',
                                        lang=params['lang'] if params['lang'] else 'en',
                                        wind=params['wind'] if params['wind'] else '')
                    if params['days']:
                        if params['days'] == '1':
                            result = {
                                params['city']: {
                                    'now': res[:4],
                                    res[4]: {
                                        'day': [res[5], res[7], res[9]],
                                        'night': [res[6], res[8], res[10]]}
                                }
                            }
                        elif params['days'] == '2':
                            result = {
                                params['city']: {
                                    'now': res[:4],
                                    res[4]: {
                                        'day': [res[5], res[7], res[9]],
                                        'night': [res[6], res[8], res[10]]},
                                    res[11]: {
                                        'day': [res[12], res[14], res[16]],
                                        'night': [res[13], res[15], res[17]]}
                                }
                            }
                        else:
                            result = {
                                params['city']: {
                                    'now': res[:4],
                                    res[4]: {
                                        'day': [res[5], res[7], res[9]],
                                        'night': [res[6], res[8], res[10]]},
                                    res[11]: {
                                        'day': [res[12], res[14], res[16]],
                                        'night': [res[13], res[15], res[17]]},
                                    res[18]: {
                                        'day': [res[19], res[21], res[23]],
                                        'night': [res[20], res[22], res[24]]}
                                }
                            }
                        return jsonify(result)
                    return jsonify({
                        params['city']: res[:4]
                    })
                return jsonify({
                    'error': 'write city to get info'
                })
    return jsonify({'error': 'write apikey to use API'})


def write_request(city, days, um, lang, wind):
    req = f'https://wttr.in/{city}'
    req += f'?m&{days}&lang={lang}&T&n' if um == 'm' else f'?u&{days}&lang={lang}&T&n'
    if wind == 'M':
        req += f'&{wind}'
    response = get(req).text
    res = []
    sign = ['┌', '│', '├', '─', '┬', '┼', '└', '┘', '┐', '┴', '┤']
    for i, j in enumerate(response.split('\n')):
        if i == 5 or i == 7 or i == 10 or i == 16:
            continue
        if i <= 6:
            if j != '':
                res.append(j[15:].strip().strip())
        else:
            if j != '':
                res.append(j.strip())
    result = []
    for k, i in enumerate(res):
        if k in [6, 7, 10, 12, 14, 15, 16, 19, 21, 22, 24, 25, 26, 29, 31]:
            continue
        res2 = i
        for j in sign:
            res2 = res2.replace(j, '')
        result.append(res2.strip())
    result = result[:-1]
    weather = ['\  /', '_ /"".-.', '\_(   ).', '/(___(__)', '.--.', '.-(    ).', '(___.__)__)', '\   /', '.-.',
               '― (   ) ―', '`-’', '/   \ '.strip(), '(   ).', '(___(__)', '‘ ‘ ‘ ‘', '_`/"".-.', ',\_(   ).',
               '_ - _ - _ -', '_ - _ - _', ',\_(   ).']
    arr = []
    for i in result:
        res = i
        for j in weather:
            res = res.replace(j, '').strip()
        for j in res.rsplit(' ' * 8):
            if j == '':
                continue
            if j.startswith(','):
                arr.append(j[1:].strip())
            else:
                arr.append(j.strip())
    return arr[1:]
