import os
from flask import Blueprint
from app import db
import echo

bp = Blueprint('cli', __name__, cli_group=None)

@bp.cli.command('init_db')
def initialize_database():
    """Initialize the database."""
    db.drop_all()
    db.create_all()
    echo('Initialized the database!')
