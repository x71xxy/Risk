from flask import render_template, redirect, url_for, flash, request, jsonify, current_app, abort
from flask_login import login_required, current_user
from werkzeug.utils import secure_filename
import os
from datetime import datetime
from app import db
from app.models.evaluation import EvaluationRequest
from app.forms.evaluation import EvaluationRequestForm
from . import main
import imghdr
from PIL import Image

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
MAX_FILE_SIZE = 5 * 1024 * 1024  # 5MB

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def validate_image(stream):
    """验证文件是否为合法图片"""
    try:
        # 使用PIL验证图片
        image = Image.open(stream)
        image.verify()
        stream.seek(0)  # 重置文件指针
        
        # 检查文件格式
        image_format = imghdr.what(stream)
        if image_format not in ['jpeg', 'png', 'gif']:
            return False
            
        # 检查图片尺寸
        image = Image.open(stream)
        if image.size[0] > 4096 or image.size[1] > 4096:  # 限制最大尺寸为4096x4096
            return False
            
        # 检查文件大小
        stream.seek(0, 2)  # 移动到文件末尾
        size = stream.tell()  # 获取文件大小
        stream.seek(0)  # 重置文件指针
        if size > current_app.config['MAX_CONTENT_LENGTH']:
            return False
            
        return True
    except Exception as e:
        current_app.logger.error(f"图片验证失败: {str(e)}")
        return False

@main.route('/request_evaluation', methods=['GET', 'POST'])
@login_required
def request_evaluation():
    form = EvaluationRequestForm()
    
    if form.validate_on_submit():
        try:
            # 检查文件数量
            if len(request.files.getlist('images')) > current_app.config['MAX_IMAGE_COUNT']:
                flash('最多只能上传5张图片', 'error')
                return render_template('request_evaluation.html', form=form)
                
            # 处理图片上传
            image_paths = []
            for image in request.files.getlist('images'):
                if image and allowed_file(image.filename):
                    if not validate_image(image):
                        flash('无效的图片文件', 'error')
                        return render_template('request_evaluation.html', form=form)
                        
                    filename = secure_filename(image.filename)
                    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
                    unique_filename = f"{timestamp}_{filename}"
                    image.save(os.path.join(current_app.config['UPLOAD_FOLDER'], unique_filename))
                    image_paths.append(unique_filename)
            
            # 创建评估请求
            evaluation = EvaluationRequest(
                user_id=current_user.id,
                title=form.title.data,
                description=form.description.data,
                category=form.category.data,
                contact_preference=form.contact_preference.data,
                images=image_paths
            )
            
            db.session.add(evaluation)
            db.session.commit()
            
            flash('评估请求已提交成功！', 'success')
            return redirect(url_for('main.my_evaluations'))
            
        except Exception as e:
            db.session.rollback()
            flash('提交失败，请稍后重试', 'error')
            current_app.logger.error(f"评估请求提交失败: {str(e)}")
    
    return render_template('request_evaluation.html', form=form)

@main.route('/my_evaluations')
@login_required
def my_evaluations():
    evaluations = EvaluationRequest.query.filter_by(user_id=current_user.id)\
                                      .order_by(EvaluationRequest.created_at.desc())\
                                      .all()
    return render_template('my_evaluations.html', evaluations=evaluations)

@main.route('/evaluation/<int:evaluation_id>')
@login_required
def evaluation_detail(evaluation_id):
    evaluation = EvaluationRequest.query.get_or_404(evaluation_id)
    
    # 验证用户权限
    if evaluation.user_id != current_user.id and not current_user.is_admin:
        abort(403)
    
    return render_template('evaluation_detail.html', evaluation=evaluation)

@main.route('/cancel_evaluation/<int:evaluation_id>', methods=['POST'])
@login_required
def cancel_evaluation(evaluation_id):
    try:
        evaluation = EvaluationRequest.query.get_or_404(evaluation_id)
        
        # 验证用户权限
        if evaluation.user_id != current_user.id:
            return jsonify({'error': '无权操作此评估'}), 403
            
        # 验证状态
        if evaluation.status != 'pending':
            return jsonify({'error': '只能取消待处理的评估'}), 400
            
        # 更新状态
        evaluation.status = 'cancelled'
        db.session.commit()
        
        return jsonify({'message': '评估已取消'}), 200
        
    except Exception as e:
        db.session.rollback()
        current_app.logger.error(f"取消评估失败: {str(e)}")
        return jsonify({'error': '操作失败，请重试'}), 500 