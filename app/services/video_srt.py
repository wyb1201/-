import subprocess  # 用于执行外部命令，如调用 FFmpeg 进行音视频处理。
from faster_whisper import WhisperModel  # 替换为 faster-whisper 库
import opencc  # 用于繁体转简体的库
import os
import torch  

# 检查是否有 GPU 并设置设备
device = "cuda" if torch.cuda.is_available() else "cpu"
print(f"使用设备: {device}")

def extract_audio_from_video(video_path, audio_output_path):
    """
    使用 FFmpeg 从视频中提取音频.
    :param video_path: 视频文件的路径
    :param audio_output_path: 提取音频文件保存路径（.wav 格式）
    """
    command = f'ffmpeg -i "{video_path}" -q:a 0 -map a "{audio_output_path}" -y'
    try:
        result = subprocess.run(command, shell=True, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        print(f"音频已提取至: {audio_output_path}")
    except subprocess.CalledProcessError as e:
        print("提取音频时发生错误:")
        print(e.stderr)
        raise e

def transcribe_audio(audio_path, model):
    """
    使用 Faster Whisper 模型对音频进行语音转录.
    :param audio_path: 音频文件的路径
    :param model: Faster Whisper 模型
    :return: Faster Whisper 转录结果
    """
    print("正在转录音频...")
    segments, info = model.transcribe(audio_path, language="zh")
    return {"segments": segments, "language": info.language}

def generate_srt(transcription, srt_output_path, converter):
    """
    将转录结果转换为 SRT 字幕格式并保存, 同时转换繁体字为简体字.
    :param transcription: Faster Whisper 转录结果
    :param srt_output_path: 输出 SRT 文件路径
    :param converter: 用于繁体字转简体字的 OpenCC 转换器
    """
    print("正在生成 SRT 文件...")
    seen_texts = set()  # 用于存储已写入的文本
    with open(srt_output_path, 'w', encoding="utf-8") as srt_file:
        for i, segment in enumerate(transcription['segments']):
            start = format_time(segment.start)
            end = format_time(segment.end)
            text = segment.text.strip()

            # 使用 opencc 将繁体中文转换为简体中文
            simplified_text = converter.convert(text)

            # 检查是否已写入相同的文本
            if simplified_text not in seen_texts:
                srt_file.write(f"{i + 1}\n{start} --> {end}\n{simplified_text}\n\n")
                seen_texts.add(simplified_text)  # 记录已写入的文本
    print(f"SRT 文件已生成至: {srt_output_path}")

def format_time(seconds):
    """
    将秒数转换为 SRT 文件所需的时间格式.
    :param seconds: 以秒为单位的时间
    :return: SRT 时间格式 (hours:minutes:seconds,milliseconds)
    """
    millisec = int((seconds - int(seconds)) * 1000)
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    seconds = int(seconds % 60)
    return f"{hours:02}:{minutes:02}:{seconds:02},{millisec:03}"

def embed_subtitles_to_video(video_path, srt_path, output_video_path, use_gpu=True):
    """
    使用 FFmpeg 将 SRT 字幕文件嵌入视频中，并根据是否使用 GPU 选择编码器.
    :param video_path: 输入视频文件的路径
    :param srt_path: 字幕文件路径 (.srt)
    :param output_video_path: 输出带字幕的视频文件路径
    :param use_gpu: 是否使用 GPU 加速进行编码
    """
    _, ext = os.path.splitext(output_video_path)
    ext = ext.lower()

    if use_gpu:
        if ext in ['.mp4', '.mkv', '.mov']:
            codec = "h264_nvenc"
            preset = "fast"
            print(f"使用 GPU 加速编码器 h264_nvenc for {ext}.")
        else:
            # 对于不兼容 GPU 编码器的容器，使用软件编码器 libx264
            codec = "libx264"
            preset = "medium"
            print(f"GPU 编码器不支持 {ext}，使用软件编码器 libx264.")
    else:
        codec = "libx264"
        preset = "medium"
        print("使用 CPU 编码器 libx264.")

    # 注意：FFmpeg 可能需要正确转义路径中的特殊字符
    command = (
        f'ffmpeg -y -i "{video_path}" -vf subtitles="{srt_path}" '
        f'-c:v {codec} -preset {preset} -c:a copy "{output_video_path}"'
    )
    print(f"执行 FFmpeg 命令: {command}")
    try:
        result = subprocess.run(command, shell=True, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        print(f"带字幕的视频已保存至: {output_video_path}")
    except subprocess.CalledProcessError as e:
        print("嵌入字幕时发生错误:")
        print(e.stderr)
        raise e

def convert_avi_to_mp4(avi_path, mp4_path):
    """
    使用 FFmpeg 将 AVI 视频转换为 MP4 格式.
    :param avi_path: 输入 AVI 视频文件的路径
    :param mp4_path: 输出 MP4 视频文件的路径
    """
    command = f'ffmpeg -y -i "{avi_path}" -c:v libx264 -c:a aac "{mp4_path}"'
    print(f"转换 AVI 到 MP4: {command}")
    try:
        subprocess.run(command, shell=True, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        print(f"已将 AVI 转换为 MP4: {mp4_path}")
    except subprocess.CalledProcessError as e:
        print("转换 AVI 到 MP4 时发生错误:")
        print(e.stderr)
        raise e

def add_subtitles_to_video(video_path):
    """
    将字幕添加到视频中并返回 SRT 文件和视频路径.
    :param video_path: 输入视频文件的路径
    :return: (srt_output_path, output_video_path)
    """
    # 设置文件路径
    audio_output_path = "extracted_audio.wav"  # 使用相对路径
    srt_output_path = "show.srt"

    # 获取输入视频的扩展名
    _, ext = os.path.splitext(video_path)
    ext = ext.lower()  # 转换为小写以确保一致性

    # 如果输入是 AVI 格式，先转换为 MP4
    if ext == '.avi':
        converted_video_path = os.path.join('app', 'static', 'uploads', 'converted_video.mp4')
        try:
            convert_avi_to_mp4(video_path, converted_video_path)
            video_to_process = converted_video_path
            output_video_filename = "video_with_subtitles.mp4"  # 输出为 MP4 格式
        except Exception as e:
            print(f"转换 AVI 到 MP4 失败: {e}")
            return None, None
    else:
        video_to_process = video_path
        output_video_filename = f"video_with_subtitles{ext}"

    # 构建输出视频的路径，保持与输入视频相同的扩展名（除了 AVI 转换为 MP4）
    output_video_path = os.path.join('app', 'static', 'uploads', output_video_filename)

    # 确保输出目录存在
    output_dir = os.path.dirname(output_video_path)
    os.makedirs(output_dir, exist_ok=True)

    # 确认输入视频文件存在
    absolute_video_path = os.path.abspath(video_to_process)
    if not os.path.exists(absolute_video_path):
        print(f"错误: 视频文件不存在于路径: {absolute_video_path}")
        return None, None

    # 第一步: 从视频中提取音频
    extract_audio_from_video(absolute_video_path, audio_output_path)

    # 第二步: 加载 Faster Whisper 模型
    # 根据设备选择合适的 compute_type
    compute_type = "float16" if device == "cuda" else "int8"  # 对于 CPU，可以使用 "int8" 或 "float32"
    try:
        model = WhisperModel("base", device=device, compute_type=compute_type)
    except Exception as e:
        print(f"加载 WhisperModel 时出错: {e}")
        return None, None

    # 第三步: 转录音频
    transcription = transcribe_audio(audio_output_path, model)

    # 第四步: 使用 OpenCC 进行繁体字到简体字的转换
    converter = opencc.OpenCC('t2s')  # t2s 表示繁体转简体

    # 第五步: 生成 SRT 字幕文件
    generate_srt(transcription, srt_output_path, converter)

    # 第六步: 将生成的 SRT 字幕嵌入到视频中
    use_gpu = (device == "cuda")
    embed_subtitles_to_video(absolute_video_path, srt_path=srt_output_path, output_video_path=output_video_path, use_gpu=use_gpu)

    # 如果输入是 AVI 格式，删除临时转换的 MP4 文件
    if ext == '.avi':
        try:
            os.remove(converted_video_path)
            print(f"已删除临时文件: {converted_video_path}")
        except Exception as e:
            print(f"删除临时文件 {converted_video_path} 时发生错误: {e}")

    return srt_output_path, output_video_path

if __name__ == "__main__":
    video_path = "videos/video_04.avi"  # 替换为您的输入视频文件路径
    srt_output_path, output_video_path = add_subtitles_to_video(video_path)
    if srt_output_path and output_video_path:
        print(f"SRT 文件: {srt_output_path}")
        print(f"带字幕的视频: {output_video_path}")
    else:
        print("添加字幕到视频时失败。")
