from app import create_app,db
from app.models import User,Conversation,Videos
from app.search import add_to_index,query_index
from app.videos.videos_functions import generate_other_names
app = create_app()
@app.shell_context_processor
def make_shell_context():
    return {'user':User,'conversation':Conversation,'db':db,'add':add_to_index,'query':query_index,'generate':generate_other_names,'vid':Videos}