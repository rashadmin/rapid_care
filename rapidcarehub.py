from app import create_app,db,socketio
from app.models import User,Conversation,Videos
from app.search import add_to_index,query_index
from app.videos.videos_functions import generate_other_names,return_url
app = create_app()
socketio.run(app,debug=False)
@app.shell_context_processor
def make_shell_context():
    return {'user':User,'conversation':Conversation,'db':db,'add':add_to_index,'query':query_index,'generate':generate_other_names,'vid':Videos,'get':return_url}