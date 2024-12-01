from datetime import datetime
from app import db
from .user import User  # 导入 User 模型

class EvaluationRequest(db.Model):
    """评估请求模型"""
    __tablename__ = 'evaluation_requests'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    title = db.Column(db.String(100), nullable=False)  # 物品名称
    description = db.Column(db.Text, nullable=False)   # 物品描述
    category = db.Column(db.String(50), nullable=False)  # 物品类别
    contact_preference = db.Column(db.String(20), nullable=False)  # 联系方式偏好
    images = db.Column(db.JSON)  # 图片路径
    status = db.Column(
        db.String(20),
        default='pending',
        nullable=False
    )
    
    # 时间戳
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # 关系
    user = db.relationship('User', backref=db.backref('evaluation_requests', lazy=True))
    
    STATUS_CHOICES = {
        'pending': '待处理',
        'in_progress': '评估中',
        'completed': '已完成',
        'cancelled': '已取消'
    }
    
    CATEGORY_CHOICES = {
        'furniture': '家具',
        'porcelain': '瓷器',
        'painting': '字画',
        'jade': '玉器',
        'other': '其他'
    }
    
    def __init__(self, user_id, title, description, category, contact_preference, images=None):
        self.user_id = user_id
        self.title = title
        self.description = description
        self.category = category
        self.contact_preference = contact_preference
        self.images = images or []
    
    def to_dict(self):
        """转为字典格式"""
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'category': self.category,
            'contact_preference': self.contact_preference,
            'images': self.images,
            'status': self.status,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        } 
    
    def get_status_display(self):
        """获取状态的显示文本"""
        return self.STATUS_CHOICES.get(self.status, self.status)
    
    def get_category_display(self):
        """获取类别的显示文本"""
        return self.CATEGORY_CHOICES.get(self.category, self.category)