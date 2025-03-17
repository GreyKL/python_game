import os
from moviepy.editor import VideoFileClip


def extract_audio(input_video_path, output_audio_path):
    """
    从视频文件中提取音频并保存为指定格式

    参数:
        input_video_path (str): 输入视频文件路径
        output_audio_path (str): 输出音频文件路径

    支持格式:
        输入视频: .mp4, .mov, .avi 等常见视频格式
        输出音频: .mp3, .wav, .ogg, .aac 等常见音频格式

    依赖:
        需要安装 moviepy 和 ffmpeg
    """
    try:
        # 检查输入文件是否存在
        if not os.path.isfile(input_video_path):
            raise FileNotFoundError(f"输入视频文件 {input_video_path} 不存在")

        # 创建输出目录（如果不存在）
        output_dir = os.path.dirname(output_audio_path)
        if output_dir and not os.path.exists(output_dir):
            os.makedirs(output_dir)

        # 加载视频文件并提取音频
        with VideoFileClip(input_video_path) as video:
            audio = video.audio
            if audio is None:
                raise ValueError("视频文件中没有找到音频轨道")

            # 根据输出格式写入音频文件
            audio.write_audiofile(output_audio_path, verbose=False, logger=None)

        print(f"成功提取音频到: {output_audio_path}")
        return True

    except Exception as e:
        print(f"处理过程中出现错误: {str(e)}")
        return False


# 使用示例
if __name__ == "__main__":
    # 提取 MP4 为 MP3
    extract_audio("/Users/kuangli/Movies/8月18日.mp4", "output_audio.mp3")

    # 提取 MOV 为 WAV
    # extract_audio("input_video.mov", "output_audio.wav")