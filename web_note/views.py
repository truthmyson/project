from flask import Blueprint, render_template, url_for, request, flash, redirect, jsonify
from modules import user_info, note_info
from __init__ import db
from flask_login import current_user, login_required, logout_user
import json

views = Blueprint('views', __name__)


@views.route('/', methods=['POST','GET'])
@login_required
def home_page():
    if request.method == 'POST':
        note = request.form.get('note')
        if len(note) < 1:
            flash('note is too shoot', category='error')
        else:
            new_note = note_info(DATA=note, user_id=current_user.id)
            db.session.add(new_note)
            db.session.commit()
    return render_template("home_page.html", user=current_user)


@views.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login_page'))

@views.route('/delete_note', methods=['POST'])
def delete_note():
    note = json.loads(request.data) # this function expects a JSON from the INDEX.js file 
    Id = note['noteId']
    note = note_info.query.get(Id)
    if note:
        if note_info.user_id == current_user.id:
            db.session.delete(note)
            db.session.commit()

    return jsonify({})