import logging

from werkzeug import exceptions
from flask import jsonify, Blueprint

err_bp = Blueprint('errors', __name__)
logger = logging.getLogger(__name__)


@err_bp.app_errorhandler(exceptions.NotFound)
def not_found(e):
    logger.info(e)
    return jsonify({'error': 'not found'}), e.code


@err_bp.app_errorhandler(exceptions.InternalServerError)
def server_error(e):
    logger.error(e, exc_info=True)
    return jsonify({'error': 'server_error'}), e.code


@err_bp.app_errorhandler(exceptions.UnprocessableEntity)
def validation_error(e):
    logger.warning(e, exc_info=True)
    return jsonify({'error': f'validation error: {e.data.get("messages")}'}), e.code


@err_bp.app_errorhandler(exceptions.HTTPException)
def error_all(e):
    logger.warning(e, exc_info=True)
    return jsonify({'error': f'http error: {repr(e)}'}), e.code
