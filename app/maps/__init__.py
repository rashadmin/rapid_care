from flask import Blueprint
bp = Blueprint('maps',__name__)
from threading import Thread
from app.maps.hospital_filter import get_top
instantiated = False

# Function to instantiate YourClass
def instantiate_your_class():
    global instantiated
    if not instantiated:
        hospital_filter_instance = get_top()
        bp.hospital_filter_instance = hospital_filter_instance
        Thread(target=bp.hospital_filter_instance.get_top_5()).start()
        instantiated = True

# Register the function to run before each request
@bp.before_app_request
def before_request():
    instantiate_your_class()

from app.maps import hospital_filter
#