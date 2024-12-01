from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_mail import Mail
from flask_migrate import Migrate
from flask_wtf.csrf import CSRFProtect
from config import Config
import os

# 创建扩展实例
db = SQLAlchemy()
migrate = Migrate()
login_manager = LoginManager()
login_manager.login_view = 'main.login'
mail = Mail()
csrf = CSRFProtect()

def create_app(config_name=None):
    app = Flask(__name__)
    
    if config_name == 'testing':
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    else:
        app.config.from_object(Config)
    
    # 创建上传目录
    upload_dir = os.path.join(app.static_folder, 'uploads')
    if not os.path.exists(upload_dir):
        os.makedirs(upload_dir)
    # 确保静态文件目录存在
    static_folder = os.path.join(app.root_path, 'static')
    if not os.path.exists(static_folder):
        os.makedirs(static_folder)
        
    # 确保上传目录存在
    upload_dir = os.path.join(static_folder, 'uploads')
    if not os.path.exists(upload_dir):
        os.makedirs(upload_dir)
    print("\n=== 开始创建应用 ===")
    
    # 初始化扩展
    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)
    mail.init_app(app)
    csrf.init_app(app)
    
    print("扩展初始化完成")
    
    # 确保模型被导入
    from app.models import user, evaluation
    print("模型导入完成")
    
    # 注册蓝图
    try:
        from app.routes import main as main_blueprint
        app.register_blueprint(main_blueprint)
        print("蓝图注册完成")
        
        # 打印应用的所有路由
        print("\n=== 应用路由映射 ===")
        for rule in app.url_map.iter_rules():
            print(f"路由: {rule.rule} [{', '.join(rule.methods)}] -> {rule.endpoint}")
            
    except Exception as e:
        print(f"蓝图注册失败: {str(e)}")
        import traceback
        traceback.print_exc()
    
    print("\n=== 应用创建完成 ===")
    return app

# 导出扩展实例
__all__ = ['db', 'login_manager', 'mail', 'migrate'] 