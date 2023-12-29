from app.api import bp
from flask import jsonify,request,url_for
from app.models import Videos
from app.api.errors import bad_request
from app import db

@bp.route('/videos/<int:id>',methods=['GET'])
def get_video(id):
    data = Videos.query.get_or_404(id).to_dict()
    return jsonify(data)

@bp.route('/videos',methods=['POST'])
def create_videos_url():
    data =request.get_json() or {}
    if 'url' not in data or 'name' not in data:
        return bad_request('Must include url and name of the video')
    if Videos.query.filter_by(url=data['url']).first():
        return bad_request(f'Url - {data["url"]} exist in the database already!')
    video = Videos()
    video.from_dict(data)
    db.session.add(video)
    db.session.commit()
    response = jsonify(video.to_dict())
    response.status_code=201
    response.headers['location'] = url_for('api.get_video',id=video.id)
    return response