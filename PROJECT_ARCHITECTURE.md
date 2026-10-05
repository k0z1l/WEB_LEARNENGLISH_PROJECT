# TÀI LIỆU KIẾN TRÚC & TIẾN ĐỘ DỰ ÁN (WEB_LEARNENGLISH_PROJECT)

## 1. TỔNG QUAN DỰ ÁN
Dự án là một Ứng dụng Web học tiếng Anh sử dụng trí tuệ nhân tạo (AI) chạy hoàn toàn **cục bộ (Local LLM)** thông qua nền tảng Ollama. Dự án đề cao tính riêng tư, không phụ thuộc vào API của bên thứ ba (như OpenAI, Gemini), và có giao diện (UI) theo phong cách hiện đại (Y2K / Neo-brutalism).

---

## 2. KIẾN TRÚC LOGIC CỦA HỆ THỐNG

Dự án áp dụng mô hình **"Dual-Model Architecture" (Kiến trúc chia để trị bằng 2 model AI riêng biệt)** nhằm khắc phục hiện tượng Overfitting của LLM.

### A. Tầng Frontend (Giao diện)
- Nhận lệnh từ người dùng (ví dụ: "Tạo 50 từ chủ đề Office", hoặc "Kiểm tra câu ví dụ này").
- Hiển thị kết quả sinh từ vựng dưới dạng CSV/Bảng và hiển thị phản hồi sửa lỗi ngữ pháp.

### B. Tầng Backend (Django - `core/views.py`)
Đóng vai trò là cầu nối xử lý logic và điều phối tác vụ AI:
1. **Thuật toán Batching (Phân mảnh):** Chia nhỏ yêu cầu tạo từ vựng lớn (ví dụ: 50 từ) thành các đợt nhỏ (10 từ/đợt) để tránh việc LLM bị kiệt sức hoặc cắt đứt (truncate) giữa chừng do giới hạn token.
2. **Thuật toán Trích xuất JSON (Regex Parsing):** Dùng biểu thức chính quy (Regex) `r'\[\s*\{.*\}\s*\]'` để tự động "cắt" lấy đúng mảng dữ liệu JSON, phớt lờ mọi văn bản rườm rà (chatty text) mà AI sinh ra ở đầu/cuối.
3. **Phân luồng Model (Model Routing):**
   - Lệnh sinh từ vựng -> Điều hướng tới Base Model.
   - Lệnh kiểm tra ngữ pháp -> Điều hướng tới Fine-tuned Model.

### C. Tầng AI Engine (Local Ollama)
1. **Sinh Từ Vựng (Vocabulary Generation):** Dùng model **`qwen2.5:7b`** (Base Model).
   - *Lý do:* Model gốc có vốn từ vựng khổng lồ của nhân loại. Không bị đóng khung dữ liệu, đảm bảo từ vựng sinh ra phong phú, không lặp lại.
2. **Kiểm Tra Ngữ Pháp (Grammar Checking):** Dùng model **`vocab-ai`** (Fine-tuned từ Qwen2.5-3B-Instruct).
   - *Ngữ cảnh sử dụng:* Nút "🤖 Check with AI" được nhúng trực tiếp vào tính năng Chỉnh sửa từ vựng (Edit Word). Đóng vai trò là "Biên tập viên" kiểm duyệt lại các câu ví dụ (Example sentence) do AI sinh ra, hoặc kiểm tra xem người dùng tự sửa câu ví dụ có đúng ngữ pháp tiếng Anh hay không.
   - *Lý do:* Model này đã được dạy (Fine-tune) trên 6000 mẫu câu lỗi để bắt chính xác các lỗi ngữ pháp kinh điển và BẮT BUỘC trả về đúng cấu trúc JSON quy định (phát hiện lỗi, gợi ý sửa, giải thích) mà không nói lời thừa.

---

## 3. NHỮNG THỨ ĐÃ LÀM (DONE)

- [x] **Xây dựng Backend & Giao diện:** Hoàn thiện luồng API xử lý dữ liệu và xuất file CSV tại `core/views.py`.
- [x] **Tạo Dữ liệu Đào tạo (Training Dataset):** Viết script `generate_data.py` sinh ra 10.000 mẫu dữ liệu JSONL bao gồm các quy tắc cấu trúc từ vựng và 80+ mẫu lỗi ngữ pháp tiếng Anh.
- [x] **Huấn luyện AI (Fine-Tuning):** Đưa dữ liệu lên Google Colab, dùng thư viện Unsloth (kỹ thuật LoRA) để huấn luyện mô hình Qwen2.5-3B.
- [x] **Tối ưu hóa Huấn luyện:** Theo dõi Loss Curve và quyết định dừng sớm ở 1500 steps (Loss hội tụ ở mức ~0.02) để tránh Overfitting quá nặng.
- [x] **Triển khai Cục bộ (Local Deployment):** Export model đã train thành file `.gguf` (gần 2GB) và import thành công vào hệ thống Ollama nội bộ với tên `vocab-ai`.
- [x] **Khắc phục Lỗi "Quên Thảm Họa" (Catastrophic Forgetting):** Phát hiện lỗi model sinh từ bị kẹt quanh 15 từ do học vẹt lúc train. Xử lý triệt để bằng cách tách đôi kiến trúc (dùng 7B cho sinh từ, 3B cho ngữ pháp).
- [x] **Sửa lỗi Prompt Role:** Đồng bộ cấu trúc vai trò (`System`/`User`) trong API Check Ngữ pháp (`views.py`) cho khớp chuẩn 100% với lúc train để đánh thức trí khôn của AI.

---

## 4. NHỮNG THỨ ĐANG LÀM (IN PROGRESS)

- [ ] **Kiểm thử Thực tế (Live Testing):** Đang trong giai đoạn test song song 2 chức năng trực tiếp trên Web UI.
- [ ] Xác nhận mức độ đa dạng khi sinh khối lượng lớn (ví dụ: yêu cầu sinh 50-100 từ vựng cho một chủ đề khó).
- [ ] Xác nhận khả năng "soi lỗi" của model ngữ pháp khi cố tình nhập các câu sai ngữ pháp phức tạp vào giao diện Example Sentence.

---

## 5. NHỮNG THỨ CHƯA LÀM (TODO / FUTURE WORK)

- [ ] **Mở rộng Tập Dữ Liệu Ngữ Pháp:** Nếu model Grammar V1 (`vocab-ai`) bắt lỗi chưa chuẩn các trường hợp hẹp, cần cập nhật lại file `generate_data.py` (chỉ tập trung sinh thêm các câu sai khó hơn), tạo file `jsonl` mới và đúc thành bản V2.
- [ ] **Tối ưu Hiệu năng API (Latency):** Việc gọi model 7B đôi khi bị chậm tùy vào cấu hình máy cục bộ, cần xem xét các cơ chế Stream/Loading mượt mà hơn trên Frontend.
- [ ] **Mở rộng Tính Năng AI Khác:** Dùng nền tảng có sẵn để phát triển chức năng tạo bài Quiz (Trắc nghiệm), Flashcard tự động, hoặc Chatbot giao tiếp (tránh ảnh hưởng đến dự án Prompt Injection song song).
