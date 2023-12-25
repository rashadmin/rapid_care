from app import create_app,db
from app.models import User,Conversation

app = create_app()

@app.shell_context_processor
def make_shell_context():
    return {'user':User,'conversation':Conversation,'db':db}