from app.api import bp
from app.maps import bp as maps_bp
from flask import jsonify,request,url_for
from app.api.errors import bad_request
from threading import Thread
from flask import current_app
from time import time
from app.models import Conversation
'''def send_async_lists(app):
     with app.app_context():
          start.get_top_5()'''
@bp.route('/maps',methods=['GET'])
def gets():
    return maps_bp.hospital_filter_instance.get_top_5()
    #Thread(target=send_async_lists, args=(current_app)).start()



