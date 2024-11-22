from flask import jsonify, request
from http import HTTPStatus

from . import app, db
from .models import URLMap
from .utils import get_unique_short_id, correct_short


@app.route('/api/id/', methods=['POST'])
def add_link():
    data = request.get_json()
    if data is None:
        return jsonify({'error': 'Отсутствует тело запроса'}), 400
    elif 'url' not in data:
        return jsonify({'error': '"url" является обязательным полем!'}), 400

    if data.get('custom_id'):
        if len(data['custom_id']) > 16 or not correct_short(data['custom_id']):
            return jsonify({'error': 'Указано недопустимое имя для короткой ссылки'}), 400
        elif URLMap.query.filter_by(short=data['custom_id']).first() is not None:
            return jsonify({'error': f'Имя "{data["custom_id"]}" уже занято.'}), 400
    else:
        data['custom_id'] = get_unique_short_id()

    link = URLMap()
    link.from_dict(data)
    db.session.add(link)
    db.session.commit()

    return jsonify(link.to_dict()), HTTPStatus.CREATED


@app.route('/api/id/<path:short_id>/', methods=['GET'])
def get_opinion(short_id):
    link = URLMap.query.filter_by(short=short_id).first()

    if link is None:
        return jsonify({'error': 'Указанный id не найден'}), HTTPStatus.NOT_FOUND

    return jsonify({'url': link.original}), HTTPStatus.OK
