"""
管理员和项目管理数据模型
"""
from database import db
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash


class Admin(db.Model):
    """管理员表"""
    __tablename__ = 'admin'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    
    def set_password(self, password):
        """设置密码"""
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        """验证密码"""
        return check_password_hash(self.password_hash, password)
    
    def to_dict(self):
        return {
            'id': self.id,
            'username': self.username,
            'created_at': self.created_at.isoformat()
        }


class Project(db.Model):
    """项目展示表"""
    __tablename__ = 'project'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    thumbnail = db.Column(db.String(255))  # 缩略图路径
    content_type = db.Column(db.String(20), nullable=False)  # pdf, markdown, link
    content_path = db.Column(db.String(255), nullable=False)  # 文件路径或链接URL
    order_index = db.Column(db.Integer, default=0)  # 排序
    is_visible = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'thumbnail': self.thumbnail,
            'content_type': self.content_type,
            'content_path': self.content_path,
            'order_index': self.order_index,
            'is_visible': self.is_visible,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }
