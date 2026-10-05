import csv
import io
import openpyxl
import json
import random
from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from .models import Word, UserWord, QuizHistory, Topic

def home_view(request):
    total_words = Word.objects.count()
    topics = Topic.objects.all()
    return render(request, 'home.html', {
        'total_words': total_words,
        'topics': topics
    })


def flashcard_view(request):
    words = Word.objects.all()
    topics = Topic.objects.all()
    
    words_data = []
    for w in words:
        words_data.append({
            'id': w.id,
            'word': w.english_word,
            'pronunciation': w.pronunciation if w.pronunciation else '',
            'pos': w.part_of_speech,
            'meaning': w.vietnamese_meaning,
            'exampleEn': w.example_sentence if w.example_sentence else '',
            'exampleVi': w.example_meaning if w.example_meaning else '',
            'topic_id': str(w.topic.id) if w.topic else ''
        })
        
    return render(request, 'flashcard.html', {
        'words': words, 
        'topics': topics,
        'words_json': words_data
    })

@require_POST
def update_word_status(request):
    if not request.user.is_authenticated:
        return JsonResponse({'success': True, 'message': 'Đã lưu cục bộ (Local Storage).'})
        
    try:
        data = json.loads(request.body)
        word_id = data.get('word_id')
        status = data.get('status')
        
        if not word_id or status not in ['LEARNED', 'REVIEW']:
            return JsonResponse({'error': 'Dữ liệu không hợp lệ.'}, status=400)
            
        word = Word.objects.get(id=word_id)
        
        UserWord.objects.update_or_create(
            user=request.user,
            word=word,
            defaults={'status': status}
        )
        return JsonResponse({'success': True, 'message': 'Đã lưu tiến độ thành công!'})
    except Word.DoesNotExist:
        return JsonResponse({'error': 'Không tìm thấy từ vựng trong hệ thống.'}, status=404)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

def quiz_view(request):
    topics = Topic.objects.all()
    all_words = list(Word.objects.all())
    total_words = len(all_words)
    
    if total_words < 4:
        return render(request, 'quiz.html', {'not_enough_words': True, 'topics': topics})
        
    num_questions = total_words
    target_words = random.sample(all_words, num_questions)
    
    quiz_data = []
    for word in target_words:
        other_words = [w for w in all_words if w.id != word.id]
        distractors = random.sample(other_words, 3)
        
        options = [
            {'text': word.vietnamese_meaning, 'is_correct': True}
        ]
        for d in distractors:
            options.append({'text': d.vietnamese_meaning, 'is_correct': False})
            
        random.shuffle(options) 
        
        quiz_data.append({
            'id': word.id,
            'english_word': word.english_word,
            'part_of_speech': word.part_of_speech,
            'pronunciation': word.pronunciation,
            'options': options
        })
        
    context = {
        'not_enough_words': False,
        'quiz_data_json': json.dumps(quiz_data),
        'topics': topics
    }
    return render(request, 'quiz.html', context)

def api_quiz_generate(request):
    topic_id = request.GET.get('topic_id')
    
    if topic_id:
        all_words = list(Word.objects.filter(topic_id=topic_id))
    else:
        all_words = list(Word.objects.all())
        
    total_words = len(all_words)
    global_words = list(Word.objects.all())
    
    if len(global_words) < 4:
        return JsonResponse({'error': 'Hệ thống cần ít nhất 4 từ vựng để tạo bài Quiz.'}, status=400)
        
    if total_words == 0:
        return JsonResponse({'error': 'Chủ đề này chưa có từ vựng nào.'}, status=400)

    num_questions = total_words
    target_words = random.sample(all_words, num_questions)
    
    quiz_data = []
    for word in target_words:
        # Distractors có thể lấy từ global_words để đảm bảo luôn đủ 3 đáp án sai
        other_words = [w for w in global_words if w.id != word.id]
        distractors = random.sample(other_words, 3)
        
        options = [
            {'text': word.vietnamese_meaning, 'is_correct': True}
        ]
        for d in distractors:
            options.append({'text': d.vietnamese_meaning, 'is_correct': False})
            
        random.shuffle(options) 
        
        quiz_data.append({
            'id': word.id,
            'english_word': word.english_word,
            'part_of_speech': word.part_of_speech,
            'pronunciation': word.pronunciation,
            'options': options
        })
        
    return JsonResponse({'success': True, 'quiz_data': quiz_data})

@require_POST
def save_quiz_history(request):
    if not request.user.is_authenticated:
        return JsonResponse({'success': True, 'message': 'Đã lưu cục bộ (Local Storage).'})
        
    try:
        data = json.loads(request.body)
        score = int(data.get('score', 0))
        total_questions = int(data.get('total_questions', 0))
        
        QuizHistory.objects.create(
            user=request.user,
            score=score,
            total_questions=total_questions
        )
        return JsonResponse({'success': True})
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)

def dashboard_view(request):
    total_words = Word.objects.count()
    
    backend_history_str = "[]"
    if request.user.is_authenticated:
        histories = QuizHistory.objects.filter(user=request.user).order_by('-created_at')
        history_list = []
        for h in histories:
            history_list.append({
                'score': h.score,
                'total_questions': h.total_questions,
                'percentage': round((h.score / h.total_questions) * 100) if h.total_questions > 0 else 0,
                'created_at': h.created_at.isoformat()
            })
        backend_history_str = json.dumps(history_list)
        
    context = {
        'total_words': total_words,
        'backend_history': backend_history_str
    }
    return render(request, 'dashboard.html', context)

def manage_words_view(request):
    words = Word.objects.select_related('topic').all().order_by('-created_at')
    topics = Topic.objects.all()
    return render(request, 'manage_words.html', {'words': words, 'topics': topics})

@require_POST
def api_save_word(request):
    try:
        data = json.loads(request.body)
        word_id = data.get('id')
        
        english_word = data.get('english_word', '').strip()
        vietnamese_meaning = data.get('vietnamese_meaning', '').strip()
        part_of_speech = data.get('part_of_speech', 'N')
        pronunciation = data.get('pronunciation', '').strip()
        example_sentence = data.get('example_sentence', '').strip()
        example_meaning = data.get('example_meaning', '').strip()
        topic_id = data.get('topic_id')
        
        if not english_word or not vietnamese_meaning:
            return JsonResponse({'error': 'Từ tiếng Anh và nghĩa tiếng Việt là bắt buộc.'}, status=400)
            
        defaults = {
            'english_word': english_word,
            'vietnamese_meaning': vietnamese_meaning,
            'part_of_speech': part_of_speech,
            'pronunciation': pronunciation,
            'example_sentence': example_sentence,
            'example_meaning': example_meaning,
        }
        
        defaults['topic_id'] = topic_id if topic_id else None
        
        if word_id:
            word, created = Word.objects.update_or_create(id=word_id, defaults=defaults)
            action = 'updated'
        else:
            word = Word.objects.create(**defaults)
            action = 'created'
            
        return JsonResponse({
            'success': True, 
            'action': action,
            'word': {
                'id': word.id,
                'english_word': word.english_word,
                'vietnamese_meaning': word.vietnamese_meaning,
                'part_of_speech': word.part_of_speech,
                'pronunciation': word.pronunciation,
                'example_sentence': word.example_sentence,
                'example_meaning': word.example_meaning,
                'topic_id': word.topic_id,
            }
        })
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)

@require_POST
def api_delete_word(request):
    try:
        data = json.loads(request.body)
        word_id = data.get('id')
        if not word_id:
            return JsonResponse({'error': 'Không tìm thấy ID từ vựng.'}, status=400)
            
        Word.objects.filter(id=word_id).delete()
        return JsonResponse({'success': True})
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)

@require_POST
def api_save_topic(request):
    try:
        data = json.loads(request.body)
        name = data.get('name', '').strip()
        
        if not name:
            return JsonResponse({'error': 'Tên chủ đề là bắt buộc.'}, status=400)
            
        topic, created = Topic.objects.get_or_create(name=name)
        
        return JsonResponse({
            'success': True,
            'topic': {
                'id': topic.id,
                'name': topic.name,
                'slug': topic.slug
            }
        })
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)

@require_POST
def api_import_words(request):
    if 'file' not in request.FILES:
        return JsonResponse({'error': 'Vui lòng chọn một file đính kèm.'}, status=400)
        
    uploaded_file = request.FILES['file']
    filename = uploaded_file.name.lower()
    
    rows = []
    
    try:
        if filename.endswith('.csv'):
            decoded_file = uploaded_file.read().decode('utf-8-sig')
            io_string = io.StringIO(decoded_file)
            reader = csv.DictReader(io_string)
            for row in reader:
                rows.append({k.strip().lower(): v.strip() for k, v in row.items() if k and v is not None})
                
        elif filename.endswith('.xlsx'):
            wb = openpyxl.load_workbook(uploaded_file, data_only=True)
            sheet = wb.active
            headers = []
            for i, row in enumerate(sheet.iter_rows(values_only=True)):
                if i == 0:
                    headers = [str(cell).strip().lower() if cell else f"col_{j}" for j, cell in enumerate(row)]
                else:
                    row_data = {}
                    for j, cell in enumerate(row):
                        if j < len(headers):
                            row_data[headers[j]] = str(cell).strip() if cell is not None else ''
                    rows.append(row_data)
        else:
            return JsonResponse({'error': 'Chỉ hỗ trợ file .csv hoặc .xlsx'}, status=400)
            
        success_count = 0
        
        def get_val(row_dict, possible_keys, default=''):
            for k in possible_keys:
                if k in row_dict and row_dict[k]:
                    return row_dict[k]
            return default

        for row in rows:
            english = get_val(row, ['english', 'en', 'word', 'từ vựng', 'từ tiếng anh', 'english_word'])
            vietnamese = get_val(row, ['vietnamese', 'vi', 'meaning', 'nghĩa', 'nghĩa tiếng việt', 'vietnamese_meaning'])
            
            if not english or not vietnamese:
                continue
                
            pos = get_val(row, ['pos', 'part of speech', 'loại từ', 'loại', 'part_of_speech'], 'N')
            pron = get_val(row, ['pronunciation', 'pron', 'phiên âm', 'ipa'])
            ex_en = get_val(row, ['example_en', 'example', 'câu ví dụ', 'ví dụ tiếng anh', 'example_sentence'])
            ex_vi = get_val(row, ['example_vi', 'nghĩa ví dụ', 'dịch câu', 'ví dụ tiếng việt', 'example_meaning'])
            topic_name = get_val(row, ['topic', 'chủ đề', 'topic_name'])
            
            topic_obj = None
            if topic_name:
                from django.utils.text import slugify
                slug_val = slugify(topic_name)
                if slug_val:
                    topic_obj, _ = Topic.objects.get_or_create(slug=slug_val, defaults={'name': topic_name})
                
            defaults = {
                'vietnamese_meaning': vietnamese,
                'part_of_speech': pos,
                'pronunciation': pron,
                'example_sentence': ex_en,
                'example_meaning': ex_vi,
                'topic': topic_obj
            }
            
            Word.objects.update_or_create(
                english_word=english,
                defaults=defaults
            )
            success_count += 1
            
        return JsonResponse({'success': True, 'count': success_count})
        
    except Exception as e:
        return JsonResponse({'error': f'Lỗi khi đọc file: {str(e)}'}, status=500)

import requests

@require_POST
def api_check_grammar(request):
    try:
        data = json.loads(request.body)
        sentence = data.get('sentence', '').strip()
        
        if not sentence:
            return JsonResponse({'error': 'Vui lòng nhập câu ví dụ để kiểm tra.'}, status=400)
            
        system_instruction = "Bạn là một chuyên gia ngôn ngữ học tiếng Anh (English Linguist)."
        user_prompt = f"""Nhiệm vụ của bạn là kiểm tra ngữ pháp và độ tự nhiên của câu tiếng Anh sau đây:
"{sentence}"

Hãy trả về kết quả định dạng JSON với cấu trúc chính xác như sau (KHÔNG dùng markdown code block, KHÔNG có text thừa):
{{
    "is_correct": true/false,
    "error_found": "Mô tả lỗi sai ngữ pháp hoặc chính tả bằng tiếng Việt (nếu is_correct=false, nếu đúng thì để trống)",
    "suggestion": "Câu tiếng Anh đã được sửa đổi cho đúng và tự nhiên nhất",
    "explanation": "Giải thích ngắn gọn quy tắc ngữ pháp tại sao lại sửa như vậy bằng tiếng Việt"
}}"""

        try:
            response = requests.post("http://localhost:11434/api/chat", json={
                "model": "vocab-ai",
                "messages": [
                    {"role": "system", "content": system_instruction},
                    {"role": "user", "content": user_prompt}
                ],
                "stream": False,
                "options": {
                    "temperature": 0.1
                }
            }, timeout=30)
            response.raise_for_status()
            result_text = response.json()['message']['content']
        except requests.exceptions.ConnectionError:
            return JsonResponse({'error': 'Không thể kết nối đến AI cục bộ. Vui lòng đảm bảo Ollama đang chạy ở cổng 11434.'}, status=503)
        except Exception as e:
            return JsonResponse({'error': f'Lỗi khi gọi AI cục bộ: {str(e)}'}, status=500)
            
        if result_text.startswith("```json"):
            result_text = result_text[7:-3]
        elif result_text.startswith("```"):
            result_text = result_text[3:-3]
            
        result_json = json.loads(result_text.strip())
        
        return JsonResponse({
            'success': True,
            'data': result_json
        })
    except Exception as e:
        error_str = str(e)
        return JsonResponse({
            'success': False, 
            'error': f'Lỗi hệ thống: {error_str}'
        })

import datetime
import re
from django.http import HttpResponse

@require_POST
def api_generate_vocab_file(request):
    try:
        data = json.loads(request.body)
        user_prompt = data.get('prompt', '').strip()
        
        if not user_prompt:
            return JsonResponse({'error': 'Vui lòng nhập yêu cầu của bạn.'}, status=400)
            
        # 1. Trích xuất số lượng yêu cầu bằng Regex
        match = re.search(r'\d+', user_prompt)
        limit_count = int(match.group()) if match else 50
            
        # 2. Chia nhỏ request thành các batch (tối đa 10 từ/batch)
        batch_size = 10
        chunks = []
        remaining = limit_count
        while remaining > 0:
            if remaining >= batch_size:
                chunks.append(batch_size)
                remaining -= batch_size
            else:
                chunks.append(remaining)
                remaining = 0
                
        all_vocab_list = []
        
        for i, chunk in enumerate(chunks):
            # Thêm phần (part) vào prompt để AI tạo ra các từ khác nhau trong mỗi lần lặp
            system_instruction = f"""Bạn là một chuyên gia giáo dục ngôn ngữ. Hãy tạo danh sách từ vựng tiếng Anh chính xác dựa trên yêu cầu của người dùng.
Yêu cầu người dùng: "{user_prompt} (Phần {i+1})"
Mỗi từ bắt buộc phải có đầy đủ phiên âm IPA, loại từ, nghĩa tiếng Việt, một câu ví dụ tiếng Anh thực tế, nghĩa tiếng Việt của câu ví dụ và tên chủ đề tương ứng.
BẮT BUỘC chỉ tạo đúng số lượng {chunk} từ được yêu cầu, KHÔNG ĐƯỢC tạo thừa hoặc thiếu dù chỉ 1 từ. Đảm bảo các từ sinh ra đa dạng và phong phú.
Trả về dữ liệu dưới dạng JSON là một mảng các object. KHÔNG dùng markdown block.
Cấu trúc mỗi object:
{{
    "english": "từ tiếng Anh",
    "vietnamese": "nghĩa tiếng Việt",
    "pos": "loại từ (N, V, ADJ, ADV, PREP, CONJ)",
    "pronunciation": "phiên âm",
    "example_en": "câu ví dụ tiếng Anh",
    "example_vi": "nghĩa câu ví dụ",
    "topic": "tên chủ đề"
}}"""

            try:
                response = requests.post("http://localhost:11434/api/chat", json={
                    "model": "qwen2.5:7b",
                    "messages": [
                        {"role": "user", "content": system_instruction}
                    ],
                    "stream": False,
                    "options": {
                        "temperature": 0.8,
                        "num_predict": 2048
                    }
                }, timeout=120)
                response.raise_for_status()
                result_text = response.json()['message']['content']
            except requests.exceptions.ConnectionError:
                return JsonResponse({'error': 'Không thể kết nối đến AI cục bộ. Vui lòng đảm bảo Ollama đang chạy ở cổng 11434.'}, status=503)
            except Exception as e:
                return JsonResponse({'error': f'Lỗi khi gọi AI cục bộ: {str(e)}'}, status=500)
                
            # Tìm mảng JSON bằng Regex để loại bỏ text thừa xung quanh
            json_match = re.search(r'\[\s*\{.*\}\s*\]', result_text, re.DOTALL)
            if json_match:
                result_text = json_match.group(0)
            else:
                if result_text.startswith("```json"):
                    result_text = result_text[7:-3]
                elif result_text.startswith("```"):
                    result_text = result_text[3:-3]
                
            try:
                vocab_list = json.loads(result_text.strip())
            except json.JSONDecodeError as e:
                print(f"\n[AI RAW OUTPUT LỖI JSON (Batch {i+1})]\n{result_text}\n[END AI RAW OUTPUT]\n")
                return JsonResponse({'error': f'AI sinh dữ liệu bị đứt đoạn hoặc sai cú pháp JSON ở Batch {i+1} ({str(e)}). Vui lòng kiểm tra Terminal.'}, status=500)
            
            if not isinstance(vocab_list, list):
                return JsonResponse({'error': f'Dữ liệu AI trả về không hợp lệ ở Batch {i+1} (không phải là mảng).'}, status=500)
                
            all_vocab_list.extend(vocab_list)
            
        # 3. Loại bỏ trùng lặp (nếu có) và cắt đủ số lượng
        seen_words = set()
        unique_vocab_list = []
        for v in all_vocab_list:
            word = v.get('english', '').lower().strip()
            if word and word not in seen_words:
                seen_words.add(word)
                unique_vocab_list.append(v)
                
        vocab_list = unique_vocab_list[:limit_count]
            
        output = io.StringIO()
        writer = csv.writer(output)
        
        writer.writerow(['english', 'vietnamese', 'pos', 'pronunciation', 'example_en', 'example_vi', 'topic'])
        
        for vocab in vocab_list:
            writer.writerow([
                vocab.get('english', ''),
                vocab.get('vietnamese', ''),
                vocab.get('pos', ''),
                vocab.get('pronunciation', ''),
                vocab.get('example_en', ''),
                vocab.get('example_vi', ''),
                vocab.get('topic', '')
            ])
            
        csv_content = output.getvalue()
        
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"ai_vocab_{timestamp}.csv"
        
        response = HttpResponse(csv_content.encode('utf-8-sig'), content_type='text/csv')
        response['Content-Disposition'] = f'attachment; filename="{filename}"'
        
        return response
        
    except Exception as e:
        error_msg = str(e)
        return JsonResponse({'error': error_msg}, status=500)
