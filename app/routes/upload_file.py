import os
from flask import request, jsonify
from werkzeug.utils import secure_filename
from app.services.repair import picture_mind, ai_anaylase
from app.services.video_srt import add_subtitles_to_video

key = None

# 保存用户密钥
def set_key():
    data = request.get_json()
    global key
    key = data.get('apiKey')
    return '',204

# 接收用户视频，生成
def upload_file():
    if 'file' not in request.files:
        return jsonify({'error': '没有文件被上传'}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': '没有文件名'}), 400

    # 保存视频
    filename = secure_filename(file.filename)
    file_path = os.path.join('app/static/uploads', filename)
    file.save(file_path)

    print(f"视频文件保存到: {file_path}")

    # 调用逻辑处理
    srt_path, fina_path = add_subtitles_to_video(file_path)
    # resp = ai_analyse(srt_path,api_key)  # api_key

    ana_chunks, overall_summary = ai_anaylase(srt_path, key)
    print(overall_summary)
    image_path = os.path.join('app', 'static','uploads','mind.png' )
    image = picture_mind(overall_summary,image_path)

    print(f"生成的视频文件保存到: {fina_path}")
    print(f"生成的脑图保存到: {image}")

    response_data = {
        'video_path': fina_path,
        'video_prompt': {
            'title': overall_summary.title,
            'contents': overall_summary.contents
        },
        'image_path': image_path
    }

    return jsonify(response_data)

