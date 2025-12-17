"""
五子棋游戏逻辑
"""


def check_winner(board, x, y, color):
    """
    检查是否有玩家获胜
    
    Args:
        board: 棋盘数组
        x, y: 最后落子位置
        color: 棋子颜色 (1=黑, 2=白)
    
    Returns:
        (is_win, winning_line): 是否获胜, 获胜的5个棋子坐标
    """
    size = len(board)
    directions = [
        (0, 1),   # 横向
        (1, 0),   # 纵向
        (1, 1),   # 右下斜
        (1, -1)   # 右上斜
    ]
    
    for dx, dy in directions:
        line = [(x, y)]
        
        # 向正方向延伸
        i = 1
        while True:
            nx, ny = x + dx * i, y + dy * i
            if 0 <= nx < size and 0 <= ny < size and board[nx][ny] == color:
                line.append((nx, ny))
                i += 1
            else:
                break
        
        # 向反方向延伸
        i = 1
        while True:
            nx, ny = x - dx * i, y - dy * i
            if 0 <= nx < size and 0 <= ny < size and board[nx][ny] == color:
                line.append((nx, ny))
                i += 1
            else:
                break
        
        # 检查是否达到5个
        if len(line) >= 5:
            # 返回连续的5个（中间的5个）
            line.sort()
            winning_line = line[:5] if len(line) == 5 else line[len(line)//2-2:len(line)//2+3]
            return True, winning_line
    
    return False, []


def is_board_full(board):
    """检查棋盘是否已满（平局）"""
    for row in board:
        if 0 in row:
            return False
    return True


def validate_move(board, x, y, size=15):
    """
    验证落子是否合法
    
    Returns:
        (is_valid, error_message)
    """
    if x < 0 or x >= size or y < 0 or y >= size:
        return False, "坐标超出范围"
    
    if board[x][y] != 0:
        return False, "该位置已有棋子"
    
    return True, None


def get_next_color(current_color):
    """获取下一个回合的颜色"""
    return 'white' if current_color == 'black' else 'black'


def color_to_value(color):
    """颜色字符串转数字"""
    return 1 if color == 'black' else 2


def value_to_color(value):
    """数字转颜色字符串"""
    if value == 1:
        return 'black'
    elif value == 2:
        return 'white'
    return None
