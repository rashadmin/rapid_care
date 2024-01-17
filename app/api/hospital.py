from app.api import bp
from flask import jsonify,request,url_for
from app.models import User,Conversation,Anonyuser
from app.api.errors import bad_request
from app import db

@bp.route('/anony_users/<string:user_id>/hospital',methods=['GET'])
def hospital_info_for_anony(user_id):
    hospital_info = Conversation.query.filter_by(anony_user_id=user_id).first().to_hospital_dict()
    return jsonify(hospital_info)