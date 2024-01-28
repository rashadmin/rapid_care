from app.api import bp
from flask import jsonify,request,url_for
from app.models import User,Conversation,Anonyuser
from app.api.errors import bad_request
from app import db
from app.maps.hospital_filter import get_places_info

@bp.route('/anony_users/<string:user_id>/hospital',methods=['GET'])
def hospital_info_for_anony(user_id):
    hospital_info = Conversation.query.filter_by(anony_user_id=user_id).first().to_hospital_dict()
    if hospital_info is None:
        return jsonify({'message':None})
    user_info = Anonyuser.query.filter_by(username=user_id).first().to_dict()
    if '_links' in user_info:
        user_info.pop('_links')
    user_info['username'] = 'Anonymous'
    
    hospital_info.update(user_info)
    return jsonify(hospital_info)

@bp.route('/hospital',methods=['GET'])
def hospital_filter():
    return get_places_info()