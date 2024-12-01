# -*- coding: utf-8 -*-
from flask import current_app, url_for
from flask_mail import Message
from app import mail
import jwt
from datetime import datetime, timedelta

def send_verification_email(temp_user):
    """发送验证邮件"""
    try:
        verification_url = url_for(
            'main.verify_email',
            token=temp_user.verify_token,
            _external=True
        )
        
        msg = Message(
            subject='验证您的 Lovejoy 古董评估账号',
            recipients=[temp_user.email]
        )
        
        msg.body = f'''亲爱的 {temp_user.username}：
感谢您注册 Lovejoy 古董评估平台！请点击以下链接验证您的邮箱：
{verification_url}
此链接将在1小时后失效。
如果这不是您的操作，请忽略此邮件。
祝好，
Lovejoy 古董评估团队'''

        mail.send(msg)
        return True
    except Exception as e:
        current_app.logger.error(f"发送验证邮件失败: {str(e)}")
        return False

def generate_token(email):
    """生成验证令牌"""
    return jwt.encode(
        {
            'email': email,
            'exp': datetime.utcnow() + timedelta(hours=1)
        },
        current_app.config['SECRET_KEY'],
        algorithm='HS256'
    )

def send_reset_email(user):
    """发送密码重置邮件"""
    token = generate_reset_token(user.email)
    msg = Message(
        '重置您的密码',
        recipients=[user.email]
    )
    reset_url = url_for('main.reset_password', token=token, _external=True)
    msg.body = f'''要重置您的密码，请访问以下链接：{reset_url}
如果您没有请求重置密码，请忽略此邮件。'''
    mail.send(msg)

def verify_reset_token(token):
    """验证重置令牌"""
    try:
        data = jwt.decode(token, current_app.config['SECRET_KEY'], algorithms=['HS256'])
        return data['reset_password']
    except:
        return None

def generate_reset_token(email):
    """生成密码重置令牌"""
    expires = datetime.utcnow() + timedelta(minutes=30)
    return jwt.encode(
        {'reset_password': email, 'exp': expires},
        current_app.config['SECRET_KEY'],
        algorithm='HS256'
    )