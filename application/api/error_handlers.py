from werkzeug import exceptions
from flask import jsonify, make_response

from application import app


@app.errorhandler(exceptions.NotFound)
def not_found(e):
    app.logger.info(e)
    return jsonify({'error': 'not found'}), e.code


@app.errorhandler(exceptions.InternalServerError)
def server_error(e):
    app.logger.error(e, exc_info=app.debug)
    return jsonify({'error': 'server_error'}), e.code


@app.errorhandler(exceptions.HTTPException)
def error_all(e):
    app.logger.warn(e, exc_info=app.debug)
    return make_response(jsonify({'error': 'http error'}), e.code)
