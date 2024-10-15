from flask import request, jsonify
from app.services.reply import interact_with_model

def ask():
    data = request.get_json()
    question = data.get('question')

    # 获取答案
    answer, url= interact_with_model(question)

    resp_answer = {
        'acknowledge': answer.acknowledge,
        'reply': answer.reply,
        'b_url': url
    }

    return jsonify(resp_answer)