from flask import Blueprint
bp = Blueprint('maps',__name__)



from app.maps import hospital_filter
