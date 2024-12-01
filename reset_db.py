import os
from app import create_app, db
from sqlalchemy import text

def reset_database():
    print("\n=== Starting Database Reset ===")
    
    app = create_app()
    with app.app_context():
        try:
            # Disable foreign key checks
            db.session.execute(text('SET FOREIGN_KEY_CHECKS=0'))
            
            # Drop existing tables
            print("Dropping existing tables...")
            db.session.execute(text('DROP TABLE IF EXISTS evaluation_requests'))
            db.session.execute(text('DROP TABLE IF EXISTS evaluation_request'))
            db.session.execute(text('DROP TABLE IF EXISTS temp_users'))
            db.session.execute(text('DROP TABLE IF EXISTS users'))
            db.session.commit()
            
            # Create new tables
            print("Creating new tables...")
            db.create_all()
            
            # Enable foreign key checks
            db.session.execute(text('SET FOREIGN_KEY_CHECKS=1'))
            db.session.commit()
            
            print("Database reset successful!")
            
        except Exception as e:
            print(f"Error: Database reset failed - {str(e)}")
            db.session.rollback()
            raise
        finally:
            print("=== Reset Complete ===")

if __name__ == '__main__':
    reset_database() 