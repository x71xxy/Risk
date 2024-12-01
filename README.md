# Lovejoy古董评估平台

## 项目简介
基于 Flask 的古董评估系统，实现了完整的用户认证系统和安全防护机制。

## 项目状态 (Coursework G6077)

### Task 1 - 用户注册 (已完成 ✓)
- [x] 基础注册功能 (register.html, temp_user.py)
- [x] 验证码集成 (使用 Google reCAPTCHA)
- [x] 密码策略实现 (config.py中的密码策略配置)
- [x] 密码加密存储 (使用Werkzeug提供的哈希功能)
- [x] 电话号码字段添加

### Task 2 - 安全登录 (已完成 ✓)
- [x] 登录功能实现 (使用Flask-Login)
- [x] 会话安全配置 (secure cookies, httponly)
- [x] 密码重置功能 (reset_request.html)
- [x] 会话管理 (Flask-Login session管理)
- [x] 登录失败次数限制

### Task 3 - 密码策略和恢复 (已完成 ✓)
- [x] 密码复杂度要求 (config.py中的配置)
- [x] 密码重置流程 (reset_request.html)
- [x] 邮箱验证系统 (verify_email.html)

### Task 4 - 评估请求页面 (已完成 ✓)
- [x] 评估表单设计 (request_evaluation.html)
- [x] 图片上传功能 (evaluation.py)
- [x] 安全文件处理 (文件验证、大小限制)
- [x] 联系方式偏好选择

### Task 5 - 评估列表页面 (已完成 ✓)
- [x] 评估记录展示 (my_evaluations.html)
- [x] 评估详情页面 (evaluation_detail.html)
- [x] 状态管理 (评估状态显示和管理)
- [x] 访问控制 (用户权限验证)

### Task 6 - AWS VPC (未开始 📅)
- [ ] VPC 配置
- [ ] 安全组设置
- [ ] 子网规划

## 安全特性实现

### 密码策略 ✓
- [x] 密码复杂度要求
  - 最小长度：8位
  - 必须包含大小写字母
  - 必须包含数字和特殊字符
- [x] 密码加密存储 (Werkzeug)
- [x] 密码重置功能

### 漏洞防护 ✓
- [x] SQL注入防护 (SQLAlchemy ORM)
- [x] XSS防护 (模板转义)
- [x] CSRF防护 (Flask-WTF)
- [x] 文件上传漏洞防护
  - 类型验证
  - 大小限制
  - 安全存储
- [x] 会话安全
  + - Cookie 安全配置
  + - HttpOnly
  + - Secure in production

### 身份验证 ✓
- [x] 用户注册和登录
- [x] 邮箱验证
- [x] 会话管理
- [ ] 双因素认证 (预留)

### 攻击防护 ✓
- [x] 暴力破解限制
- [x] reCAPTCHA集成
- [x] 密码哈希加盐

## 技术栈
- Flask 3.0.0
- MySQL + SQLAlchemy
- Flask-Login (会话管理)
- Flask-WTF (表单处理)
- Flask-Mail (邮件发送)
- Werkzeug (密码哈希)

## 待办事项
- [ ] 完成 VPC 配置
- [ ] 准备视频演示
- [ ] 完成自我评估

## 作者
[您的姓名]
[您的学号]
[课程信息]
