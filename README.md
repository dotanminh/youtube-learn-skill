# 🏛️ YouTube-Learn: Multimodal Belief Archaeology

> **Skill dành cho AI Agent - đào sâu thế giới quan (worldview), niềm tin ẩn và trực quan slide bài giảng của speaker thay vì chỉ tóm tắt nội dung video YouTube.**

![Version](https://img.shields.io/badge/version-4.0.0-blue)
![License](https://img.shields.io/badge/license-MIT-green)
![Platform](https://img.shields.io/badge/platform-Antigravity%20%7C%20Gemini%20CLI-purple)

## 🤔 Tại sao cần skill này?

Hầu hết công cụ AI đều **tóm tắt** video YouTube. Nhưng tóm tắt thì ai cũng làm được - chỉ cần copy bullet points là xong.

**Belief Archaeology** (Khảo cổ Niềm tin) khác hoàn toàn. Nó coi mỗi transcript và khung hình slide như một **di chỉ khảo cổ** - nội dung bề mặt chỉ là lớp đất phủ. Kho báu thực sự nằm bên dưới: **worldview, giả định, và mô hình tư duy** chi phối mọi hành động và lời nói của speaker.

---

## ✨ Tính năng mới trên Phiên bản 4.0.0

- **Phân tích Đa phương tiện (Multimodal Analysis):** Tự động tải video chất lượng tối ưu và cắt các khung hình tĩnh (frames) chia đều theo thời lượng để AI Agent có thể trực tiếp quan sát và đọc chữ trên các slide bài giảng.
- **Quản lý Speaker Profile tập trung:** Chuyển đổi từ cấu trúc file `speaker.md` cục bộ trong từng video sang quản lý tập trung tại thư mục `speakers/` dùng chung, giúp tích lũy và cập nhật thông tin người chia sẻ xuyên suốt nhiều video.
- **QA Tự động hóa (Automated Quality Gate):** Tích hợp script `verify_output.py` kiểm tra cấu trúc thư mục, tệp tin bắt buộc, sự nhất quán của bảng chỉ mục index và đối chiếu thực tế thay vì để Agent tự đánh giá cảm tính.
- **Tối ưu hóa YouTube Live:** Hỗ trợ nhận diện và xử lý các đường dẫn dạng phát trực tiếp (YouTube Live).

---

## 📦 Yêu cầu & Cài đặt

### 1. Công cụ hệ thống
Skill yêu cầu các công cụ xử lý media sau được cài đặt và thêm vào biến môi trường hệ thống (`PATH`):
- [yt-dlp](https://github.com/yt-dlp/yt-dlp) - Tải video/audio từ YouTube.
- [ffmpeg](https://ffmpeg.org/) - Trích xuất các khung hình tĩnh từ video.

### 2. Dành cho người dùng Antigravity / Gemini CLI
Copy folder skill vào thư mục skills:

```bash
# Clone repo này
git clone https://github.com/dotanminh/youtube-learn-skill.git

# Copy vào thư mục skills của Antigravity
# Windows:
xcopy /E /I youtube-learn-skill "%USERPROFILE%\.gemini\antigravity\skills\youtube-learn"

# macOS/Linux:
cp -r youtube-learn-skill ~/.gemini/antigravity/skills/youtube-learn
```

### 3. Cài đặt các thư viện Python
```bash
pip install -r resources/requirements.txt
```

---

## 🚀 Cách sử dụng

### Bắt đầu nhanh
Chia sẻ link YouTube với AI agent và nói:
```
youtube-learn https://www.youtube.com/watch?v=VIDEO_ID
```
Hoặc dùng ngôn ngữ tự nhiên:
- "Học sâu video này"
- "Phân tích thế giới quan video [URL]"
- "Chạy belief archaeology [URL]"

### Chạy Script độc lập
Tải video/audio, transcript và tự động cắt frames không cần thông qua AI Agent:
```bash
python scripts/watch_video.py https://www.youtube.com/watch?v=VIDEO_ID output_directory
```

Kiểm tra chất lượng và QA tệp tin đầu ra:
```bash
python scripts/verify_output.py output_directory --fix
```

---

## 🔬 Pipeline 8 Phase

```
Phase 1: Thu thập dữ liệu      → Tải transcript + video + cắt 8-24 frames
Phase 2: Chân dung Speaker      → Nghiên cứu người nói, cập nhật profile trung tâm ở speakers/
Phase 3: Belief Archaeology     → Trích xuất tối đa 3 worldviews (⚡ CORE)
Phase 4: Tổng hợp               → So sánh với mainstream, tìm mâu thuẫn ngầm (tension)
Phase 5: Vault Check             → Đối chiếu với tri thức hiện có trong Second Brain
Phase 6: Câu hỏi suy ngẫm       → 3 câu hỏi phản tư để người dùng chiêm nghiệm
Phase 7: Lưu trữ (Atomize)      → Lưu trữ cấu trúc markdown, cập nhật _INDEX.md
Phase 8: QA Checklist            → Chạy verify_output.py kiểm duyệt chất lượng nghiêm ngặt
```

---

## 📂 Cấu trúc Lưu trữ

Mỗi video sau khi phân tích sẽ được lưu trữ gọn gàng theo chuẩn P.A.R.A:

```
youtube-learn/
├── _INDEX.md                          ← Bản đồ tổng các video & worldviews
├── speakers/
│   └── thanh-tran-5-phut-ai.md        ← Profile trung tâm của từng speaker
├── YYYY-MM-DD_ten-video/
│   ├── analysis.md                    ← File phân tích chi tiết 8 Phase
│   ├── transcript.txt                 ← Phụ đề/transcript gốc của video
│   ├── frames/
│   │   ├── frame_01.jpg               ← Ảnh cắt slide bài giảng
│   │   └── ...
│   └── worldviews/
│       └── worldview-[ten].md         ← Mỗi worldview lưu 1 file riêng biệt
```

---

## 📋 Templates có sẵn
Các mẫu tài liệu chuẩn hóa nằm trong thư mục `references/`:
- `speaker_profile_template.md` - Mẫu chân dung người chia sẻ.
- `worldview_template.md` - Mẫu phân tích thế giới quan 5 chiều (Hiện tượng, Niềm tin ẩn, Đúng khi, Sai khi, Áp dụng cho tôi).

---

## 📄 Giấy phép
MIT License - xem file [LICENSE](LICENSE) để biết chi tiết.

## 🙏 Lời cảm ơn
- Tải transcript bằng [youtube-transcript-api](https://github.com/jdepoix/youtube-transcript-api) và [yt-dlp](https://github.com/yt-dlp/yt-dlp).
- Xây dựng tối ưu cho nền tảng [Google Antigravity](https://blog.google/technology/google-deepmind/introducing-gemini-cli/) AI Agent.

---

**Cung cấp bởi 🏛️ [Minh Đỗ](https://zalo.me/g/igkywu632)**
