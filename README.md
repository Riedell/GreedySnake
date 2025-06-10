# GreedySnake
A Greedy Snake Game Implemented in Python.

这是一个使用Python和Pygame库实现的贪吃蛇游戏  
![image](https://github.com/user-attachments/assets/a078de74-a5c1-4986-afd0-017f0ae7313e)


## 游戏特点

- 精美像素风格界面
- 流畅的蛇移动动画
- 多种食物类型（不同颜色和分数）
- 动态变化的食物（普通食物和特殊食物）
- 障碍物设计增加难度
- 分数显示和最高分记录
- 游戏暂停和重新开始功能
- 碰撞特效

## 游戏控制

- **方向键 / WASD**：控制蛇的移动方向
- **空格键**：暂停/继续游戏
- **R键**：重新开始游戏
- **ESC键**：退出游戏

## 游戏规则

1. 使用方向键 / WASD控制蛇的移动方向
2. 吃到红色食物得1分，金色食物得3分，紫色食物得5分
3. 每得5分蛇的速度会增加
4. 撞到墙壁、自己的身体或障碍物游戏结束
5. 游戏结束后按R键重新开始

## 部署运行步骤



### 1. 安装Python

### 2. 安装Pygame

```bash
pip install pygame
```

### 3. 运行游戏

1. 在命令提示符或终端中，导航到游戏文件夹：

   ```bash
   cd path/to/snake_game
   ```

2. 运行游戏：

   ```bash
   python snake_game.py
   ```



## 使用 UV 部署和运行（推荐）

### 1. 安装 UV

```bash
pip install uv
```

### 3. 创建虚拟环境

```bash
# uv venv .venv
uv venv
```

### 4. 激活虚拟环境

- Windows:

  ```bash
  .\.venv\Scripts\activate
  ```

- macOS/Linux:

  ```bash
  source .venv/bin/activate
  ```

### 5. 安装依赖

```bash
uv pip install pygame
# uv pip list
```

### 6. 运行游戏

```bash
# python snake_game.py
# Pycharm Run Button # chcp 65001
uv run .\snake_game.py # uv run
```


## 常见问题解决

### 1. pychram提示：Error: Python packaging tool 'setuptools' not found

```bash
uv pip install setuptools
```



### 2. 方向键没反应

1. 切换输入法为英文状态
2. 确认事件循环是否正常运行

在 Game.run() 中检查以下代码是否正确执行：

```python
for event in pygame.event.get():
    if event.type == pygame.QUIT:
        ...
    if event.type == pygame.KEYDOWN:
        ...
```

- 确保这段代码位于主循环中。
- 检查是否被其他逻辑中断（如死循环、异常抛出等）。
  可以加一句调试打印：

可以加一句调试打印：

```python
print(event)
```

运行游戏后，在终端查看是否有类似 <Event(2-KeyButtonDown ...)> 的输出。如果没有，说明 Pygame 未接收到键盘输入。

3. 焦点问题：窗口是否获得输入焦点？

有时，Pygame 窗口可能未获得输入焦点，导致按键无效。
解决方案：
确保你在启动游戏后点击了游戏窗口，使它获得焦点。
也可以尝试在初始化后添加一个提示：

```python
print("请单击游戏窗口以获取键盘控制权...")
```






















