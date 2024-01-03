from flask import Blueprint
bp = Blueprint('main',__name__)
from app.main import form,routes
from app.chat import chat