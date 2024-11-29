import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'your-secret-key'
    
    # 根据环境选择数据库URL
    if os.environ.get('FLASK_ENV') == 'production':
        # AWS RDS配置
        SQLALCHEMY_DATABASE_URI = os.environ.get('AWS_DATABASE_URL')
    else:
        # 本地开发配置
        SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
            'mysql+pymysql://username:password@localhost/lovejoy_db'
    
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # 文件上传配置
    UPLOAD_FOLDER = 'app/static/uploads'
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB max-limit
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
    
    # 邮件服务器配置
    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD') 