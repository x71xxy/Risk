from datetime import datetime
from app import db
from .user import User  # 导入 User 模型

class EvaluationRequest(db.Model):
    """评估请求模型"""
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    title = db.Column(db.String(100), nullable=False)  # 物品名称
    description = db.Column(db.Text, nullable=False)   # 物品描述
    category = db.Column(db.String(50), nullable=False)  # 物品类别
    condition = db.Column(db.String(50), nullable=False)  # 物品状况
    age_estimation = db.Column(db.String(50))  # 预估年代
    dimensions = db.Column(db.String(100))  # 尺寸
    image_paths = db.Column(db.JSON)  # 图片路径（可多张）
    
    # 评估状态
    STATUS_PENDING = 'pending'
    STATUS_IN_PROGRESS = 'in_progress'
    STATUS_COMPLETED = 'completed'
    STATUS_REJECTED = 'rejected'
    
    status = db.Column(
        db.String(20),
        default=STATUS_PENDING,
        nullable=False
    )
    
    # 时间戳
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # 评估结果
    estimated_value = db.Column(db.Float)  # 估价
    evaluator_notes = db.Column(db.Text)   # 评估师备注
    
    # 关系
    user = db.relationship('User', backref=db.backref('evaluation_requests', lazy=True))
    
    def __repr__(self):
        return f'<EvaluationRequest {self.title}>'
    
    def to_dict(self):
        """转换为字典格式"""
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'category': self.category,
            'condition': self.condition,
            'age_estimation': self.age_estimation,
            'dimensions': self.dimensions,
            'status': self.status,
            'created_at': self.created_at.isoformat(),
            'estimated_value': self.estimated_value,
            'images': self.image_paths
        } 