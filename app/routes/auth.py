from flask import render_template, redirect, url_for, flash, request, session
from flask_login import login_user, logout_user, login_required, current_user
from app.models.user import User, TempUser
from app import db
from app.utils.password_validation import validate_password
from werkzeug.security import generate_password_hash
from app.utils.email import (
    send_reset_email, 
    verify_reset_token, 
    send_verification_email,
    generate_token
)
from app import mail
from app.forms import (
    RegistrationForm,
    LoginForm,
    ResetPasswordRequestForm,
    ResetPasswordForm
)
from . import main
from datetime import datetime, timedelta
from flask import current_app

@main.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
        
    form = RegistrationForm()
    
    if request.method == 'POST':
        print("POST请求数据:", request.form)
        
    if form.validate_on_submit():
        print("表单验证成功")
        try:
            # 检查用户名是否已存在于正式用户表
            existing_user = User.query.filter_by(username=form.username.data).first()
            if existing_user:
                flash('用户名已被使用', 'error')
                return render_template('register.html', form=form)
            
            # 检查用户名是否已存在于临时用户表
            existing_temp_user = TempUser.query.filter_by(username=form.username.data).first()
            if existing_temp_user:
                # 如果临时用户已过期，则删除它
                if datetime.now() > existing_temp_user.expires_at:
                    db.session.delete(existing_temp_user)
                    db.session.commit()
                else:
                    flash('用户名已被使用，请等待验证邮件或选择其他用户名', 'error')
                    return render_template('register.html', form=form)
                
            # 检查邮箱是否已存在于正式用户表
            existing_email = User.query.filter_by(email=form.email.data).first()
            if existing_email:
                flash('该邮箱已被注册', 'error')
                return render_template('register.html', form=form)
                
            # 检查邮箱是否已存在于临时用户表
            existing_temp_email = TempUser.query.filter_by(email=form.email.data).first()
            if existing_temp_email:
                # 如果临时用户已过期，则删除它
                if datetime.now() > existing_temp_email.expires_at:
                    db.session.delete(existing_temp_email)
                    db.session.commit()
                else:
                    flash('该邮箱已被注册，请等待验证邮件或使用其他邮箱', 'error')
                    return render_template('register.html', form=form)
            
            # 验证密码复杂度
            is_valid, error_message = validate_password(form.password.data)
            if not is_valid:
                flash(error_message, 'error')
                return render_template('register.html', form=form)
                
            # 验证两次密码是否一致
            if form.password.data != form.confirm_password.data:
                flash('两次输入的密码不一致', 'error')
                return render_template('register.html', form=form)
            
            # 创建临时用户
            temp_user = TempUser(
                username=form.username.data,
                email=form.email.data,
                phone=form.phone.data if form.phone.data else None
            )
            temp_user.password_hash = generate_password_hash(form.password.data)
            
            # 生成验证令牌
            token = generate_token(form.email.data)
            temp_user.verify_token = token
            temp_user.expires_at = datetime.now() + timedelta(hours=1)
            
            # 保存临时用户
            db.session.add(temp_user)
            db.session.commit()
            
            # 发送验证邮件
            if send_verification_email(temp_user):
                flash('请查收验证邮件完成注册。', 'success')
            else:
                flash('验证邮件发送失败，请重试。', 'error')
                return render_template('register.html', form=form)
            
            return redirect(url_for('main.register_pending'))
            
        except Exception as e:
            db.session.rollback()
            current_app.logger.error(f"注册失败: {str(e)}")
            flash('注册失败，请重试。如果问题持续存在，请联系客服。', 'error')
            
    else:
        # 打印具体的验证错误信息
        print("表单验证失败")
        for field, errors in form.errors.items():
            print(f"字段 {field} 的错误: {errors}")
            for error in errors:
                flash(f"{form[field].label.text}: {error}", 'error')
                
    return render_template('register.html', form=form)

@main.route('/register/pending')
def register_pending():
    return render_template('register_pending.html')

@main.route('/verify-email/<token>')
def verify_email(token):
    try:
        temp_user = TempUser.query.filter_by(verify_token=token).first()
        
        if not temp_user:
            flash('验证链接无效或已过期', 'error')
            return redirect(url_for('main.register'))
            
        if datetime.now() > temp_user.expires_at:
            db.session.delete(temp_user)
            db.session.commit()
            flash('验证链接已过期，请重新注册', 'error')
            return redirect(url_for('main.register'))
            
        # 创建正式用户
        user = User(
            username=temp_user.username,
            email=temp_user.email,
            phone=temp_user.phone if hasattr(temp_user, 'phone') else None,
            password_hash=temp_user.password_hash,
            is_verified=True
        )
        
        try:
            db.session.add(user)
            db.session.delete(temp_user)
            db.session.commit()
            flash('邮箱验证成功！请登录', 'success')
            return redirect(url_for('main.login'))
            
        except Exception as e:
            db.session.rollback()
            current_app.logger.error(f"验证失败: {str(e)}")
            flash('验证失败，请重试', 'error')
            return redirect(url_for('main.register'))
            
    except Exception as e:
        current_app.logger.error(f"验证过程出错: {str(e)}")
        flash('验证过程出错，请重试', 'error')
        return redirect(url_for('main.register'))

@main.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
        
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        
        if user and user.check_password(form.password.data):
            if not user.is_verified:  # 注意这里改为 is_verified
                flash('请先验证您的邮箱', 'error')
                return render_template('login.html', form=form)
                
            login_user(user)
            next_page = request.args.get('next')
            if next_page:
                return redirect(next_page)
            return redirect(url_for('main.home'))
            
        flash('用户名或密码错误', 'error')
        
    return render_template('login.html', form=form)

@main.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.home'))

@main.route('/reset_password_request', methods=['GET', 'POST'])
def reset_password_request():
    form = ResetPasswordRequestForm()
    if form.validate_on_submit():
        email = request.form.get('email')
        user = User.query.filter_by(email=email).first()
        
        if user:
            send_reset_email(user)
            flash('重置密码的邮件已发送，请查收', 'success')
            return redirect(url_for('main.login'))
        else:
            flash('未找到该邮箱对应的账号', 'error')
            
    return render_template('reset_request.html', form=form)

@main.route('/reset_password/<token>', methods=['GET', 'POST'])
def reset_password(token):
    form = ResetPasswordForm()
    email = verify_reset_token(token)
    if not email:
        flash('重置链接无效或已过期', 'error')
        return redirect(url_for('main.reset_password_request'))
        
    user = User.query.filter_by(email=email).first()
    if not user:
        flash('用户不存在', 'error')
        return redirect(url_for('main.reset_password_request'))
        
    if form.validate_on_submit():
        is_valid, error_message = validate_password(form.password.data)
        if not is_valid:
            flash(error_message, 'error')
            return render_template('reset_password.html', form=form)
            
        user.set_password(form.password.data)
        db.session.commit()
        flash('密码已重置，请使用新密码登录', 'success')
        return redirect(url_for('main.login'))
        
    return render_template('reset_password.html', form=form) 