from flask import Blueprint

main = Blueprint('main', __name__)  # Creates main blueprint

# Imports files necessary for this package
from VOH.main import views
from VOH.main import ta_view
from VOH.main import student_view
from VOH.main import socket_manager

from init_db import *

create_ta_list("VOH/static/data/ta_netids.csv")  # Creates list of TAs in mongoDB
create_student_list("VOH/static/data/student_netids.csv") # Creates list of students in mongoDB
