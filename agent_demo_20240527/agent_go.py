# agent_go.py
# 同济子豪兄 2024-5-27
# 看懂“图像”、听懂“人话”、指哪打哪的机械臂
# 机械臂+大模型+多模态+语音识别=具身智能体Agent

print('\n听得懂人话、看得懂图像、拎得清动作的具身智能机械臂！')
print('同济子豪兄 2024-5-27 \n')

# 导入常用函数
from utils_asr import *             # 录音+语音识别
from utils_robot import *           # 连接机械臂
from utils_llm import *             # 大语言模型API
from utils_led import *             # 控制LED灯颜色
from utils_camera import *          # 摄像头
from utils_robot import *           # 机械臂运动
from utils_pump import *            # GPIO、吸泵
from utils_vlm_move import *        # 多模态大模型识别图像，吸泵吸取并移动物体
from utils_drag_teaching import *   # 拖动示教
from utils_agent import *           # 智能体Agent编排
from utils_tts import *             # 语音合成模块

# print('播放欢迎词')
pump_off()
# back_zero()
play_wav('asset/welcome.wav')


def agent_play():
    '''
    主函数，语音控制机械臂智能体编排动作
    '''
    # 归零
    back_zero()
    
    # print('测试摄像头')
    # check_camera()
    
    # 输入指令
    # 先回到原点，再把LED灯改为墨绿色，然后把绿色方块放在篮球上
    start_record_ok = input('是否开启录音，输入数字录音指定时长，按k打字输入，按c输入默认指令\n')
    if str.isnumeric(start_record_ok):
        DURATION = int(start_record_ok)
        record(DURATION=DURATION)   # 录音
        order = speech_recognition() # 语音识别
    elif start_record_ok == 'k':
        order = input('请输入指令')
    elif start_record_ok == 'c':
        order = '先归零，再摇头，然后把绿色方块放在篮球上'
    else:
        print('无指令，退出')
        # exit()
        raise NameError('无指令，退出')
    
    # 智能体Agent编排动作
    agent_plan_output = eval(agent_plan(order))
    
    print('智能体编排动作如下\n', agent_plan_output)
    # plan_ok = input('是否继续？按c继续，按q退出')
    plan_ok = 'c'
    if plan_ok == 'c':
        response = agent_plan_output['response'] # 获取机器人想对我说的话
        print('开始语音合成')
        tts(response)                     # 语音合成，导出wav音频文件
        play_wav('temp/tts.wav')          # 播放语音合成音频文件
        for each in agent_plan_output['function']: # 运行智能体规划编排的每个函数
            print('开始执行动作', each)
            eval(each)
    elif plan_ok =='q':
        # exit()
        raise NameError('按q退出')

# agent_play()
if __name__ == '__main__':
    agent_play()

