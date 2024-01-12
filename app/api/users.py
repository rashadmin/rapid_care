from app.api import bp
from flask import jsonify,request,url_for
from app.models import User,Conversation,Anonyuser
from app.api.errors import bad_request
from app import db
import uuid

################################################################################################################################
# getting user chats
# - normal user
@bp.route('/users/<int:id>/chats/<int:chat_id>',methods=['GET'])
def get_chat(id,chat_id):
    data = Conversation.query.filter_by(user_id=id,conversation_no=chat_id).first_or_404().to_dict()
    return jsonify(data)
# - anonymous user    
@bp.route('/anony_users/<string:user_id>/chat',methods=['GET'])
def get_anony_chat(user_id):
    data = Conversation.query.filter_by(anony_user_id=user_id).first_or_404().to_dict()
    return jsonify(data)
################################################################################################################################


################################################################################################################################
@bp.route('/users/<int:id>',methods=['GET'])
def get_user(id):
    data = User.query.get_or_404(id).to_dict()
    return jsonify(data)

@bp.route('/users/<int:id>/chats',methods=['GET'])
def get_chats(id):
    page = request.args.get('page', 1, type=int)
    per_page = min(request.args.get('per_page', 10, type=int), 100)
    data = Conversation.to_collection_dict(Conversation.query.filter_by(user_id=id),id=id,page=page,per_page=per_page,endpoint='api.get_chats')
    return data
################################################################################################################################


################################################################################################################################
@bp.route('/users/<int:id>/chats/<int:chat_id>',methods=['PUT'])
def update_chat(id,chat_id):
    conversation = Conversation.query.filter_by(user_id=id,conversation_no=chat_id).first_or_404()
    data = request.get_json() or {}
    if  'user_message' not in  data:
        return bad_request('Specify the Conversation number and Ensure message is in data')
    conversation.from_dict(id,data=data)
    db.session.commit()
    return jsonify(conversation.to_dict())

@bp.route('/anony_users/<string:user_id>/chat',methods=['PUT'])
def update_anony_chat(user_id):
    conversation = Conversation.query.filter_by(anony_user_id=user_id).first_or_404()
    data = request.get_json() or {}
    if  'user_message' not in  data:
        return bad_request('Specify and Ensure message is in data')
    conversation.from_dict(user_id,data=data,anony=True)
    db.session.commit()
    return jsonify(conversation.to_dict())

################################################################################################################################


################################################################################################################################

@bp.route('/users/<int:id>',methods=['PUT'])
def update_user(id):
    user = User.query.get_or_404(id)
    data = request.get_json() or {}
    if 'email' in data and data['email'] != user.email and User.query.filter_by(email=data['email']).first():
        return bad_request('please use a different Email Address')
    user.from_dict(data)
    db.session.commit()
    return jsonify(user.to_dict())

@bp.route('/users/user_id',methods=['PUT'])
def update_anony_user(user_id):
    user = Anonyuser.query.query.filter_by(user_id=user_id).first_or_404().to_dict()
    data = request.get_json() or {}
    user.from_dict(data)
    db.session.commit()
    return jsonify(user.to_dict())

################################################################################################################################


################################################################################################################################
@bp.route('/users/<int:id>/chats',methods=['POST'])
def add_chat(id):
    conversation = Conversation()
    conversation_no = Conversation.query.filter_by(user_id=id).count() + 1
    conversation.from_dict(id,conversation_no=conversation_no,new_chat=True)
    db.session.add(conversation)
    db.session.commit()
    response = jsonify(conversation.to_dict())
    response.status_code=201
    response.headers['location'] = url_for('api.get_chat',id=id,chat_id=conversation_no)
    return response

@bp.route('/anony_users/<string:user_id>/chat',methods=['POST'])
def add_anony_chat(user_id):
    conversation = Conversation()
    conversation.from_dict(id,new_chat=True,anony=True)
    db.session.add(conversation)
    db.session.commit()
    response = jsonify(conversation.to_dict())
    response.status_code=201
    response.headers['location'] = url_for('api.get_anony_chat',user_id=user_id)
    return response
################################################################################################################################


################################################################################################################################
@bp.route('/users/<int:id>/chats/<int:chat_id>/hospitaldetail',methods=['GET'])
def get_map(id,chat_id):
    data = Conversation.query.filter_by(user_id=id,conversation_no=chat_id).first_or_404().to_map()
    return jsonify(data)
################################################################################################################################


################################################################################################################################
@bp.route('/users',methods=['POST'])
def create_user():
    data =request.get_json() or {}
    if 'username' not in data or 'email' not in data or 'firstname' not in data or 'lastname' not in data:
        return bad_request('Must include FIRST NAME,LAST_NAME,USERNAME,EMAIL')
    if User.query.filter_by(username=data['username']).first():
        return bad_request(f'Use a different username as {data["username"]} is taken!')
    if User.query.filter_by(username=data['email']).first():
        return bad_request(f'Use a different email as {data["email"]} has been used!')
    user = User()
    user.from_dict(data,new_user=True)
    db.session.add(user)
    db.session.commit()
    response = jsonify(user.to_dict())
    response.status_code=201
    response.headers['location'] = url_for('api.get_user',id=user.id)
    return response


@bp.route('/anony_users',methods=['POST'])
def create_anony_user():
    while True:
        user_id = str(uuid.uuid4())
        if  not Anonyuser.query.filter_by(username=user_id).first():
            print(len(user_id))
            user = Anonyuser()
            data = request.get_json() or {}
            user.from_dict(user_id,data) 
            db.session.add(user)
            db.session.commit()
            response = jsonify(user.to_dict())
            response.status_code=201
            response.headers['location'] = url_for('api.add_anony_chat',user_id=user.username)
            return response
################################################################################################################################





