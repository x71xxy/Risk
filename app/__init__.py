from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_mail import Mail
from config import Config

# 创建扩展实例
db = SQLAlchemy()
login_manager = LoginManager()
login_manager.login_view = 'main.login'
mail = Mail()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    
    # 初始化扩展
    db.init_app(app)
    login_manager.init_app(app)
    mail.init_app(app)
    
    # 注册蓝图
    from app.routes import main
    app.register_blueprint(main)
    
    # 确保所有模型都被导入
    from app.models import User, EvaluationRequest
    
    return app

# 导出扩展实例，这样其他模块可以直接从 app 导入
__all__ = ['db', 'login_manager', 'mail'] 