from app.api import bp
from flask import jsonify,request,url_for
from app.models import User,Conversation
from app.api.errors import bad_request
from app import db

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
    

@bp.route('/users/<int:id>/chats/<int:chat_id>',methods=['GET'])
def get_chat(id,chat_id):
    data = Conversation.query.filter_by(user_id=id,conversation_no=chat_id).first_or_404().to_dict()
    return jsonify(data)
    

@bp.route('/users/<int:id>/chats/<int:chat_id>',methods=['PUT'])
def update_chat(id,chat_id):
    conversation = Conversation.query.filter_by(user_id=id,conversation_no=chat_id).first_or_404()
    data = request.get_json() or {}
    if  'user_message' not in  data:
        return bad_request('Specify the Conversation number and Ensure message is in data')
    conversation.from_dict(id,data=data)
    db.session.commit()
    return jsonify(conversation.to_dict())

@bp.route('/users/<int:id>',methods=['PUT'])
def update_user(id):
    user = User.query.get_or_404(id)
    data = request.get_json() or {}
    if 'email' in data and data['email'] != user.email and User.query.filter_by(email=data['email']).first():
        return bad_request('please use a different Email Address')
    user.from_dict(data)
    db.session.commit()
    return jsonify(user.to_dict())

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
