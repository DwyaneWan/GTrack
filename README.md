# GTrack
GTrack is a website application that stores the details and general information of student projects going on at Georgia Tech. It uses python Flask framework and it connects to MySQL DBMS at the back end. The data stores in the database include the project milestones, grades for submissions, team members’ duties and schedules, etc.

GTrack is implemented following a [tutorial](https://scotch.io/tutorials/build-a-crud-web-app-with-python-and-flask-part-one) on Scotch.io by Mbithe Nzomo.

![image](https://github.com/DwyaneWan/GTrack/blob/master/WX20180122-115306.png?raw=true)

## Installation and Set Up
Prerequisites:
* [Python 2](https://www.python.org/download/releases/2.7.2/)
* [virtualenv](https://virtualenv.pypa.io/en/stable/)

Clone the repo from GitHub:
```
git clone https://github.com/andela-mnzomo/project-dream-team-three
```

Create a virtual environment for the project and activate it:
```
virtualenv dream-team
source dream-team/bin/activate
```

Install the required packages:
```
pip install -r requirements.txt
```

## Database configuration
You will need to create a MySQL user your terminal, as well as a MySQL database. Then, grant all privileges on your database to your user, like so:

```
$ mysql -u root

mysql> CREATE USER 'gt_admin'@'localhost' IDENTIFIED BY 'gt2017';

mysql> CREATE DATABASE gtrack_db;

mysql> GRANT ALL PRIVILEGES ON dreamteam_db . * TO 'gt_admin'@'localhost';
```

Note that `gt_admin` is the database user and `gt2017` is the user password. After creating the database, run migrations as follows:

* `flask db migrate`
* `flask db upgrade`

## instance/config.py file
Create a directory, `instance`, and in it create a `config.py` file. This file should contain configuration variables that should not be publicly shared, such as passwords and secret keys. The app requires you to have the following configuration
variables:
* SECRET_KEY
* SQLALCHEMY_DATABASE_URI (`'mysql://dt_admin:gt2017@localhost/gtrack_db'`)

## Launching the Program
Set the FLASK_APP and FLASK_CONFIG variables as follows:

* `export FLASK_APP=run.py`
* `export FLASK_CONFIG=development`

You can now run the app with the following command: `flask run`

## Testing
First, create a test database and grant all privileges on your test database to your user:

```
$ mysql -u root

mysql> CREATE DATABASE gtrack_test;

mysql> GRANT ALL PRIVILEGES ON gtrack_test . * TO 'gt_admin'@'localhost';
```

To test, run the following command: `python tests.py`

## Built With...
* [Flask](http://flask.pocoo.org/)
