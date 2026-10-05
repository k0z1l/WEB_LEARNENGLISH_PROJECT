# 🌐 LingoAI - Web Learn English Project

Một ứng dụng Web học tiếng Anh hiện đại được tích hợp Trí tuệ Nhân tạo (AI) chạy **hoàn toàn cục bộ** (Local LLM), không phụ thuộc vào API của bên thứ ba, đảm bảo quyền riêng tư và miễn phí 100%.

## ✨ Tính năng nổi bật
* **Neo-Brutalism UI:** Giao diện tối giản, hiện đại, mang phong cách Y2K và brutalism.
* **Tự động sinh từ vựng (AI Vocab Gen):** Yêu cầu chủ đề bất kỳ, hệ thống sẽ gọi AI (Qwen 7B) sinh ra hàng chục từ vựng kèm ngữ nghĩa, phiên âm và câu ví dụ.
* **Trợ lý Ngữ pháp (Grammar Checker):** Kiểm duyệt câu ví dụ tiếng Anh bằng một mô hình AI chuyên biệt (vocab-ai) được Fine-tune riêng biệt trên 6,000 mẫu câu lỗi.
* **Quản lý học tập:** Dashboard, Flashcard, và hệ thống Quiz thông minh.

## 🧠 Kiến trúc AI (Dual-Model)
Dự án áp dụng mô hình phân luồng để tối ưu hiệu suất và tránh Overfitting:
1. **Base Model (`qwen2.5:7b`):** Chuyên dùng để sinh từ vựng sáng tạo và đa dạng.
2. **Fine-Tuned Model (`vocab-ai`):** Chuyên đóng vai trò biên tập viên bắt lỗi ngữ pháp siêu chuẩn xác.

> Đọc chi tiết về thuật toán Batching, Regex Parsing và quá trình Fine-tune AI tại file [PROJECT_ARCHITECTURE.md](PROJECT_ARCHITECTURE.md).

## 🚀 Hướng dẫn cài đặt

### 1. Yêu cầu hệ thống
* Python 3.10+
* [Ollama](https://ollama.com/) (Để chạy Local AI)

### 2. Cài đặt Backend
```bash
# Clone dự án
git clone https://github.com/TenCuaBan/WEB_LEARNENGLISH_PROJECT.git
cd WEB_LEARNENGLISH_PROJECT

# Cài đặt thư viện
pip install -r requirements.txt

# Chạy server
python manage.py runserver
```

### 3. Cài đặt AI Models
```bash
# Tải model sinh từ vựng
ollama pull qwen2.5:7b

# (Tùy chọn) Model Grammar Checker cần được build từ file GGUF nội bộ.
```

## 📝 License
Dự án được xây dựng cho mục đích học tập và nghiên cứu AI cục bộ.
