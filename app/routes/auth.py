from flask import render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required, current_user
from app.models.user import User
from app import db
from app.utils.password_validation import validate_password
from werkzeug.security import generate_password_hash
from app.utils.email import send_reset_email, verify_reset_token
from app import mail
from . import main

@main.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')
        
        if User.query.filter_by(username=username).first():
            flash('用户名已存在', 'error')
            return render_template('register.html')
            
        if User.query.filter_by(email=email).first():
            flash('该邮箱已被注册', 'error')
            return render_template('register.html')
            
        if password != confirm_password:
            flash('两次输入的密码不一致', 'error')
            return render_template('register.html')
            
        is_valid, error_message = validate_password(password)
        if not is_valid:
            return render_template('register.html', password_error=error_message)
            
        user = User(
            username=username,
            email=email,
            password_hash=generate_password_hash(password)
        )
        
        try:
            db.session.add(user)
            db.session.commit()
            flash('注册成功！请登录', 'success')
            return redirect(url_for('main.login'))
        except:
            db.session.rollback()
            flash('注册失败，请重试', 'error')
            
    return render_template('register.html')

@main.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        user = User.query.filter_by(username=username).first()
        
        if user and user.check_password(password):
            login_user(user)
            return redirect(url_for('main.home'))
            
        flash('用户名或密码错误')
        
    return render_template('login.html')

@main.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.home'))

@main.route('/reset_password_request', methods=['GET', 'POST'])
def reset_password_request():
    if request.method == 'POST':
        email = request.form.get('email')
        user = User.query.filter_by(email=email).first()
        
        if user:
            send_reset_email(user)
            flash('重置密码的邮件已发送，请查收', 'success')
            return redirect(url_for('main.login'))
        else:
            flash('未找到该邮箱对应的账号', 'error')
            
    return render_template('reset_request.html')

@main.route('/reset_password/<token>', methods=['GET', 'POST'])
def reset_password(token):
    email = verify_reset_token(token)
    if not email:
        flash('重置链接无效或已过期', 'error')
        return redirect(url_for('main.reset_password_request'))
        
    user = User.query.filter_by(email=email).first()
    if not user:
        flash('用户不存在', 'error')
        return redirect(url_for('main.reset_password_request'))
        
    if request.method == 'POST':
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')
        
        if password != confirm_password:
            flash('两次输入的密码不一致', 'error')
            return render_template('reset_password.html')
            
        is_valid, error_message = validate_password(password)
        if not is_valid:
            flash(error_message, 'error')
            return render_template('reset_password.html')
            
        user.set_password(password)
        db.session.commit()
        flash('密码已重置，请使用新密码登录', 'success')
        return redirect(url_for('main.login'))
        
    return render_template('reset_password.html') 