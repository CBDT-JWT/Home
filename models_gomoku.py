"""
五子棋游戏数据模型
"""
from database import db
from datetime import datetime
import random
import string
import json


def generate_room_code():
    """生成6位房间码"""
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))


class GomokuRoom(db.Model):
    """五子棋房间"""
    __tablename__ = 'gomoku_room'
    
    id = db.Column(db.Integer, primary_key=True)
    room_code = db.Column(db.String(6), unique=True, nullable=False, index=True)
    creator_name = db.Column(db.String(50), nullable=False)
    status = db.Column(db.String(20), default='waiting', nullable=False)  # waiting, playing, finished
    board_state = db.Column(db.Text, default='[]')  # JSON格式的15x15数组
    board_size = db.Column(db.Integer, default=15)
    current_turn = db.Column(db.String(10), default='black')  # black, white
    winner = db.Column(db.String(50))
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # 关系
    players = db.relationship('GomokuPlayer', backref='room', lazy=True, cascade='all, delete-orphan')
    moves = db.relationship('GomokuMove', backref='room', lazy=True, cascade='all, delete-orphan')
    
    def __init__(self, **kwargs):
        super(GomokuRoom, self).__init__(**kwargs)
        if not self.room_code:
            self.room_code = generate_room_code()
        if not self.board_state or self.board_state == '[]':
            # 初始化空棋盘
            size = self.board_size or 15
            self.board_state = json.dumps([[0] * size for _ in range(size)])
    
    def get_board(self):
        """获取棋盘数组"""
        return json.loads(self.board_state)
    
    def set_board(self, board):
        """设置棋盘数组"""
        self.board_state = json.dumps(board)
    
    def to_dict(self, include_board=True):
        """转换为字典"""
        data = {
            'room_code': self.room_code,
            'creator_name': self.creator_name,
            'status': self.status,
            'current_turn': self.current_turn,
            'winner': self.winner,
            'board_size': self.board_size,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat(),
            'player_count': len(self.players),
            'move_count': len(self.moves)
        }
        
        if include_board:
            data['board'] = self.get_board()
            data['players'] = [p.to_dict() for p in self.players]
            
        return data


class GomokuPlayer(db.Model):
    """五子棋玩家"""
    __tablename__ = 'gomoku_player'
    
    id = db.Column(db.Integer, primary_key=True)
    room_id = db.Column(db.Integer, db.ForeignKey('gomoku_room.id'), nullable=False)
    player_name = db.Column(db.String(50), nullable=False)
    player_color = db.Column(db.String(10), nullable=False)  # black, white
    is_ready = db.Column(db.Boolean, default=False)
    joined_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    last_active = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def to_dict(self):
        """转换为字典"""
        return {
            'name': self.player_name,
            'color': self.player_color,
            'is_ready': self.is_ready,
            'joined_at': self.joined_at.isoformat()
        }


class GomokuMove(db.Model):
    """五子棋走棋记录"""
    __tablename__ = 'gomoku_move'
    
    id = db.Column(db.Integer, primary_key=True)
    room_id = db.Column(db.Integer, db.ForeignKey('gomoku_room.id'), nullable=False)
    player_name = db.Column(db.String(50), nullable=False)
    player_color = db.Column(db.String(10), nullable=False)
    position_x = db.Column(db.Integer, nullable=False)
    position_y = db.Column(db.Integer, nullable=False)
    move_number = db.Column(db.Integer, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    
    def to_dict(self):
        """转换为字典"""
        return {
            'move_number': self.move_number,
            'player_name': self.player_name,
            'player_color': self.player_color,
            'x': self.position_x,
            'y': self.position_y,
            'created_at': self.created_at.isoformat()
        }
