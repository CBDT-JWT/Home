"""
初始化管理员系统数据库
"""
import sys
import os

# 添加项目根目录到路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import app
from database import db
from models_admin import Admin, Project

def init_admin_db():
    """初始化管理员系统数据库"""
    with app.app_context():
        # 创建表
        db.create_all()
        print("✓ 管理员系统数据库表创建成功")
        
        # 检查是否已有管理员
        admin_count = Admin.query.count()
        if admin_count == 0:
            # 创建默认管理员
            admin = Admin(username='admin')
            admin.set_password('admin123')  # 默认密码，请修改！
            db.session.add(admin)
            db.session.commit()
            print("✓ 默认管理员账户创建成功")
            print("  用户名: admin")
            print("  密码: admin123")
            print("  ⚠️  请立即修改默认密码！")
        else:
            print(f"✓ 已存在 {admin_count} 个管理员账户")
        
        # 显示表信息
        inspector = db.inspect(db.engine)
        tables = inspector.get_table_names()
        admin_tables = [t for t in tables if t in ['admin', 'project']]
        
        print(f"\n已创建的管理员系统表:")
        for table in admin_tables:
            print(f"  - {table}")

if __name__ == '__main__':
    init_admin_db()
