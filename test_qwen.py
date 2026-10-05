import requests
import json

system_instruction = """Bạn là một chuyên gia giáo dục ngôn ngữ. Hãy tạo danh sách từ vựng tiếng Anh chính xác dựa trên yêu cầu của người dùng.
Yêu cầu người dùng: "Tạo 10 từ vựng TOEIC chủ đề Technology (Phần 1)"
Mỗi từ bắt buộc phải có đầy đủ phiên âm IPA, loại từ, nghĩa tiếng Việt, một câu ví dụ tiếng Anh thực tế, nghĩa tiếng Việt của câu ví dụ và tên chủ đề tương ứng.
BẮT BUỘC chỉ tạo đúng số lượng 10 từ được yêu cầu, KHÔNG ĐƯỢC tạo thừa hoặc thiếu dù chỉ 1 từ. Đảm bảo các từ sinh ra đa dạng và phong phú.
Trả về dữ liệu dưới dạng JSON là một mảng các object. KHÔNG dùng markdown block.
Cấu trúc mỗi object:
{
    "english": "từ tiếng Anh",
    "vietnamese": "nghĩa tiếng Việt",
    "pos": "loại từ (N, V, ADJ, ADV, PREP, CONJ)",
    "pronunciation": "phiên âm",
    "example_en": "câu ví dụ tiếng Anh",
    "example_vi": "nghĩa câu ví dụ",
    "topic": "tên chủ đề"
}"""

try:
    response = requests.post('http://localhost:11434/api/chat', json={
        'model': 'qwen2.5:7b',
        'messages': [
            {'role': 'user', 'content': system_instruction}
        ],
        'stream': False,
        'options': {'temperature': 0.8, 'num_predict': 2048}
    }, timeout=120)
    result = response.json()
    with open('test_qwen_output.txt', 'w', encoding='utf-8') as f:
        f.write(result.get('message', {}).get('content', 'No content'))
    print("Success")
except Exception as e:
    print(f'Error: {e}')
