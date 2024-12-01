from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SelectField, MultipleFileField
from wtforms.validators import DataRequired, Length

class EvaluationRequestForm(FlaskForm):
    title = StringField('物品名称', validators=[
        DataRequired(),
        Length(min=2, max=100)
    ])
    
    description = TextAreaField('物品描述', validators=[
        DataRequired(),
        Length(min=10, max=1000)
    ])
    
    category = SelectField('物品类别', choices=[
        ('furniture', '家具'),
        ('porcelain', '瓷器'),
        ('painting', '字画'),
        ('jade', '玉器'),
        ('other', '其他')
    ], validators=[DataRequired()])
    
    contact_preference = SelectField('联系方式偏好', choices=[
        ('email', '邮箱'),
        ('phone', '电话'),
        ('both', '都可以')
    ], validators=[DataRequired()])
    
    images = MultipleFileField('上传图片') 