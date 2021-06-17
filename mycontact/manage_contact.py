import functools

from flask import (
	Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from werkzeug.exceptions import abort
from werkzeug.security import check_password_hash, generate_password_hash
from mycontact.model.db_model import (Contacts, db)
from mycontact.auth import login_required

bp = Blueprint('manage_contact',__name__,url_prefix='/contact')


@bp.route('/<int:user_id>/all')
@login_required
def dashboard(user_id):
	if user_id != g.user.id:
		abort(403)

	contacts = Contacts.query.filter_by(user_id =user_id)
	if contacts.first() is None:
		contacts = None
	return render_template('dashboard/main-dashboard.html', contacts = contacts)

@bp.route('/add', methods=('GET','POST'))
@login_required
def add_contact():
	if request.method == 'POST':
		name = request.form['name']
		number = int(request.form['number'])
		error_msg = None

		if not name:
			error_msg = 'Name is required'
		elif not number:
			error_msg = 'Number is required'

		if error_msg is None:
			new_contact = Contacts(contact_name = name, contact_number = number, user_id = g.user.id)
			db.session.add(new_contact)
			db.session.commit()
			flash('New contact is added')
			return redirect(url_for('manage_contact.dashboard', user_id = g.user.id))
		flash(error_msg)
	return render_template('dashboard/add-contact.html')

@bp.route('/<int:contact_id>/edit', methods=('GET','POST'))
@login_required
def edit_contact(contact_id):
	contact = get_single_contact(contact_id, g.user.id)
	if  request.method == 'POST':
		contact_name = request.form['name']
		contact_number = request.form['number']
		error_msg = None
		if not contact_name:
			error_msg = 'Name is required'
		elif not contact_number:
			error_msg = 'Phone number is required'

		if error_msg is None:
			contact.contact_name = contact_name
			contact.contact_number = contact_number
			db.session.commit()
			return redirect(url_for('manage_contact.dashboard', user_id=g.user.id))

	return render_template('dashboard/edit-contact.html', contact = contact)

@bp.route('/<int:user_id>/<int:contact_id>/delete')
@login_required
def delete_contact(contact_id, user_id):
	if user_id != g.user.id:
		abort(403)
	c = get_single_contact(contact_id, user_id)

	db.session.delete(c)
	db.session.commit()
	return redirect(url_for('manage_contact.dashboard', user_id = user_id))

def get_single_contact(contact_id, user_id):
	c = Contacts.query.filter_by(id=contact_id, user_id=user_id).one_or_none()
	if c is None:
		abort(404,'Contact doesn\'t exist')
	return c
