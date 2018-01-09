from flask import flash, redirect, render_template, url_for
from flask_login import login_required, login_user, logout_user
from . import auth
from forms import LoginForm, RegistrationForm
from .. import db
from ..models import Student

@auth.route('/register', methods=['GET','POST'])
def register():
	"""
	Handle request to the /register route
	Sdd an employee to the database through registration form 
	"""
	form = RegistrationForm()
	if form.validate_on_submit():
		student = Student(email=form.email.data,
							username=form.username.data,
							name=form.name.data,
							password=form.password.data)

		# add an employee to the database
		db.session.add(student)
		db.session.commit()
		flash('You have successfully registered! You may now log in.')

		# redirect to the login page
		return redirect(url_for('auth.login'))

	return render_template('auth/register.html', form=form, title='Register')

@auth.route('/login', methods=['GET','POST'])
def login():
	"""
	Handle requests to the /login route
	Log an employee in through the login form
	"""
	form = LoginForm()
	if form.validate_on_submit():

		# check whether the employee exists in the database and whether the password entered matches the passsword in the database
		
		student = Student.query.filter_by(email=form.email.data).first()
		if student is not None and student.verify_password(form.password.data):

			# log employee in 
			login_user(student)

			# redirect to the appropriate dashboard page
			if student.is_admin:
				return redirect(url_for('home.admin_dashboard'))
			else:
				return redirect(url_for('home.dashboard'))



		# when login details are not correct
		else:
			flash('Invalid Email or Password')

	# load login template
	return render_template('auth/login.html', form=form, title='Login')

@auth.route('/logout')
@login_required
def logout():
	"""
	Handle requests to the /logout route
	Log an employee out through the logout link
	"""
	logout_user()
	flash('You have successfully been logged out')

	# redirect to the login page
	return redirect(url_for('auth.login'))