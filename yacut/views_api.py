from flask import jsonify, request
from http import HTTPStatus

from . import app, db
from .models import URLMap
from .utils import get_unique_short_id, correct_short
from .error_handler import InvalidAPIUsage


@app.route('/api/id/', methods=['POST'])
def add_link():
    data = request.get_json()
    if data is None:
        raise InvalidAPIUsage("Отсутствует тело запроса")
    elif 'url' not in data:
        raise InvalidAPIUsage('"url" является обязательным полем!')
    if data.get('custom_id'):
        if len(data['custom_id']) > 16 or not correct_short(data['custom_id']):
            raise InvalidAPIUsage('Указано недопустимое имя для короткой ссылки')
        elif URLMap.query.filter_by(short=data['custom_id']).first() is not None:
            raise InvalidAPIUsage(f'Имя "{data["custom_id"]}" уже занято.')
    else:
        data['custom_id'] = get_unique_short_id()
    link = URLMap()
    link.from_dict(data)
    db.session.add(link)
    db.session.commit()
    return jsonify(link.to_dict()), HTTPStatus.CREATED
    if 'custom_id' not in data or not data['custom_id']:
        new_short_url = create_random_short_url()
        add_to_database(data['url'], new_short_url)
        return jsonify({
            'url': data['url'],
            'short_link': url_for(
                endpoint='get_unique_short_id',
                _external=True,
                _scheme='http') + new_short_url}), STATUS_CODE_CREATED
    if URLMap.query.filter_by(short=data['custom_id']).first():
        raise InvalidAPIUsage(
            'Предложенный вариант короткой ссылки уже существует.'
        )
    if (not re.match(REGEX, data['custom_id'])
            or len(data['custom_id']) > MAX_CUSTOM_LINK_LENGTH):
        raise InvalidAPIUsage('Указано недопустимое имя для короткой ссылки')
    add_to_database(data['url'], data['custom_id'])
    return jsonify({
        'url': data['url'],
        'short_link': url_for(
            endpoint='get_unique_short_id',
            _external=True,
            _scheme='http') + data['custom_id']}), STATUS_CODE_CREATED


@app.route('/api/id/<path:short_id>/', methods=['GET'])
def get_opinion(short_id):
    link = URLMap.query.filter_by(short=short_id).first()
    if link is None:
        raise InvalidAPIUsage('Указанный id не найден', HTTPStatus.NOT_FOUND)
    return jsonify({'url': link.original}), HTTPStatus.OK
