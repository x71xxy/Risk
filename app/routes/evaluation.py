from flask import render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from werkzeug.utils import secure_filename
import os
import time
from app import db
from app.models.evaluation import EvaluationRequest
from . import main

# 配置上传文件
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
UPLOAD_FOLDER = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'static/uploads')

# 确保上传目录存在
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@main.route('/')
def home():
    return render_template('home.html')

@main.route('/request_evaluation', methods=['GET', 'POST'])
@login_required
def request_evaluation():
    if request.method == 'POST':
        # 获取表单数据
        evaluation = EvaluationRequest(
            user_id=current_user.id,
            title=request.form.get('title'),
            description=request.form.get('description'),
            category=request.form.get('category'),
            condition=request.form.get('condition'),
            age_estimation=request.form.get('age_estimation'),
            dimensions=request.form.get('dimensions')
        )
        
        # 处理图片上传
        images = []
        if 'images' in request.files:
            files = request.files.getlist('images')
            for file in files:
                if file and allowed_file(file.filename):
                    filename = secure_filename(file.filename)
                    # 使用时间戳和用户ID创建唯一文件名
                    unique_filename = f"{current_user.id}_{int(time.time())}_{filename}"
                    file_path = os.path.join(UPLOAD_FOLDER, unique_filename)
                    file.save(file_path)
                    images.append(f'/static/uploads/{unique_filename}')
        
        evaluation.image_paths = images
        
        try:
            db.session.add(evaluation)
            db.session.commit()
            flash('评估请求已提交', 'success')
            return redirect(url_for('main.my_evaluations'))
        except Exception as e:
            db.session.rollback()
            flash('提交失败，请重试', 'error')
            print(f"Error: {str(e)}")
            
    return render_template('request_evaluation.html')

@main.route('/my_evaluations')
@login_required
def my_evaluations():
    evaluations = EvaluationRequest.query.filter_by(user_id=current_user.id).all()
    return render_template('my_evaluations.html', evaluations=evaluations) 