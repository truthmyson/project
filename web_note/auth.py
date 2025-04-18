from flask import Blueprint, render_template, url_for, request, flash, redirect
from werkzeug.security import generate_password_hash, check_password_hash
from modules import user_info, note_info
from __init__ import db
from flask_login import login_required, login_user, current_user

auth = Blueprint('auth', __name__)


@auth.route('/signup', methods=['POST','GET'])
def signup_page():
    if request.method == 'POST':
        email = request.form.get('email')
        username = request.form.get('username')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')

        check_email = user_info.query.filter_by(EMAIL=email).first()
        if len(email) < 5:
            flash('email must mave 5 or more characters', category='error')
        elif check_email:
            flash('email already exist', category='error')
            return redirect(url_for('views.home_page'))
        elif len(username) < 2:
            flash('username must have 2 or more characters.',  category='error')
        elif password1 != password2:
            flash('passwords do not match', category='error')
        elif len(password2) < 6:
            flash('password must be 6 or more', category='error')
        else:
            new_user = user_info(EMAIL=email,USERNAME=username,PASSWORD=password2)
            db.session.add(new_user)
            db.session.commit()
            flash('account created', category='success')
            login_user(new_user)
            return redirect(url_for('views.home_page'))

    return render_template("signUp_page.html")

@auth.route('/login', methods=['POST','GET'])
def login_page():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        user_check = user_info.query.filter_by(EMAIL=email).first()
        check_passsword = user_info.query.filter_by(PASSWORD=password).first()
        if user_check:  
            if check_passsword:
                flash('logged in successfull', category='success')
                login_user(user_check, remember=True)
                return redirect(url_for('views.home_page'))
            else:
                flash(f'incorrect password', category='error')
        else:
            flash('account does not exist', category='error')
    return render_template("login_page.html")