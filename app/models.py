from app import db,login
from datetime import datetime
from werkzeug.security import generate_password_hash,check_password_hash 
from flask_login import UserMixin
import enum
from app.search import add_to_index,remove_index,query_index
from flask import url_for
from app.videos_functions import generate_other_names
import json
from app.chat import chat
class BloodGroup(enum.Enum):
    a_positive = 'A+'
    b_positive = 'B+'
    ab_positive = 'AB+'
    o_positive = 'O+'
    a_negative = 'A-'
    b_negative = 'B-'
    ab_negative = 'AB-'
    o_negative = 'O-'
class Genotype(enum.Enum):
    AA = 'AA'
    AS = 'AS'
    SS = 'SS'
    SC = 'SC'
    AC = 'AC'

class PaginatedAPIMixin(object):
    @staticmethod
    def to_collection_dict(query,page,per_page,endpoint,**kwargs):
        resources = query.paginate(page=page,per_page=per_page,error_out=False)
        data = {
            'chats':[item.to_dict() for item in resources.items],
            '_meta':{
                'page':page,
                'per_page':per_page,
                'total_pages':resources.pages,
                'total_items':resources.total
            },
            '_links':{
                'self':url_for(endpoint,page=page,per_page=per_page,**kwargs),
                'prev':url_for(endpoint,page=page-1,per_page=per_page,**kwargs) if resources.has_prev else None,
                'next':url_for(endpoint,page=page+1,per_page=per_page,**kwargs) if resources.has_next else None,
            }
        }
        return data
class SeachableMixin(object):
    @classmethod
    def search(cls,expression,page,per_page):
        ids,total = query_index(cls.__tablename__,expression,page,per_page)
        if total == 0:
            return [],0
        when = []
        for i in range(len(ids)):
            when.append((ids[i],i))
        return cls.query.filter(cls.id.in_(ids)).order_by(db.case(*when,value=cls.id)),total
    
    @classmethod
    def before_commit(cls,session):
        session._changes = {
                            'add':list(session.new),
                            'update':list(session.dirty),
                            'delete':list(session.deleted)
        }
    @classmethod
    def after_commit(cls,session):
        for obj in session._changes['add']:
            if isinstance(obj,SeachableMixin):
                add_to_index(obj.__tablename__,obj)
        for obj in session._changes['update']:
            if isinstance(obj,SeachableMixin):
                add_to_index(obj.__tablename__,obj)
        for obj in session._changes['delete']:
            if isinstance(obj,SeachableMixin):
                remove_index(obj.__tablename__,obj)
        session._changes = None

    @classmethod
    def reindex(cls):
        for obj in cls.query:
            add_to_index(cls.__tablename__,obj)
db.event.listen(db.session,'before_commit',SeachableMixin.before_commit)
db.event.listen(db.session,'after_commit',SeachableMixin.after_commit)
class User(UserMixin,db.Model):
    id = db.Column(db.Integer,primary_key=True)
    firstname = db.Column(db.String(25),nullable = False)
    lastname = db.Column(db.String(25),nullable = False)
    username = db.Column(db.String(25),unique=True,nullable = False)
    email =  db.Column(db.String(),unique=True,nullable = False)
    date_joined = db.Column(db.Date,default=datetime.utcnow)
    password_hash = db.Column(db.String(120),nullable = False)
    bloodgroup = db.Column(db.Enum(BloodGroup))
    genotype = db.Column(db.Enum(Genotype))
    medical_history = db.Column(db.Text)
    conversations = db.Relationship('Conversation',backref = 'user')
    
    
    def __repr__(self):
        return f'<User : {self.username}, Email : {self.email}>'
    

    def set_password(self,password):
        self.password_hash = generate_password_hash(password)


    def check_password(self,password):
        return check_password_hash(self.password_hash,password)

    def conversations_history_by_last_created(self):
        history = Conversation.query.filter_by(user_id=self.id)
        return history.order_by(Conversation.created_at.desc())
    def conversations_history_by_last_updated(self):
        history = Conversation.query.filter_by(user_id=self.id)
        return history.order_by(Conversation.modified_at.desc())    
    def to_dict(self):
        data = {
            'id' : self.id,
            'first_name':self.firstname,
            'last_name': self.lastname,
            'username':self.username,
            'email':self.email,
            'bloodgroup':self.bloodgroup.value,
            'genotype':self.genotype.value,
            'medical_history':self.medical_history,
            '_links':{
                'self': url_for('api.get_user',id=self.id),
                'conversations':url_for('api.get_chats',id=self.id)}
        }
        return data
    def from_dict(self,data,new_user=False):
        for field in ['first_name','last_name','username','email','bloodgroup','genotype','medical_history']:
            if field in data:
                setattr(self,field,data[field])
        if new_user and 'password' in data:
            self.set_password(data['password'])



class Conversation(SeachableMixin,PaginatedAPIMixin,db.Model):
    __searchable__ = ['title','message']
    id = db.Column(db.Integer,primary_key=True)
    conversation_no =  db.Column(db.Integer,nullable = False)
    created_at = db.Column(db.Date,default=datetime.utcnow)
    modified_at = db.Column(db.Date,default=datetime.utcnow)
    title = db.Column(db.String(120),nullable = False)
    message = db.Column(db.Text,nullable = False)
    is_dict_done = db.Column(db.Boolean,nullable=True)
    search_keywords = db.Column(db.Text)
    user_id = db.Column(db.Integer,db.ForeignKey('user.id'))

    def __repr__(self):
        return f'<User : {self.user_id} Conversation_Number : {self.conversation_no}, Title : {self.title}, Created : {self.created_at}>'
    def to_dict(self):
        data = {
            'id' : self.id,
            'conversation_no':self.conversation_no,
            'created_at': self.created_at.isoformat() + 'Z',
            'modified_at':self.modified_at.isoformat() + 'Z',
            'title':self.title,
            'message':json.loads(self.message),
            '_links':self.search_keywords
        }
        return data
    def from_dict(self,user_id,conversation_no=None,new_chat=False,data=None):
        if new_chat:
            message = chat('[]')
            message.add_system_message()
            message.get_response()
            self.created_at = datetime.utcnow()
            self.conversation_no = conversation_no
            self.title = f'Untitled_{conversation_no}'
            self.message = message.return_all_message()
            self.modified_at = datetime.utcnow()
            self.user_id = user_id
            self.is_dict_done = False
        if not new_chat:
            message = chat(self.message)
            message.add_user_message(data['user_message'])
            self.message = message.return_all_message()
            self.modified_at = datetime.utcnow()
            #Bot message adeed
            message = chat(self.message)
            message.get_response()
            response = message.get_dict_response(is_dict_done=self.is_dict_done,text = data['user_message'])
            if response:
                search_keywords = json.loads(response)['FirstAid_searchwords']
                if search_keywords:
                    search = [Videos.search(keyword,1,2) for keyword in search_keywords]
                    return_link = {search[i][0].all()[0].name:search[i][0].all()[0].url for i in range(len(search)) if search[i][1]['value']!=0}
                    self.search_keywords = repr(return_link)
                    self.is_dict_done = True
            self.message = message.return_all_message()
            self.modified_at = datetime.utcnow()

class Videos(SeachableMixin,db.Model):
    __searchable__ = ['name','other_names']
    id = db.Column(db.Integer,primary_key=True)
    url =  db.Column(db.String(100),nullable = False,unique=True)
    name = db.Column(db.Text,nullable=False)
    other_names = db.Column(db.Text,nullable=False)


    def __repr__(self):
        return f'<Videos : {self.name}, Link : {self.url}>'

    def from_dict(self,data):
        self.other_names = repr(generate_other_names(data['name']))
        self.name = data['name']
        self.url = data['url']

    def to_dict(self):
        data = {
            'url':self.url,
            'name':self.name,
            'other_names':eval(self.other_names)
        }
        return data
@login.user_loader
def load_user(id):
    return db.session.get(User,int(id))
