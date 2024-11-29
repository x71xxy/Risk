from dotenv import load_dotenv
load_dotenv()  # 加载 .env 文件中的环境变量

from app import create_app, db

app = create_app()

if __name__ == '__main__':
    with app.app_context():
        db.drop_all()  # 删除所有表
        db.create_all()  # 重新创建表
    app.run(debug=True) 