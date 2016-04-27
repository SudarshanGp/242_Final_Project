from database import TA
from flask import render_template, request, jsonify, redirect, url_for

from VOH.main.database.authentication import *
from VOH.main.forms import ChatForm
from . import main


@main.route('/TA/<net_id>/', methods=['GET', 'POST'])
def TA_page(net_id):
    """
    Landing Page after Login for a TA
    Creates and stores a Chat form for future use
    :param net_id: net_id of TA
    :return: Rendered template of ta.html
    """
    # Check for TA login
    if "net_id" in session and session["net_id"] == net_id:
        ta = TA.get_TA(net_id)
        return render_template("ta.html", netid = ta[0]["name"], login_status = check_login_status())
    # Redirect if TA not logged in
    else:
        return redirect(url_for("main.main_page"))