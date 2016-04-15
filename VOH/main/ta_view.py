from database import TA
from flask import render_template, request, jsonify, redirect, url_for

from VOH.main.database.authentication import *
from VOH.main.forms import ChatForm
from . import main


@main.route('/TA/<net_id>', methods=['GET', 'POST'])
def TA_page(net_id):
    """
    @author: Sudarshan
    Landing Page after Login for a particular user
    landing_page() validates the form submission and redirects to /chat/ if it is successful form POST
    :param user: NetID of user
    """
    ta = TA.get_TA(net_id)
    form = ChatForm()  # Create a form as an instance of ChatFrom class
    if form.validate_on_submit(): # On submission of From
        session['netID'] = form.netID.data # Get NetID
        session['chatID'] = form.chatID.data # Get unique chatID
        return redirect(url_for('.chat')) # Redirect to /chat/
    elif request.method == 'GET': # If its a get request
        form.netID.data = session.get('netID', '') # Retrieve netID from form
        form.chatID.data = session.get('chatID', '') # Retrieve chatID from form
    return render_template("ta.html", netid = ta[0]["name"], form = form, login_status = check_login_status()) # Render landing page