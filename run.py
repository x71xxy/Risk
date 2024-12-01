from dotenv import load_dotenv
load_dotenv()  # 加载 .env 文件中的环境变量

from app import create_app, db
import os

app = create_app()

if __name__ == '__main__':
    with app.app_context():
        app.config['WTF_CSRF_ENABLED'] = True
        db.create_all()  # 重新创建表
    
    debug_mode = os.environ.get('FLASK_ENV') == 'development'
    app.run(debug=debug_mode, host='0.0.0.0', port=int(os.environ.get('PORT', 5000))) 