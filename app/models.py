from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

from app import db, login_manager

class Student(UserMixin, db.Model):
	"""
	Create an Student Table
	"""

	__tablename__='students'

	id = db.Column(db.Integer, primary_key=True)
	email = db.Column(db.String(60), index=True, unique=True)
	username = db.Column(db.String(60), index=True, unique=True)
	name = db.Column(db.String(60), index=True)
	password_hash = db.Column(db.String(128))
	is_admin = db.Column(db.Boolean, default=True)

	@property
	def password(self):
		# Prevent password from being accessed
		raise AttributeError('pass word is not readable attribute')

	@password.setter
	def password(self, password):
		# Set Password to a hashed password
		self.password_hash = generate_password_hash(password)

	def verify_password(self, password):
		# Check if hashed password matches actual password
		return check_password_hash(self.password_hash, password)

	def __repr__(self):
		return "<Student: {}>".format(self.username)

# Set up user_loader
@login_manager.user_loader
def load_user(user_id):
	return Student.query.get(int(user_id))

class Participation(db.Model):

	__tablename__ = 'participations'

	stu_id = db.Column(db.Integer, db.ForeignKey('students.id'), primary_key=True)
	pro_id = db.Column(db.Integer, db.ForeignKey('teams.pro_id'), primary_key=True)
	task = db.Column(db.String(1024))
	progress = db.Column(db.String(1024))

	def __repr__(self):
		return "<Participation: {}>".format(self.stu_id, self.pro_id)

class Team(db.Model):

	__tablename__ = 'teams'

	pro_id = db.Column(db.Integer, primary_key=True)
	course_no = db.Column(db.Integer)
	team_no = db.Column(db.Integer)
	title = db.Column(db.String(128), index=True)

	def __repr__(self):
		return "<Team: {}>".format(self.title)

class Milestone(db.Model):

	__tablename__ = 'milestones'

	pro_id = db.Column(db.Integer, db.ForeignKey('teams.pro_id'), primary_key=True)
	mil_no = db.Column(db.Integer, primary_key=True)
	pro_title = db.Column(db.String(60))
	ins_ssn = db.Column(db.Integer, db.ForeignKey('instructors.ssn'))
	deadline = db.Column(db.String(128))
	status = db.Column(db.String(60))
	grade = db.Column(db.String(60))

	def __repr__(self):
		return "<Milestone: {}>".format(self.mil_no)

class Appointment(db.Model):

	__tablename__ = 'appointments'

	pro_id = db.Column(db.Integer, db.ForeignKey('teams.pro_id'), primary_key=True)
	time = db.Column(db.String(60), primary_key=True)
	ins_ssn = db.Column(db.Integer, db.ForeignKey('instructors.ssn'))
	status = db.Column(db.String(60))

	def __repr__(self):
		return "<Appointment: {}>".format(self.time)

class Instructor(db.Model):

	__tablename__ = 'instructors'

	ssn = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(60))
	office = db.Column(db.String(60))
	office_hrs = db.Column(db.String(128))

	def __repr__(self):
		return "<Instructor: {}>".format(self.name)

class Department(db.Model):
	"""
	Create a Department table
	"""

	__tablename__ = 'departments'

	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(60), unique=True)
	description = db.Column(db.String(200))
	#students = db.relationship('Student', backref='department', lazy='dynamic')

	def __repr__(self):
		return "<Department: {}>".format(self.name)


class Role(db.Model):

	__tablename__ = 'roles'
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(60), unique=True)
	description = db.Column(db.String(200))
	#students = db.relationship('Student', backref='role', lazy='dynamic')

	def __repr__(self):
		return '<Role: {}>'.format(self.name)
