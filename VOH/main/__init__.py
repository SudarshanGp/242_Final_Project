from flask import Blueprint

main = Blueprint('main', __name__)

from VOH.main import views
from VOH.main import socket_manager