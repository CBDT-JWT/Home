"""
数据库实例
单独文件避免循环导入
"""
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
