import os
from dotenv import load_dotenv

load_dotenv()  # 加载 .env 文件中的环境变量

class Config:
    # 基础配置
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-key-please-change-in-production'
    
    # 数据库配置
    if os.environ.get('FLASK_ENV') == 'production':
        SQLALCHEMY_DATABASE_URI = os.environ.get('AWS_DATABASE_URL')
    else:
        SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///lovejoy.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # 密码策略配置
    PASSWORD_MIN_LENGTH = 8
    PASSWORD_REQUIRE_UPPER = True
    PASSWORD_REQUIRE_LOWER = True
    PASSWORD_REQUIRE_DIGITS = True
    PASSWORD_REQUIRE_SPECIAL = True
    
    # 邮件服务器配置
    MAIL_SERVER = os.environ.get('MAIL_SERVER', 'smtp.qq.com')
    MAIL_PORT = int(os.environ.get('MAIL_PORT', 587))
    MAIL_USE_TLS = True
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    MAIL_DEFAULT_SENDER = ('Lovejoy古董评估', os.environ.get('MAIL_USERNAME'))
    
    # 文件上传配置
    MAX_CONTENT_LENGTH = 5 * 1024 * 1024  # 限制单个文件大小为5MB
    UPLOAD_FOLDER = 'app/static/uploads'
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
    MAX_IMAGE_COUNT = 5  # 每次评估最多上传5张图片
    
    # 图片验证配置
    MAX_IMAGE_DIMENSION = 4096  # 最大图片尺寸
    ALLOWED_MIME_TYPES = ['image/jpeg', 'image/png', 'image/gif']
    
    # 安全配置
    SESSION_COOKIE_SECURE = os.environ.get('FLASK_ENV') == 'production'
    REMEMBER_COOKIE_SECURE = os.environ.get('FLASK_ENV') == 'production'
    SESSION_COOKIE_HTTPONLY = True
    REMEMBER_COOKIE_HTTPONLY = True
    
    # reCAPTCHA配置
    RECAPTCHA_PUBLIC_KEY = os.environ.get('RECAPTCHA_PUBLIC_KEY', '6LeZHI4qAAAAAHJG1aDnSd7D5G8hbCclDTEUMooN')
    RECAPTCHA_PRIVATE_KEY = os.environ.get('RECAPTCHA_PRIVATE_KEY', '6LeZHI4qAAAAAHBGr9x1EBhNguxHjCPYVePUzBGc')
    RECAPTCHA_OPTIONS = {'theme': 'clean'}