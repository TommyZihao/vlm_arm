# utils_led.py
# 同济子豪兄 2024-5-22
# 大模型控制LED灯颜色

from utils_llm import llm_qianfan, llm_yi
from utils_robot import mc

print('导入LED灯控制模块')

# 备选颜色
# 贝加尔湖、中国红、大海、绿叶、金子、蓝宝石、小猪佩奇、墨绿色、黑色

# 系统提示词
SYS_PROMPT = '我即将说的这句话中包含一个目标物体，帮我把这个物体的一种可能的颜色，以0-255的RGB像素值形式返回给我，整理成元组格式，例如(255, 30, 60)，直接回复元组本身，以括号开头，不要回复任何中文内容，下面是这句话：'

def llm_led(PROMPT_LED='帮我把LED灯的颜色改为贝加尔湖的颜色'):
    '''
    大模型控制LED灯颜色
    '''
    
    PROMPT = SYS_PROMPT + PROMPT_LED
    
    n = 1
    while n < 5:
        try:
            # 调用大模型API
            # response = llm_qianfan(PROMPT) 
            response = llm_yi(PROMPT) 
            
            # 提取颜色
            rgb_tuple = eval(response)
        
            # 设置LED灯的RGB颜色
            mc.set_color(rgb_tuple[0], rgb_tuple[1], rgb_tuple[2])
            print('LED灯颜色修改成功', rgb_tuple)

            break
            
        except Exception as e:
            print('大模型返回json结构错误，再尝试一次', e)
            n += 1