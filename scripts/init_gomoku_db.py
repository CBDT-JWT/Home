"""
初始化五子棋数据库表
"""
import sys
import os

# 添加项目根目录到路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import app
from database import db

# 导入所有模型
from models_gomoku import GomokuRoom, GomokuPlayer, GomokuMove

def init_gomoku_db():
    """初始化五子棋数据库表"""
    with app.app_context():
        # 创建表
        db.create_all()
        print("✓ 五子棋数据库表创建成功")
        
        # 显示表信息
        inspector = db.inspect(db.engine)
        tables = inspector.get_table_names()
        gomoku_tables = [t for t in tables if t.startswith('gomoku_')]
        
        print(f"\n已创建的五子棋表:")
        for table in gomoku_tables:
            print(f"  - {table}")

if __name__ == '__main__':
    init_gomoku_db()
