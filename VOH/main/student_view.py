from . import main
from VOH.main.forms import ChatForm
from flask import render_template, request, session, jsonify, redirect, url_for
from student import *
from authentication import *

@main.route('/student/<net_id>', methods=['GET','POST'])
def student_page(net_id):
    student = get_student(net_id)
    return render_template("landing.html", netid = student[0]["name"] ,form = None, login_status = check_login_status()) # Render landing page

