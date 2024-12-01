from flask_wtf import FlaskForm, RecaptchaField
from wtforms import (
    StringField, 
    PasswordField, 
    EmailField, 
    TelField,
    SubmitField,
    BooleanField
)
from wtforms.validators import (
    DataRequired, 
    Email, 
    Length, 
    EqualTo, 
    Optional
)
from wtforms.validators import ValidationError
from ..models.user import User

class RegistrationForm(FlaskForm):
    username = StringField('用户名', validators=[
        DataRequired(),
        Length(min=2, max=20)
    ])
    
    email = EmailField('邮箱', validators=[
        DataRequired(),
        Email()
    ])
    
    phone = TelField('手机号码(选填)', validators=[
        Optional(),
        Length(min=11, max=11)
    ])
    
    password = PasswordField('密码', validators=[
        DataRequired(),
        Length(min=8)
    ])
    
    confirm_password = PasswordField('确认密码', validators=[
        DataRequired(),
        EqualTo('password')
    ])
    
    recaptcha = RecaptchaField()
    
    submit = SubmitField('注册')
    
    def validate_username(self, field):
        if User.query.filter_by(username=field.data).first():
            raise ValidationError('用户名已被使用')
            
    def validate_email(self, field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError('邮箱已被注册')
            
    def validate_phone(self, field):
        if field.data:
            if not field.data.isdigit():
                raise ValidationError('请输入有效的手机号码')
            if User.query.filter_by(phone=field.data).first():
                raise ValidationError('该手机号码已被注册') 

class LoginForm(FlaskForm):
    username = StringField('用户名', validators=[DataRequired()])
    password = PasswordField('密码', validators=[DataRequired()])
    remember_me = BooleanField('记住我')
    submit = SubmitField('登录')

class ResetPasswordRequestForm(FlaskForm):
    email = EmailField('邮箱', validators=[
        DataRequired(),
        Email()
    ])
    submit = SubmitField('发送重置链接')

class ResetPasswordForm(FlaskForm):
    password = PasswordField('新密码', validators=[
        DataRequired(),
        Length(min=8, message='密码长度至少为8个字符')
    ])
    confirm_password = PasswordField('确认新密码', validators=[
        DataRequired(),
        EqualTo('password', message='两次输入的密码不一致')
    ])
    submit = SubmitField('重置密码')

class Enable2FAForm(FlaskForm):
    token = StringField('验证码', validators=[
        DataRequired(),
        Length(min=6, max=6)
    ])
    submit = SubmitField('启用双因素认证')

class Verify2FAForm(FlaskForm):
    token = StringField('验证码', validators=[
        DataRequired(),
        Length(min=6, max=6)
    ])
    submit = SubmitField('验证') 