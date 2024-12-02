#!/bin/bash

# 更新系统包
sudo yum update -y

# 安装必要的依赖
sudo yum install -y python3-pip python3-devel mysql-devel gcc

# 创建并激活虚拟环境
python3 -m venv venv
source venv/bin/activate

# 安装依赖
pip install -r requirements.txt

# 复制生产环境配置
cp production.env .env

# 初始化数据库
flask db upgrade

# 配置 Gunicorn 服务
sudo tee /etc/systemd/system/lovejoy.service << EOF
[Unit]
Description=Lovejoy Gunicorn Daemon
After=network.target

[Service]
User=ec2-user
Group=ec2-user
WorkingDirectory=/home/ec2-user/lovejoy
Environment="PATH=/home/ec2-user/lovejoy/venv/bin"
ExecStart=/home/ec2-user/lovejoy/venv/bin/gunicorn --workers 3 --bind 0.0.0.0:8000 wsgi:app

[Install]
WantedBy=multi-user.target
EOF

# 启动服务
sudo systemctl start lovejoy
sudo systemctl enable lovejoy 