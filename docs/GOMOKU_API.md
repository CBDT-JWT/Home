# 五子棋功能 API 设计文档

## 概述
实现一个支持多人在线对弈的五子棋系统，包括房间管理、游戏对弈、聊天等功能。

## 数据模型设计

### 1. GomokuRoom (房间表)
```python
- id: Integer (主键)
- room_code: String(6) (房间码，唯一索引)
- creator_name: String(50) (创建者昵称)
- status: String(20) (状态: waiting/playing/finished)
- board_state: Text (棋盘状态，JSON格式)
- current_turn: String(10) (当前回合: black/white)
- winner: String(50) (获胜者昵称，可空)
- created_at: DateTime (创建时间)
- updated_at: DateTime (更新时间)
```

### 2. GomokuPlayer (玩家表)
```python
- id: Integer (主键)
- room_id: Integer (外键关联 GomokuRoom)
- player_name: String(50) (玩家昵称)
- player_color: String(10) (棋子颜色: black/white)
- is_ready: Boolean (是否准备)
- joined_at: DateTime (加入时间)
- last_active: DateTime (最后活跃时间)
```

### 3. GomokuMove (走棋记录表)
```python
- id: Integer (主键)
- room_id: Integer (外键关联 GomokuRoom)
- player_name: String(50) (玩家昵称)
- player_color: String(10) (棋子颜色)
- position_x: Integer (X坐标, 0-14)
- position_y: Integer (Y坐标, 0-14)
- move_number: Integer (第几步)
- created_at: DateTime (落子时间)
```

## API 端点设计

### 1. 房间管理

#### 1.1 创建房间
```
POST /api/gomoku/rooms
Request Body:
{
  "creator_name": "玩家1",
  "board_size": 15  // 可选，默认15
}

Response (201):
{
  "room_code": "ABC123",
  "creator_name": "玩家1",
  "status": "waiting",
  "created_at": "2025-12-17T10:00:00"
}
```

#### 1.2 加入房间
```
POST /api/gomoku/rooms/{room_code}/join
Request Body:
{
  "player_name": "玩家2"
}

Response (200):
{
  "room_code": "ABC123",
  "player_name": "玩家2",
  "player_color": "white",
  "message": "成功加入房间"
}

Error (400):
{
  "error": "房间已满"
}
```

#### 1.3 获取房间信息
```
GET /api/gomoku/rooms/{room_code}

Response (200):
{
  "room_code": "ABC123",
  "status": "playing",
  "creator_name": "玩家1",
  "players": [
    {
      "player_name": "玩家1",
      "player_color": "black",
      "is_ready": true
    },
    {
      "player_name": "玩家2",
      "player_color": "white",
      "is_ready": true
    }
  ],
  "board_state": [[0,0,0,...], ...],  // 15x15 二维数组
  "current_turn": "black",
  "move_count": 5,
  "last_move": {
    "x": 7,
    "y": 7,
    "color": "white"
  }
}
```

#### 1.4 获取房间列表（可选）
```
GET /api/gomoku/rooms?status=waiting

Response (200):
{
  "rooms": [
    {
      "room_code": "ABC123",
      "creator_name": "玩家1",
      "status": "waiting",
      "player_count": 1,
      "created_at": "2025-12-17T10:00:00"
    }
  ]
}
```

### 2. 游戏操作

#### 2.1 准备/取消准备
```
POST /api/gomoku/rooms/{room_code}/ready
Request Body:
{
  "player_name": "玩家1",
  "is_ready": true
}

Response (200):
{
  "message": "准备状态已更新",
  "is_ready": true,
  "game_started": false  // 双方都准备时为 true
}
```

#### 2.2 落子
```
POST /api/gomoku/rooms/{room_code}/move
Request Body:
{
  "player_name": "玩家1",
  "x": 7,
  "y": 7
}

Response (200):
{
  "success": true,
  "move_number": 6,
  "board_state": [[0,0,0,...], ...],
  "current_turn": "white",
  "game_over": false,
  "winner": null
}

Response (game over):
{
  "success": true,
  "move_number": 15,
  "board_state": [[0,0,0,...], ...],
  "game_over": true,
  "winner": "玩家1",
  "winning_line": [[7,7], [7,8], [7,9], [7,10], [7,11]]
}

Error (400):
{
  "error": "不是你的回合"
}
```

#### 2.3 悔棋请求（可选）
```
POST /api/gomoku/rooms/{room_code}/undo
Request Body:
{
  "player_name": "玩家1"
}

Response (200):
{
  "message": "悔棋请求已发送",
  "waiting_approval": true
}
```

#### 2.4 认输
```
POST /api/gomoku/rooms/{room_code}/surrender
Request Body:
{
  "player_name": "玩家1"
}

Response (200):
{
  "message": "游戏结束",
  "winner": "玩家2"
}
```

### 3. 获取游戏历史

#### 3.1 获取走棋记录
```
GET /api/gomoku/rooms/{room_code}/moves

Response (200):
{
  "moves": [
    {
      "move_number": 1,
      "player_name": "玩家1",
      "player_color": "black",
      "x": 7,
      "y": 7,
      "created_at": "2025-12-17T10:05:00"
    },
    ...
  ]
}
```

### 4. 轮询/实时更新

#### 4.1 轮询房间状态（用于简单实现）
```
GET /api/gomoku/rooms/{room_code}/state?after_move={last_move_number}

Response (200):
{
  "has_update": true,
  "current_move": 6,
  "board_state": [[0,0,0,...], ...],
  "current_turn": "white",
  "last_move": {
    "x": 8,
    "y": 7,
    "color": "black"
  },
  "game_over": false
}
```

## 游戏逻辑规则

### 棋盘表示
- 使用 15x15 二维数组
- 0: 空位
- 1: 黑棋
- 2: 白棋

### 胜利条件
- 横向、纵向、斜向任意方向连续5个相同颜色的棋子

### 游戏流程
1. 玩家1创建房间，自动成为黑方
2. 玩家2加入房间，自动成为白方
3. 双方点击准备
4. 黑方先手开始下棋
5. 轮流落子直到产生胜者或平局
6. 可以重新开始或离开房间

## 实现阶段

### Phase 1: 基础功能
- [x] API 设计
- [ ] 数据模型实现
- [ ] 创建/加入房间
- [ ] 基础落子逻辑
- [ ] 胜负判定

### Phase 2: 前端界面
- [ ] 房间创建/加入页面
- [ ] 棋盘渲染
- [ ] 交互逻辑
- [ ] 状态轮询

### Phase 3: 增强功能
- [ ] 悔棋功能
- [ ] 聊天功能
- [ ] 观战功能
- [ ] 游戏记录回放

### Phase 4: 优化
- [ ] WebSocket 实时通信
- [ ] 房间过期清理
- [ ] 性能优化
- [ ] 移动端适配

## 技术选型
- 后端: Flask + SQLAlchemy
- 数据库: SQLite (现有)
- 前端: 原生 JavaScript + Canvas
- 实时更新: 轮询 (Phase 1) → WebSocket (Phase 4)
