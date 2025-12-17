"""
五子棋游戏 API 路由
"""
from flask import Blueprint, jsonify, request
from datetime import datetime

gomoku_bp = Blueprint('gomoku', __name__, url_prefix='/api/gomoku')


def get_dependencies():
    """延迟导入依赖，避免循环引用"""
    from app import db
    from models_gomoku import GomokuRoom, GomokuPlayer, GomokuMove
    from gomoku_logic import (
        check_winner, is_board_full, validate_move,
        get_next_color, color_to_value, value_to_color
    )
    return db, GomokuRoom, GomokuPlayer, GomokuMove, {
        'check_winner': check_winner,
        'is_board_full': is_board_full,
        'validate_move': validate_move,
        'get_next_color': get_next_color,
        'color_to_value': color_to_value,
        'value_to_color': value_to_color
    }


@gomoku_bp.route('/rooms', methods=['POST'])
def create_room():
    """创建房间"""
    db, GomokuRoom, GomokuPlayer, GomokuMove, logic = get_dependencies()
    
    try:
        data = request.get_json()
        creator_name = data.get('creator_name', '').strip()
        board_size = data.get('board_size', 15)
        
        if not creator_name:
            return jsonify({'error': '请输入玩家昵称'}), 400
        
        if len(creator_name) > 50:
            return jsonify({'error': '昵称过长（最多50个字符）'}), 400
        
        if board_size not in [15, 19]:
            board_size = 15
        
        # 创建房间
        room = GomokuRoom(
            creator_name=creator_name,
            board_size=board_size
        )
        db.session.add(room)
        db.session.flush()  # 获取房间ID
        
        # 创建者自动加入，成为黑方
        player = GomokuPlayer(
            room_id=room.id,
            player_name=creator_name,
            player_color='black'
        )
        db.session.add(player)
        db.session.commit()
        
        return jsonify({
            'room_code': room.room_code,
            'creator_name': room.creator_name,
            'player_color': 'black',
            'status': room.status,
            'board_size': room.board_size,
            'created_at': room.created_at.isoformat()
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


@gomoku_bp.route('/rooms/<room_code>/join', methods=['POST'])
def join_room(room_code):
    """加入房间"""
    try:
        db = get_db()
        GomokuRoom, GomokuPlayer, GomokuMove = get_models()
        
        data = request.get_json()
        player_name = data.get('player_name', '').strip()
        
        if not player_name:
            return jsonify({'error': '请输入玩家昵称'}), 400
        
        if len(player_name) > 50:
            return jsonify({'error': '昵称过长（最多50个字符）'}), 400
        
        # 查找房间
        room = GomokuRoom.query.filter_by(room_code=room_code.upper()).first()
        if not room:
            return jsonify({'error': '房间不存在'}), 404
        
        # 检查房间状态
        if room.status != 'waiting':
            return jsonify({'error': '房间已开始游戏或已结束'}), 400
        
        # 检查房间人数
        player_count = GomokuPlayer.query.filter_by(room_id=room.id).count()
        if player_count >= 2:
            return jsonify({'error': '房间已满'}), 400
        
        # 检查昵称是否重复
        existing = GomokuPlayer.query.filter_by(
            room_id=room.id,
            player_name=player_name
        ).first()
        if existing:
            return jsonify({'error': '该昵称已被使用'}), 400
        
        # 加入房间，成为白方
        player = GomokuPlayer(
            room_id=room.id,
            player_name=player_name,
            player_color='white'
        )
        db.session.add(player)
        db.session.commit()
        
        return jsonify({
            'room_code': room.room_code,
            'player_name': player_name,
            'player_color': 'white',
            'message': '成功加入房间'
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


@gomoku_bp.route('/rooms/<room_code>', methods=['GET'])
def get_room(room_code):
    """获取房间信息"""
    try:
        room = GomokuRoom.query.filter_by(room_code=room_code.upper()).first()
        if not room:
            return jsonify({'error': '房间不存在'}), 404
        
        # 获取最后一步棋
        last_move = GomokuMove.query.filter_by(room_id=room.id)\
            .order_by(GomokuMove.move_number.desc()).first()
        
        response = room.to_dict(include_board=True)
        
        if last_move:
            response['last_move'] = {
                'x': last_move.position_x,
                'y': last_move.position_y,
                'color': last_move.player_color
            }
        else:
            response['last_move'] = None
        
        return jsonify(response), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@gomoku_bp.route('/rooms/<room_code>/ready', methods=['POST'])
def ready_player(room_code):
    """玩家准备/取消准备"""
    try:
        data = request.get_json()
        player_name = data.get('player_name', '').strip()
        is_ready = data.get('is_ready', True)
        
        if not player_name:
            return jsonify({'error': '请提供玩家昵称'}), 400
        
        room = GomokuRoom.query.filter_by(room_code=room_code.upper()).first()
        if not room:
            return jsonify({'error': '房间不存在'}), 404
        
        player = GomokuPlayer.query.filter_by(
            room_id=room.id,
            player_name=player_name
        ).first()
        
        if not player:
            return jsonify({'error': '玩家不在房间中'}), 404
        
        # 更新准备状态
        player.is_ready = is_ready
        player.last_active = datetime.utcnow()
        
        # 检查是否两个玩家都准备好了
        players = GomokuPlayer.query.filter_by(room_id=room.id).all()
        game_started = False
        
        if len(players) == 2 and all(p.is_ready for p in players):
            room.status = 'playing'
            game_started = True
        
        db.session.commit()
        
        return jsonify({
            'message': '准备状态已更新',
            'is_ready': is_ready,
            'game_started': game_started
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


@gomoku_bp.route('/rooms/<room_code>/move', methods=['POST'])
def make_move(room_code):
    """落子"""
    try:
        data = request.get_json()
        player_name = data.get('player_name', '').strip()
        x = data.get('x')
        y = data.get('y')
        
        if not player_name:
            return jsonify({'error': '请提供玩家昵称'}), 400
        
        if x is None or y is None:
            return jsonify({'error': '请提供落子坐标'}), 400
        
        try:
            x = int(x)
            y = int(y)
        except (ValueError, TypeError):
            return jsonify({'error': '坐标格式错误'}), 400
        
        # 查找房间
        room = GomokuRoom.query.filter_by(room_code=room_code.upper()).first()
        if not room:
            return jsonify({'error': '房间不存在'}), 404
        
        # 检查游戏状态
        if room.status != 'playing':
            return jsonify({'error': '游戏未开始'}), 400
        
        # 查找玩家
        player = GomokuPlayer.query.filter_by(
            room_id=room.id,
            player_name=player_name
        ).first()
        
        if not player:
            return jsonify({'error': '玩家不在房间中'}), 404
        
        # 检查是否轮到该玩家
        if player.player_color != room.current_turn:
            return jsonify({'error': '还没轮到你下棋'}), 400
        
        # 获取棋盘
        board = room.get_board()
        
        # 验证落子
        is_valid, error_msg = validate_move(board, x, y, room.board_size)
        if not is_valid:
            return jsonify({'error': error_msg}), 400
        
        # 落子
        color_value = color_to_value(player.player_color)
        board[x][y] = color_value
        
        # 记录走棋
        move_number = GomokuMove.query.filter_by(room_id=room.id).count() + 1
        move = GomokuMove(
            room_id=room.id,
            player_name=player_name,
            player_color=player.player_color,
            position_x=x,
            position_y=y,
            move_number=move_number
        )
        db.session.add(move)
        
        # 检查胜负
        is_win, winning_line = check_winner(board, x, y, color_value)
        game_over = False
        winner = None
        
        if is_win:
            room.status = 'finished'
            room.winner = player_name
            game_over = True
            winner = player_name
        elif is_board_full(board):
            room.status = 'finished'
            room.winner = 'draw'
            game_over = True
            winner = 'draw'
        else:
            # 切换回合
            room.current_turn = get_next_color(room.current_turn)
        
        # 更新棋盘
        room.set_board(board)
        room.updated_at = datetime.utcnow()
        player.last_active = datetime.utcnow()
        
        db.session.commit()
        
        response = {
            'success': True,
            'move_number': move_number,
            'board_state': board,
            'current_turn': room.current_turn,
            'game_over': game_over,
            'winner': winner
        }
        
        if is_win:
            response['winning_line'] = [[pos[0], pos[1]] for pos in winning_line]
        
        return jsonify(response), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


@gomoku_bp.route('/rooms/<room_code>/surrender', methods=['POST'])
def surrender(room_code):
    """认输"""
    try:
        data = request.get_json()
        player_name = data.get('player_name', '').strip()
        
        if not player_name:
            return jsonify({'error': '请提供玩家昵称'}), 400
        
        room = GomokuRoom.query.filter_by(room_code=room_code.upper()).first()
        if not room:
            return jsonify({'error': '房间不存在'}), 404
        
        if room.status != 'playing':
            return jsonify({'error': '游戏未开始'}), 400
        
        player = GomokuPlayer.query.filter_by(
            room_id=room.id,
            player_name=player_name
        ).first()
        
        if not player:
            return jsonify({'error': '玩家不在房间中'}), 404
        
        # 找到对手
        opponent = GomokuPlayer.query.filter_by(room_id=room.id)\
            .filter(GomokuPlayer.player_name != player_name).first()
        
        # 结束游戏
        room.status = 'finished'
        room.winner = opponent.player_name if opponent else 'unknown'
        room.updated_at = datetime.utcnow()
        
        db.session.commit()
        
        return jsonify({
            'message': '游戏结束',
            'winner': room.winner
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


@gomoku_bp.route('/rooms/<room_code>/moves', methods=['GET'])
def get_moves(room_code):
    """获取走棋记录"""
    try:
        room = GomokuRoom.query.filter_by(room_code=room_code.upper()).first()
        if not room:
            return jsonify({'error': '房间不存在'}), 404
        
        moves = GomokuMove.query.filter_by(room_id=room.id)\
            .order_by(GomokuMove.move_number).all()
        
        return jsonify({
            'moves': [m.to_dict() for m in moves]
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@gomoku_bp.route('/rooms', methods=['GET'])
def list_rooms():
    """获取房间列表"""
    try:
        status = request.args.get('status')
        
        query = GomokuRoom.query
        if status:
            query = query.filter_by(status=status)
        
        rooms = query.order_by(GomokuRoom.created_at.desc()).limit(20).all()
        
        return jsonify({
            'rooms': [room.to_dict(include_board=False) for room in rooms]
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500
