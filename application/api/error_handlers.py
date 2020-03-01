from werkzeug import exceptions
from flask import jsonify

from application import app


@app.errorhandler(exceptions.NotFound)
def not_found(e):
    return jsonify({'error': 'not found'}), e.code


@app.errorhandler(exceptions.InternalServerError)
def server_error(e):
    return jsonify({'error': 'server_error'}), e.code
