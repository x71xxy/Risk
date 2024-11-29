from flask import Blueprint

main = Blueprint('main', __name__)

from . import auth, evaluation

__all__ = ['main'] 