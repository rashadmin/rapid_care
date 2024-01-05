from app import db
from app.main import bp
from flask import render_template,url_for,redirect,flash,request,current_app
from app.main.form import Chatbot,NewChat,Edit_Profile
from flask_login import current_user,login_user,logout_user,login_required
from app.models import User,Conversation
from urllib.parse import urlsplit
from datetime import datetime
from app.chat.chat import chat
from config import Config
@bp.route('/')
@bp.route('/index')
@login_required
def index():
    conversation_check = Conversation.query.filter_by(user_id=current_user.id).count()
    return render_template('index.html',title='index',conversation_check=conversation_check)



'''def should_apply_before_request():
    # Check the endpoint to determine whether @before_request should be applied.
    protected_endpoints = ['/chatbot/<chat_id>']
    return request.endpoint in protected_endpoints
'''

@bp.route('/chatbot',methods = ['GET','POST'])
@login_required
def chats():
    page = request.args.get('page',1,type=int)
    conversation = Conversation.query.filter_by(user_id=current_user.id).paginate(page=page,per_page=current_app.config['CHAT_PER_PAGE'],error_out=False)
    prev_url = url_for('main.chats',page=conversation.prev_num) if conversation.has_prev else None
    next_url = url_for('main.chats',page=conversation.next_num) if conversation.has_next else None
    chat_form = NewChat()
    if chat_form.send.data and chat_form.validate():
        conversation_check = Conversation.query.filter_by(user_id=current_user.id).count() + 1
        message = chat('[]')
        message.add_system_message()
        message.get_response()
        conversation = Conversation(conversation_no = conversation_check,title=f'Untitled_{conversation_check}',
                                    message=message.return_all_message(),user=current_user)
        db.session.add(conversation)
        db.session.commit()
        return redirect(url_for('main.chatbot',chat_id=conversation_check))
    return render_template('chat.html',conversation=conversation,prev_url=prev_url,chat_form=chat_form,next_url=next_url)

@bp.route('/chatbot/<chat_id>',methods = ['GET','POST'])
@login_required
def chatbot(chat_id):
    conversation = Conversation.query.filter_by(user_id=current_user.id).first()
    if conversation is None:
        message = chat('[]')
        message.add_system_message()
        message.get_response()
        conversation = Conversation(conversation_no = 1,title=f'Untitled_1',
                                    message=message.return_all_message(),user=current_user)
        db.session.add(conversation)
        db.session.commit()
        return redirect(url_for('main.chatbot',chat_id=1)) 
    conversation = Conversation.query.filter_by(user_id=current_user.id,conversation_no=chat_id).first_or_404()
    form1 = Chatbot()
    chat_form = NewChat()
    if chat_form.send.data and chat_form.validate():
        conversation_check = Conversation.query.filter_by(user_id=current_user.id).count() + 1
        message = chat('[]')
        message.add_system_message()
        message.get_response()
        conversation = Conversation(conversation_no = conversation_check,title=f'Untitled_{conversation_check}',
                                    message=message.return_all_message(),user=current_user)
        db.session.add(conversation)
        db.session.commit()
        return redirect(url_for('main.chatbot',chat_id=conversation_check))
    if form1.submit.data and form1.validate():
        print(form1.message.data)
        #User's message added
        message = chat(conversation.message)
        message.add_user_message(form1.message.data)
        conversation.message = message.return_all_message()
        conversation.modified_at = datetime.utcnow()
        flash('Successfully sent message in')
        #add a new message to the current conversation
        #Bot message adeed
        message = chat(conversation.message)
        flash('Expecting a response')
        message.get_response()
        conversation.message = message.return_all_message()
        conversation.modified_at = datetime.utcnow()

        db.session.commit()
        
        return redirect(url_for('main.chatbot',chat_id=conversation.conversation_no))
    return render_template('chatbot.html',title='login',form1=form1,chat_form=chat_form,conversation=conversation)

@bp.route('/editprofile',methods=['GET','POST'])
@login_required
def EditProfile():
    form = Edit_Profile()
    if form.validate_on_submit():
        current_user.bloodgroup = form.bloodgroup.data
    if form.validate_on_submit():
        current_user.genotype = form.genotype.data
        current_user.medical_history = form.medical_history.data
        db.session.commit()
        return redirect(url_for('main.index'))
    elif request.method == 'GET':
        form.bloodgroup.data = current_user.bloodgroup
        form.genotype.data = current_user.genotype 
        form.medical_history.data = current_user.medical_history 
    return render_template('edit_profile.html',title='edit_profile',form=form)
