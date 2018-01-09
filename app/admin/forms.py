from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
from wtforms.ext.sqlalchemy.fields import QuerySelectField
from ..models import Department, Role


class DepartmentForm(FlaskForm):
	"""
	Form for admin to add or delete a department
	"""
	name = StringField('Name', validators=[DataRequired()])
	description = StringField('Description', validators=[DataRequired()])
	submit = SubmitField('Submit')

class AptForm(FlaskForm):
	"""
	Form for admin to add or edit role
	"""
	pro_id = StringField('Project ID', validators=[DataRequired()])
	time = StringField('time', validators=[DataRequired()])
	ins_ssn = StringField('Instructor SSN', validators=[DataRequired()])
	submit = SubmitField('Submit')

class EmployeeAssignForm(FlaskForm):
	"""
	Form for admin to assign role for members
	"""
	department = QuerySelectField(query_factiory=lambda: Department.query.all(), get_label="name")
	role = QuerySelectField(query_factiory=lambda: Role.query.all(), get_label="name")
	submit = SubmitField('Submit')