# drag_coords.py
# Demo：拖动示教（实时获取坐标）

# 同济子豪兄 2024-5-11

# 导入工具包
from pymycobot.mycobot import MyCobot
from pymycobot import PI_PORT, PI_BAUD
import time

# 连接机械臂
mc = MyCobot(PI_PORT, PI_BAUD)

# 机械臂归零
mc.send_angles([0, 0, 0, 0, 0, 0], 60)
time.sleep(3)

# 机械臂移动至桌面
mc.send_angles([0, -90, 0, 0, 0, 0], 40)
time.sleep(3)

# 放松机械臂
mc.release_all_servos()
time.sleep(1)

# 实时获取坐标并打印
start = time.time()
while time.time()-start < 60: # 在一段时间内

    try:
        # 获取当前坐标
        coords = mc.get_coords()
        
        # 解析出坐标值
        X, Y, Z, Rx, Ry, Rz = coords[0], coords[1], coords[2], coords[3], coords[4], coords[5]
        
        # 打印坐标值
        print('X{:7}  Y{:7}  Z{:7}  Rx{:9}  Ry{:7}  Rz{:7}'.format(X, Y, Z, Rx, Ry, Rz))
    except:
        pass