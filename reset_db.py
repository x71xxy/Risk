import os
from app import create_app, db
from sqlalchemy import text

def reset_database():
    print("\n=== 开始重置数据库 ===")
    
    app = create_app()
    with app.app_context():
        try:
            # 禁用外键检查
            db.session.execute(text('SET FOREIGN_KEY_CHECKS=0'))
            
            # 删除现有表
            print("删除现有表...")
            db.session.execute(text('DROP TABLE IF EXISTS evaluation_requests'))
            db.session.execute(text('DROP TABLE IF EXISTS evaluation_request'))
            db.session.execute(text('DROP TABLE IF EXISTS temp_users'))
            db.session.execute(text('DROP TABLE IF EXISTS users'))
            db.session.commit()
            
            # 创建新表
            print("创建新表...")
            db.create_all()
            
            # 启用外键检查
            db.session.execute(text('SET FOREIGN_KEY_CHECKS=1'))
            db.session.commit()
            
            print("数据库重置成功！")
            
        except Exception as e:
            print(f"错误：数据库重置失败 - {str(e)}")
            db.session.rollback()
            raise
        finally:
            print("=== 重置完成 ===")

if __name__ == '__main__':
    reset_database() 