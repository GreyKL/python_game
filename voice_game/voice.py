import sounddevice as sd
import numpy as np
import speech_recognition as sr
from pynput import keyboard  # 用于监听键盘事件
import pyautogui  # 用于模拟快捷键操作


def record_audio(duration=2, sample_rate=16000):
    """
    录制音频
    """
    print("开始录音...")
    audio = sd.rec(int(duration * sample_rate), samplerate=sample_rate, channels=1, dtype='int16')
    sd.wait()  # 等待录音完成
    print("录音结束...")
    return audio


def recognize_audio(audio_data, sample_rate=16000):
    """
    将录音转化为文字
    """
    recognizer = sr.Recognizer()
    try:
        # 将 NumPy 数据转换为 AudioData
        audio = sr.AudioData(audio_data.tobytes(), sample_rate=sample_rate, sample_width=2)
        text = recognizer.recognize_google(audio, language="zh-CN")
        print(f"识别结果: {text}")
        return text
    except sr.UnknownValueError:
        print("无法识别语音")
    except sr.RequestError as e:
        print(f"语音识别服务出错: {e}")
    return ""


def handle_command(command):
    """
    根据识别的语音执行不同逻辑
    """
    if "截图" in command:
        pyautogui.keyDown("command")
        pyautogui.keyDown("shift")
        pyautogui.press("3")  # 按下 "3"
        pyautogui.keyUp("shift")
        pyautogui.keyUp("command")
        print("截图完成")  # macOS 的截图快捷键，Windows 可改为 "win", "printscreen"
    elif "结束程序" in command:
        print("正在结束程序...")
        exit(0)  # 退出程序09
    else:
        print("未匹配的命令")


class KeyListener:
    """
    键盘监听器类
    """
    def __init__(self):
        self.keys_pressed = set()  # 存储当前按下的键

    def on_press(self, key):
        """
        键盘按下事件
        """
        try:
            if hasattr(key, 'char') and key.char:  # 检测普通按键
                self.keys_pressed.add(key.char)

            # 检测是否同时按下 '9' 和 '0'
            if 'm' in self.keys_pressed and 'n' in self.keys_pressed:
                print("检测到按键组合，准备录音...")
                audio_data = record_audio()  # 录制音频
                text = recognize_audio(audio_data)  # 转文字
                if text:  # 如果成功识别
                    handle_command(text)  # 根据识别内容执行命令
        except Exception as e:
            print(f"按键处理异常: {e}")

    def on_release(self, key):
        """
        键盘释放事件
        """
        try:
            if hasattr(key, 'char') and key.char:
                self.keys_pressed.discard(key.char)  # 从按下集合中移除
        except Exception as e:
            print(f"按键释放异常: {e}")


def main():
    print("程mn序已启动，按下 'm' 和 'n' 键开始录音...")
    listener = KeyListener()

    # 启动键盘监听器
    with keyboard.Listener(on_press=listener.on_press, on_release=listener.on_release) as k_listener:
        k_listener.join()


if __name__ == "__main__":
    main()