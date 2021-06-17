import functools

from flask import (
	Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from werkzeug.security import check_password_hash, generate_password_hash
from mycontact.model.db_model import (User, db)

#from mycontact.db import get_db

#Blueprint named auth
bp = Blueprint('auth',__name__,url_prefix='/auth')

@bp.route('/register', methods=('GET','POST'))
def register():
	if request.method == 'POST':
		uname = request.form['username']
		password = request.form['password']
		error_msg = None

		user = User.query.filter_by(username=uname).one_or_none()
		if not uname:
			error_msg = 'Username is required'
		elif not password:
			error_msg = 'Password is required'
		elif user is not None:
			error_msg = 'Username {} is already exist'.format(uname)

		if error_msg is None:
			new_user = User(username=uname, password = generate_password_hash(password))
			db.session.add(new_user)
			db.session.commit()
			flash('Register is success')
			return redirect(url_for('auth.login'))
		flash(error_msg)
	return render_template('authentication/register.html')

@bp.route('/login', methods=('GET','POST'))
def login():
	if request.method == 'POST':
		uname = request.form['username']
		password = request.form['password']
		error_msg = None
		user = User.query.filter_by(username=uname).one_or_none()

		if user is None:
			error_msg = 'Username {} is not exist'.format(uname)
		elif not check_password_hash(user.password, password):
			error_msg = 'Incorrect Password'

		if error_msg is None:
			session.clear()
			session['user_id'] = user.id
			# return render_template('dashboard/main-dashboard.html')
			return redirect(url_for('manage_contact.dashboard', user_id = user.id))
		flash(error_msg)
	return render_template('authentication/login.html')

@bp.before_app_request
def load_logged_in_user():
	user_id = session.get('user_id')
	print('here here')
	if user_id is None:
		g.user = None
	else:
		user = User.query.filter_by(id=user_id).first()
		g.user = user

@bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('auth.login'))

def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('auth.login'))
        return view(**kwargs)

    return wrapped_view
