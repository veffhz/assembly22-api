## REST api with Flask

##### features:
 - rest api for locations, enrollments
 - rest api for participants, events
 - jwt token authentication
 - admin panel for manage service data
 
##### requirements:
 - Python 3.5+
 - Flask 1.1.1
 - Gunicorn 20.0.4

##### install requirements:
`pip3 install -r requirements.txt`

##### create and fill db 
`flask db upgrade`
`python fill_db.py`

##### run app:
 - run `gunicorn 'wsgi:app'`
 - register on http://localhost:8000/register/
 - get token on http://localhost:8000/auth/
