# drag_angles.py
# Demo：拖动示教（实时获取角度）

# 同济子豪兄 2024-5-13

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
while time.time()-start < 120: # 在一段时间内

    try:
        # 获取当前坐标
        angles = mc.get_angles()
        
        # 解析出坐标值
        A, B, C, D, E, F = angles[0], angles[1], angles[2], angles[3], angles[4], angles[5]
        
        # 打印坐标值
        print('A{:7}  B{:7}  C{:7}  D{:7}  E{:7}  F{:7}'.format(A, B, C, D, E, F))
    except:
        pass