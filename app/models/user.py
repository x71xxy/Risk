from datetime import datetime
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from app import db, login_manager
from itsdangerous import URLSafeTimedSerializer
from flask import current_app

from datetime import datetime
from app import db
from werkzeug.security import generate_password_hash, check_password_hash

class User(UserMixin, db.Model):
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    phone = db.Column(db.String(20), unique=True, nullable=True)
    password_hash = db.Column(db.String(512), nullable=False)
    is_verified = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
        
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
        
    @property
    def is_authenticated(self):
        """用户是否已认证"""
        return True  # 如果用户对象存在，就认为已认证
        
    @property
    def is_active(self):
        """用户是否已激活"""
        return True  # 允许未验证的用户也能登录
        
    @property
    def is_anonymous(self):
        """是否是匿名用户"""
        return False  # 这是实际的用户对象，所以不是匿名
        
    def get_id(self):
        """获取用户ID"""
        return str(self.id)

class TempUser(db.Model):
    __tablename__ = 'temp_users'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    phone = db.Column(db.String(20), nullable=True)
    password_hash = db.Column(db.String(512))
    verify_token = db.Column(db.String(512))
    expires_at = db.Column(db.DateTime, default=datetime.utcnow)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __init__(self, username, email, phone=None):
        self.username = username
        self.email = email
        self.phone = phone
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
        
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    def generate_email_token(self):
        """生成邮箱验证令牌"""
        try:
            s = URLSafeTimedSerializer(current_app.config['SECRET_KEY'])
            token = s.dumps(self.email, salt=current_app.config['VERIFY_EMAIL_SALT'])
            self.email_verify_token = token
            self.email_verify_sent_at = datetime.now()
            return token
        except Exception as e:
            print(f"生成验证令牌失败: {str(e)}")
            return None
        
    @staticmethod
    def verify_email_token(token, expiration=3600):
        """验证邮箱令牌"""
        s = URLSafeTimedSerializer(current_app.config['SECRET_KEY'])
        try:
            email = s.loads(
                token,
                salt=current_app.config['VERIFY_EMAIL_SALT'],
                max_age=expiration
            )
            return email
        except:
            return None
    
    @classmethod
    def cleanup_expired(cls):
        """清理过期的临时用户"""
        try:
            expired = cls.query.filter(cls.expires_at < datetime.now()).all()
            for user in expired:
                db.session.delete(user)
            db.session.commit()
        except Exception as e:
            current_app.logger.error(f"清理过期用户失败: {str(e)}")
            db.session.rollback()

@login_manager.user_loader
def load_user(id):
    return User.query.get(int(id)) 