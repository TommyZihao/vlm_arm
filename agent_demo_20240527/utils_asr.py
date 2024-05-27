# utils_asr.py
# 同济子豪兄 2024-5-22
# 录音+语音识别

print('导入录音+语音识别模块')

import pyaudio
import wave
import numpy as np
import os
import sys
from API_KEY import *

# 确定麦克风索引号
# import sounddevice as sd
# print(sd.query_devices())

def record(MIC_INDEX=0, DURATION=5):
    '''
    调用麦克风录音，需用arecord -l命令获取麦克风ID
    DURATION，录音时长
    '''
    print('开始 {} 秒录音'.format(DURATION))
    os.system('sudo arecord -D "plughw:{}" -f dat -c 1 -r 16000 -d {} temp/speech_record.wav'.format(MIC_INDEX, DURATION))
    print('录音结束')

def record_auto(MIC_INDEX=1):
    '''
    开启麦克风录音，保存至'temp/speech_record.wav'音频文件
    音量超过阈值自动开始录音，低于阈值一段时间后自动停止录音
    MIC_INDEX：麦克风设备索引号
    '''
    
    CHUNK = 1024               # 采样宽度
    RATE = 16000               # 采样率
    
    QUIET_DB = 2000            # 分贝阈值，大于则开始录音，否则结束
    delay_time = 1             # 声音降至分贝阈值后，经过多长时间，自动终止录音
    
    FORMAT = pyaudio.paInt16
    CHANNELS = 1 if sys.platform == 'darwin' else 2 # 采样通道数
    
    # 初始化录音
    p = pyaudio.PyAudio()
    stream = p.open(format=FORMAT,
                    channels=CHANNELS,
                    rate=RATE,
                    input=True,
                    frames_per_buffer=CHUNK,
                    input_device_index=MIC_INDEX
                   )
    
    frames = []             # 所有音频帧
    
    flag = False            # 是否已经开始录音
    quiet_flag = False      # 当前音量小于阈值
    
    temp_time = 0           # 当前时间是第几帧
    last_ok_time = 0        # 最后正常是第几帧
    START_TIME = 0          # 开始录音是第几帧
    END_TIME = 0            # 结束录音是第几帧
    
    print('可以说话啦！')
    
    while True:
        
        # 获取当前chunk的声音
        data = stream.read(CHUNK, exception_on_overflow=False)
        frames.append(data)
        # 获取当前chunk的音量分贝值
        temp_volume = np.max(np.frombuffer(data, dtype=np.short))
        
        if temp_volume > QUIET_DB and flag==False:
            print("音量高于阈值，开始录音")
            flag =True
            START_TIME = temp_time
            last_ok_time = temp_time
    
        if flag: # 录音中的各种情况
    
            if(temp_volume < QUIET_DB and quiet_flag==False):
                print("录音中，当前音量低于阈值")
                quiet_flag = True
                last_ok_time = temp_time
                
            if(temp_volume > QUIET_DB):
                # print('录音中，当前音量高于阈值，正常录音')
                quiet_flag = False
                last_ok_time = temp_time
    
            if(temp_time > last_ok_time + delay_time*15 and quiet_flag==True):
                print("音量低于阈值{:.2f}秒后，检测当前音量".format(delay_time))
                if(quiet_flag and temp_volume < QUIET_DB):
                    print("当前音量仍然小于阈值，录音结束")
                    END_TIME = temp_time
                    break
                else:
                    print("当前音量重新高于阈值，继续录音中")
                    quiet_flag = False
                    last_ok_time = temp_time
                    
        # print('当前帧 {} 音量 {}'.format(temp_time+1, temp_volume))
        temp_time += 1
        if temp_time > 150:  # 超时直接退出
            END_TIME = temp_time
            print('超时，录音结束')
            break
    
    # 停止录音
    stream.stop_stream()
    stream.close()
    p.terminate()
    
    # 导出wav音频文件
    output_path = 'temp/speech_record.wav'
    wf = wave.open(output_path, 'wb')
    wf.setnchannels(CHANNELS)
    wf.setsampwidth(p.get_sample_size(FORMAT))
    wf.setframerate(RATE)
    wf.writeframes(b''.join(frames[START_TIME-2:END_TIME]))
    wf.close()
    print('保存录音文件', output_path)

import appbuilder
# 配置密钥
os.environ["APPBUILDER_TOKEN"] = APPBUILDER_TOKEN
asr = appbuilder.ASR() # 语音识别组件
def speech_recognition(audio_path='temp/speech_record.wav'):
    '''
    AppBuilder-SDK语音识别组件
    '''
    print('开始语音识别')
    # 载入wav音频文件
    with wave.open(audio_path, 'rb') as wav_file:
        
        # 获取音频文件的基本信息
        num_channels = wav_file.getnchannels()
        sample_width = wav_file.getsampwidth()
        framerate = wav_file.getframerate()
        num_frames = wav_file.getnframes()
        
        # 获取音频数据
        frames = wav_file.readframes(num_frames)
        
    # 向API发起请求
    content_data = {"audio_format": "wav", "raw_audio": frames, "rate": 16000}
    message = appbuilder.Message(content_data)
    speech_result = asr.run(message).content['result'][0]
    print('语音识别结果：', speech_result)
    return speech_result