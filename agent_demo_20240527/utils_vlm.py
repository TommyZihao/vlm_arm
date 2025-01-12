# utils_vlm.py
# 同济子豪兄 2024-5-22
# 多模态大模型、可视化

print('导入视觉大模型模块')
import time
import cv2
import numpy as np
from PIL import Image
from PIL import ImageFont, ImageDraw
# 导入中文字体，指定字号
font = ImageFont.truetype('asset/SimHei.ttf', 26)

from API_KEY import *

# 系统提示词
SYSTEM_PROMPT = '''
我即将说一句给机械臂的指令，你帮我从这句话中提取出起始物体和终止物体，并从这张图中分别找到这两个物体左上角和右下角的像素坐标，输出json数据结构。

例如，如果我的指令是：请帮我把红色方块放在房子简笔画上。
你输出这样的格式：
{
 "start":"红色方块",
 "start_xyxy":[[102,505],[324,860]],
 "end":"房子简笔画",
 "end_xyxy":[[300,150],[476,310]]
}

只回复json本身即可，不要回复其它内容

我现在的指令是：
'''

# Yi-Vision调用函数
import openai
from openai import OpenAI
import base64
def yi_vision_api(PROMPT='帮我把红色方块放在钢笔上', img_path='temp/vl_now.jpg'):

    '''
    零一万物大模型开放平台，yi-vision视觉语言多模态大模型API
    '''
    
    client = OpenAI(
        api_key=YI_KEY,
        base_url="https://api.lingyiwanwu.com/v1"
    )
    
    # 编码为base64数据
    with open(img_path, 'rb') as image_file:
        image = 'data:image/jpeg;base64,' + base64.b64encode(image_file.read()).decode('utf-8')
    
    # 向大模型发起请求
    completion = client.chat.completions.create(
      model="yi-vision",
      messages=[
        {
          "role": "user",
          "content": [
            {
              "type": "text",
              "text": SYSTEM_PROMPT + PROMPT
            },
            {
              "type": "image_url",
              "image_url": {
                "url": image
              }
            }
          ]
        },
      ]
    )
    
    # 解析大模型返回结果
    result = eval(completion.choices[0].message.content.strip())
    print('    大模型调用成功！')
    
    return result


def QwenVL_api(PROMPT='帮我把红色方块放在钢笔上', img_path='temp/vl_now.jpg'):
    '''
    通义千问QwenVL视觉语言多模态大模型API，模型列表请见：https://help.aliyun.com/zh/model-studio/getting-started/models?spm=0.0.0.i3#9f8890ce29g5u
    '''

    client = OpenAI(
        api_key=Qwen_KEY,
        base_url="https://dashscope.aliyuncs.com/compatible-mode/v1"
    )

    # 编码为base64数据
    with open(img_path, 'rb') as image_file:
        image = 'data:image/jpeg;base64,' + base64.b64encode(image_file.read()).decode('utf-8')

    # 向大模型发起请求
    completion = client.chat.completions.create(
        model="qwen-vl-max-latest",
        messages=[
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": SYSTEM_PROMPT + PROMPT
                    },
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": image
                        }
                    }
                ]
            },
        ]
    )

    # 解析大模型返回结果
    result = eval(completion.choices[0].message.content.strip())
    print('    大模型调用成功！')

    return result

def post_processing_viz(result, img_path, check=False):
    
    '''
    视觉大模型输出结果后处理和可视化
    check：是否需要人工看屏幕确认可视化成功，按键继续或退出
    '''

    # 后处理
    img_bgr = cv2.imread(img_path)
    img_h = img_bgr.shape[0]
    img_w = img_bgr.shape[1]
    # 缩放因子
    FACTOR = 999
    # 起点物体名称
    START_NAME = result['start']
    # 终点物体名称
    END_NAME = result['end']
    # 起点，左上角像素坐标
    START_X_MIN = int(result['start_xyxy'][0][0] * img_w / FACTOR)
    START_Y_MIN = int(result['start_xyxy'][0][1] * img_h / FACTOR)
    # 起点，右下角像素坐标
    START_X_MAX = int(result['start_xyxy'][1][0] * img_w / FACTOR)
    START_Y_MAX = int(result['start_xyxy'][1][1] * img_h / FACTOR)
    # 起点，中心点像素坐标
    START_X_CENTER = int((START_X_MIN + START_X_MAX) / 2)
    START_Y_CENTER = int((START_Y_MIN + START_Y_MAX) / 2)
    # 终点，左上角像素坐标
    END_X_MIN = int(result['end_xyxy'][0][0] * img_w / FACTOR)
    END_Y_MIN = int(result['end_xyxy'][0][1] * img_h / FACTOR)
    # 终点，右下角像素坐标
    END_X_MAX = int(result['end_xyxy'][1][0] * img_w / FACTOR)
    END_Y_MAX = int(result['end_xyxy'][1][1] * img_h / FACTOR)
    # 终点，中心点像素坐标
    END_X_CENTER = int((END_X_MIN + END_X_MAX) / 2)
    END_Y_CENTER = int((END_Y_MIN + END_Y_MAX) / 2)
    
    # 可视化
    # 画起点物体框
    img_bgr = cv2.rectangle(img_bgr, (START_X_MIN, START_Y_MIN), (START_X_MAX, START_Y_MAX), [0, 0, 255], thickness=3)
    # 画起点中心点
    img_bgr = cv2.circle(img_bgr, [START_X_CENTER, START_Y_CENTER], 6, [0, 0, 255], thickness=-1)
    # 画终点物体框
    img_bgr = cv2.rectangle(img_bgr, (END_X_MIN, END_Y_MIN), (END_X_MAX, END_Y_MAX), [255, 0, 0], thickness=3)
    # 画终点中心点
    img_bgr = cv2.circle(img_bgr, [END_X_CENTER, END_Y_CENTER], 6, [255, 0, 0], thickness=-1)
    # 写中文物体名称
    img_rgb = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2RGB) # BGR 转 RGB
    img_pil = Image.fromarray(img_rgb) # array 转 pil
    draw = ImageDraw.Draw(img_pil)
    # 写起点物体中文名称
    draw.text((START_X_MIN, START_Y_MIN-32), START_NAME, font=font, fill=(255, 0, 0, 1)) # 文字坐标，中文字符串，字体，rgba颜色
    # 写终点物体中文名称
    draw.text((END_X_MIN, END_Y_MIN-32), END_NAME, font=font, fill=(0, 0, 255, 1)) # 文字坐标，中文字符串，字体，rgba颜色
    img_bgr = cv2.cvtColor(np.array(img_pil), cv2.COLOR_RGB2BGR) # RGB转BGR
    # 保存可视化效果图
    cv2.imwrite('temp/vl_now_viz.jpg', img_bgr)

    formatted_time = time.strftime("%Y%m%d%H%M", time.localtime())
    cv2.imwrite('visualizations/{}.jpg'.format(formatted_time), img_bgr)

    # 在屏幕上展示可视化效果图
    cv2.imshow('zihao_vlm', img_bgr) 

    if check:
        print('    请确认可视化成功，按c键继续，按q键退出')
        while(True):
            key = cv2.waitKey(10) & 0xFF
            if key == ord('c'): # 按c键继续
                break
            if key == ord('q'): # 按q键退出
                # exit()
                cv2.destroyAllWindows()   # 关闭所有opencv窗口
                raise NameError('按q退出')
    else:
        if cv2.waitKey(1) & 0xFF == None:
            pass

    return START_X_CENTER, START_Y_CENTER, END_X_CENTER, END_Y_CENTER
