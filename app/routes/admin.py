from flask import render_template, redirect, url_for, flash, request, jsonify, current_app
from flask_login import login_required, current_user
from . import main
from ..utils.decorators import admin_required
from ..models.user import User
from ..models.evaluation import EvaluationRequest
from app import db

@main.route('/admin')
@admin_required
def admin_dashboard():
    """管理员仪表盘"""
    stats = {
        'total_users': User.query.count(),
        'total_evaluations': EvaluationRequest.query.count(),
        'pending_evaluations': EvaluationRequest.query.filter_by(status='pending').count(),
        'completed_evaluations': EvaluationRequest.query.filter_by(status='completed').count()
    }
    return render_template('admin/dashboard.html', stats=stats)

@main.route('/admin/users')
@admin_required
def admin_users():
    """用户管理"""
    page = request.args.get('page', 1, type=int)
    users = User.query.paginate(page=page, per_page=20)
    return render_template('admin/users.html', users=users)

@main.route('/admin/evaluations')
@admin_required
def admin_evaluations():
    """评估管理"""
    page = request.args.get('page', 1, type=int)
    status = request.args.get('status', '')
    
    query = EvaluationRequest.query
    if status:
        query = query.filter_by(status=status)
        
    evaluations = query.order_by(EvaluationRequest.created_at.desc())\
                      .paginate(page=page, per_page=20)
    return render_template('admin/evaluations.html', evaluations=evaluations)

@main.route('/admin/evaluation/<int:id>/update', methods=['POST'])
@admin_required
def update_evaluation_status(id):
    """更新评估状态"""
    evaluation = EvaluationRequest.query.get_or_404(id)
    status = request.json.get('status')
    
    if status not in EvaluationRequest.STATUS_CHOICES:
        return jsonify({'error': '无效的状态'}), 400
        
    evaluation.status = status
    db.session.commit()
    
    return jsonify({'message': '状态已更新'}) 