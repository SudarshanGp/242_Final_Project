from flask import Blueprint

main = Blueprint('main', __name__)

from VOH.main import views
from VOH.main import socket_manager

from init_db import *

create_ta_list("VOH/static/data/ta_netids.csv")
create_student_list("VOH/static/data/student_netids.csv")