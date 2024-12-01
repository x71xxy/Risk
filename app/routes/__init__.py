from flask import Blueprint

main = Blueprint('main', __name__)

# 导入所有路由
from .auth import *
from .evaluation import *
from .views import *

# 确保导出 Blueprint
__all__ = ['main'] 