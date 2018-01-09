import sys
from flask import abort, flash, redirect, url_for, render_template
from flask_login import current_user, login_required

from . import admin 
from forms import DepartmentForm, AptForm, EmployeeAssignForm
from .. import db
from ..models import Department, Role, Student, Milestone, Team, Appointment


def check_admin():
	"""
	Prevent a non admin access
	"""
	if not current_user.is_admin:
		abort(403)

# Department views

@admin.route('/deparments', methods=['GET', 'POST'])
@login_required
def list_departments():
	"""
	List all departments
	"""
	check_admin()
	departments = Department.query.all()
	return render_template('admin/departments/departments.html',
							departments=departments, title = 'Departments')


@admin.route('/deparments/add', methods=['GET', 'POST'])
@login_required
def add_department():
	"""
	add deparment to the database
	"""
	check_admin()
	add_department = True
	form = DepartmentForm()
	if form.validate_on_submit():
		department = Department(name=form.name.data, description=form.description.data)
		try:
			#add department to the database
			db.session.add(department)
			db.session.commit()
			flash('You have successfully created a deparment')
		except:
			#in case department name already exists 
			flash('Error : Department name already exists')
		#redirect to departments page
		return redirect(url_for('admin.list_departments'))

	# load the department template
	return render_template('admin/departments/department.html', action ="Add", add_department=add_department, form=form, title="Add Department")

@admin.route('/departments/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_department(id):
	"""
	Edit a department
	"""
	check_admin()

	add_department = False
	department = Department.query.get_or_404(id)
	form = DepartmentForm(obj=department)
	if form.validate_on_submit():
		department.name = form.name.data
		department.description = form.description.data
		db.session.commit()
		flash('You have successfully edited the department')

		# return to the departments page
		return redirect(url_for('admin.list_departments'))

	form.description.data = department.description
	form.name.data = department.name 
	return render_template('admin/departments/department.html', action="Edit", add_department=add_department, form=form, department=department, title="Edit Department")

@admin.route('/departments/delete/<int:id>', methods=['GET', 'POST'])
@login_required
def delete_department(id):
	"""
	Delete a department from the database
	"""
	check_admin()

	department = Department.query.get_or_404(id)
	db.session.delete(department)
	db.session.commit()
	flash('You have successfully deleted the department.')

	# redirect to the departments page
	return redirect(url_for('admin.list_departments'))

	return render_template(title="Delete Department")


@admin.route('/appointments')
@login_required
def list_apts():
	check_admin()
	"""
	List all appointments
	"""
	appointments = Appointment.query.all()
	return render_template('admin/appointments/appointments.html', appointments=appointments, title='Appointments')

@admin.route('/appointments/add', methods=['GET', 'POST'])
@login_required
def add_apt():
	"""
	Add an apt to the database
	"""
	check_admin()
	add_apt = True

	form = AptForm()
	if form.validate_on_submit():
		apt = Appointment(pro_id=form.pro_id.data, time=form.time.data,
						  ins_ssn = form.ins_ssn.data, status = 'to confirm')
		try: 
			# add role to the database
			db.session.add(apt)
			db.session.commit()
			flash('You have succesfully added one appointment to be confirmed by the instructor.')
		except:
			# in case role name already exists
			flash('Error: Appointment Time Clash')

		#redirect to the list roles page
		return redirect(url_for('admin.list_apts'))

	# load the role template 
	return render_template('admin/appointments/appointment.html', add_apt=add_apt, form=form, title='Add Appointment')

@admin.route('/roles/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_role(id):
	"""
	Edit a role
	"""
	check_admin()

	add_role = False

	role = Role.query.get_or_404(id)
	form = RoleForm(obj=role)
	if form.validate_on_submit():
		role.name = form.name.data
		role.description = form.description.data
		db.session.add(role)
		db.session.commit()
		flash('You have successfully edited the role.')

		# redirect to the roles page
		return redirect(url_for('admin.list_roles'))

	form.description.data = role.description
	form.name.data = role.name
	return render_template('admin/roles/role.html', add_role=add_role,
						   form=form, title="Edit Appointment")

@admin.route('/roles/delete/<int:id>', methods=['GET', 'POST'])
@login_required
def delete_role(id):
	"""
	Delete a role from the database
	"""
	check_admin()

	role = Role.query.get_or_404(id)
	db.session.delete(role)
	db.session.commit()
	flash('You have successfully deleted the role.')

	# redirect to the roles page
	return redirect(url_for('admin.list_roles'))

	return render_template(title="Delete Appointment")

@admin.route('/milestones')
@login_required
def count_milestones():
	"""
	List all team members
	"""
	check_admin()
	all = db.engine.execute('select count(*) as no\
	 	from milestones as m\
	 	where m.pro_id in (select pro_id from participations as p where p.stu_id = 1)')

	graded = db.engine.execute('select count(*) as no\
		 	from milestones as m\
		 	where m.pro_id in (select pro_id from participations as p where p.stu_id = 1)\
		 	and m.status = \'graded\'')

	todo = db.engine.execute('select count(*) as no\
			 	from milestones as m\
			 	where m.pro_id in (select pro_id from participations as p where p.stu_id = 1)\
			 	and m.status = \'todo\'')

	return render_template('admin/milestones/milestones.html', all = all,
						   todo = todo, graded = graded, title='Milestones')

@admin.route('/all_milestones.html')
@login_required
def show_all_milestones():
	"""
	List all team members
	"""
	check_admin()
	milestones = Milestone.query.all()
	return render_template('admin/milestones/all_milestones.html', milestones=milestones, title='All Milestones')

@admin.route('/graded_milestones')
@login_required
def show_graded_milestones():
	"""
	List all team members
	"""
	check_admin()
	gradedmilestones = db.engine.execute('select * from milestones as m where m.status = \'graded\'')
	return render_template('admin/milestones/all_milestones.html', milestones=gradedmilestones, title='Graded Milestones')

@admin.route('/todo_milestones')
@login_required
def show_todo_milestones():
	"""
	List all team members
	"""
	check_admin()
	todomilestones = db.engine.execute('select * from milestones as m where m.status = \'todo\'')
	return render_template('admin/milestones/todo_milestones.html', milestones=todomilestones, title='Todo Milestones')

@admin.route('/members')
@login_required
def list_members():
	"""
	List all team members
	"""
	check_admin()
	members = db.engine.execute('select s.id as id, s.name as name, t.title as title, p.task as task,\
 		p.progress as progress, s.email as email\
 		from (participations p left join students s on p.stu_id = s.id\
 		left join teams t on p.pro_id = t.pro_id)\
		where p.pro_id in (select pro_id from participations as p where p.stu_id = 1)')
	return render_template('admin/members/members.html', members=members, title='Team Members')

@admin.route('/members/assign/<int:id>', methods=['GET','POST'])
@login_required
def edit_work(id):
	"""
	Assign employee to department
	"""
	check_admin()
	participation = Participation.query.get_or_404(id, pro_id)

	form = EmployeeAssignForm(obj=employee)
	if form.validate_on_submit():
		employee.department = form.department.data
		employee.role = form.role.data
		db.session.add(employee)
		db.session.commit()
		flash('You have successfully assigned a department and role.')

		# redirect to the roles page
		return redirect(url_for('admin.list_employees'))

	return render_template('admin/members/member.html',
						   employee=employee, form=form,
						   title='Assign Employee')