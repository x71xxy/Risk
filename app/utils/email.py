from flask_mail import Message
from flask import current_app, url_for
from app import mail
import jwt
from datetime import datetime, timedelta

def send_reset_email(user):
    """发送密码重置邮件"""
    # 生成重置令牌，有效期30分钟
    token = generate_reset_token(user.email)
    
    msg = Message(
        subject='密码重置请求',
        sender=current_app.config['MAIL_DEFAULT_SENDER'],  # 系统邮箱作为发件人
        recipients=[user.email]  # 用户邮箱作为收件人
    )
                  
    msg.body = f'''亲爱的 {user.username}：

您收到这封邮件是因为您请求重置密码。要重置您的密码，请点击以下链接：

{url_for('main.reset_password', token=token, _external=True)}

如果您没有请求重置密码，请忽略此邮件。

此链接将在30分钟后失效。

祝好,
Lovejoy古董评估团队
'''
    mail.send(msg)

def generate_reset_token(email: str) -> str:
    """生成密码重置令牌"""
    expires = datetime.utcnow() + timedelta(minutes=30)
    return jwt.encode(
        {'reset_password': email, 'exp': expires},
        current_app.config['SECRET_KEY'],
        algorithm='HS256'
    )

def verify_reset_token(token: str) -> str:
    """验证重置令牌"""
    try:
        data = jwt.decode(token, 
                         current_app.config['SECRET_KEY'],
                         algorithms=['HS256'])
        return data['reset_password']
    except:
        return None 