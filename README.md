# 🏛️ YouTube-Learn: Belief Archaeology

> **Skill dành cho AI Agent - đào sâu worldview (thế giới quan) và niềm tin ẩn của speaker thay vì chỉ tóm tắt nội dung video YouTube.**

![Version](https://img.shields.io/badge/version-2.1.0-blue)
![License](https://img.shields.io/badge/license-MIT-green)
![Platform](https://img.shields.io/badge/platform-Antigravity%20%7C%20Gemini%20CLI-purple)

## 🤔 Tại sao cần skill này?

Hầu hết công cụ AI đều **tóm tắt** video YouTube. Nhưng tóm tắt thì ai cũng làm được - chỉ cần copy bullet points là xong.

**Belief Archaeology** (Khảo cổ Niềm tin) khác hoàn toàn. Nó coi mỗi transcript như một **di chỉ khảo cổ** - nội dung bề mặt (những gì speaker nói) chỉ là lớp đất phủ. Kho báu thực sự nằm bên dưới: **worldview, giả định, và mô hình tư duy** chi phối mọi hành động và lời nói của speaker.

### So sánh: Tóm tắt vs. Belief Archaeology

| Cách tiếp cận | Output | Độ sâu |
|---------------|--------|--------|
| Tóm tắt | "Speaker nói X, Y, Z" | Bề mặt |
| **Belief Archaeology** | "Speaker **tin rằng** A, điều đó khiến họ làm X. Niềm tin này đúng khi B, sai khi C, và bạn có thể áp dụng bằng cách D." | Chiều sâu |

## ✨ Tính năng chính

- **Pipeline 8 Phase** - có cấu trúc, lặp lại được, kiểm soát chất lượng
- **Tự động lấy Transcript** - hỗ trợ tiếng Việt, tiếng Anh, và 50+ ngôn ngữ qua `youtube-transcript-api`
- **Chân dung Speaker** - nghiên cứu CON NGƯỜI, không chỉ lời nói
- **Trích xuất Worldview** - tối đa 3 niềm tin cốt lõi mỗi video, phân tích 5 chiều
- **Đối chiếu Knowledge Base** - so sánh phát hiện mới với kiến thức đã có
- **QA Checklist** - 9 tiêu chí kiểm tra chất lượng, không được bỏ qua

## 📦 Cài đặt

### Dành cho người dùng Antigravity / Gemini CLI

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

### Cài thư viện phụ thuộc

```bash
pip install youtube-transcript-api
```

> Yêu cầu `youtube-transcript-api` phiên bản 1.2.4 trở lên.

## 🚀 Cách sử dụng

### Bắt đầu nhanh

Chia sẻ link YouTube với AI agent và nói:

```
youtube-learn https://www.youtube.com/watch?v=VIDEO_ID
```

Hoặc dùng ngôn ngữ tự nhiên:
- "Học sâu video này"
- "Phân tích worldview"
- "Belief archaeology [URL]"

### Cấu hình

Sửa `SKILL.md` để tùy chỉnh đường dẫn phù hợp với hệ thống của bạn:

```yaml
# Nơi lưu folder phân tích video
storage_root: ~/youtube-learn/      # Đổi thành đường dẫn bạn muốn

# File index knowledge base của bạn (cho bước Vault Check)
knowledge_index: ~/knowledge/index.md  # Tùy chọn - bỏ qua Phase 5 nếu không có
```

### Chạy Script độc lập

Script lấy transcript hoạt động độc lập, không cần AI agent:

```bash
python scripts/fetch_transcript.py https://www.youtube.com/watch?v=VIDEO_ID output.txt
```

## 🔬 Pipeline 8 Phase

```
Phase 1: Thu thập dữ liệu      → Lấy transcript + metadata
Phase 2: Chân dung Speaker      → Nghiên cứu người nói
Phase 3: Belief Archaeology     → Trích xuất tối đa 3 worldviews (⚡ CORE)
Phase 4: Tổng hợp               → So sánh với mainstream, tìm mâu thuẫn
Phase 5: Vault Check             → Đối chiếu với knowledge base hiện có
Phase 6: Câu hỏi suy ngẫm       → 3 câu hỏi để internalize
Phase 7: Atomize                 → Lưu trữ có cấu trúc
Phase 8: QA Checklist            → 9 tiêu chí kiểm tra chất lượng
```

### Format output Phase 3 (Phần cốt lõi)

Mỗi worldview được phân tích theo 5 chiều:

| Chiều phân tích | Mô tả |
|-----------------|-------|
| 📍 Hiện tượng | Quote gốc + bối cảnh cụ thể |
| 💡 Niềm tin ẩn | 1 câu dễ nhớ NHƯ TỤC NGỮ - không phải triết học |
| ✅ Đúng khi | 2 ví dụ cụ thể ai cũng hiểu |
| ❌ Sai khi | 1-2 trường hợp worldview này thất bại |
| 🎯 Áp dụng cho tôi | 1 gợi ý actionable cụ thể nhất |

## 📂 Cấu trúc output

Mỗi video sau khi phân tích sẽ tạo 1 folder có cấu trúc:

```
youtube-learn/
├── _INDEX.md                          ← Bản đồ tổng (tự động cập nhật)
├── YYYY-MM-DD_ten-video/
│   ├── analysis.md                    ← Bản phân tích đầy đủ 8 Phase
│   ├── transcript.txt                 ← Transcript gốc (luôn giữ lại)
│   ├── speaker.md                     ← Chân dung speaker
│   └── worldviews/
│       └── worldview-[ten].md         ← Mỗi worldview 1 file riêng
```

## 📋 Templates có sẵn

Trong thư mục `references/`:

- `speaker_profile_template.md` - Template chân dung speaker
- `worldview_template.md` - Template phân tích worldview

## 🛠️ Tùy chỉnh

### Tương thích với mọi hệ thống quản lý kiến thức

Skill được thiết kế để hoạt động với bất kỳ hệ thống nào (Obsidian, Notion, P.A.R.A, Zettelkasten...):

1. **Storage root** - Đổi thư mục output trong `SKILL.md`
2. **Vault Check** - Trỏ đến file knowledge index của bạn, hoặc tắt Phase 5
3. **"Áp dụng cho tôi"** - Thay tên/bối cảnh của bạn vào Phase 3

### Hỗ trợ ngôn ngữ

Script lấy transcript ưu tiên theo thứ tự:
1. Tiếng Việt (`vi`)
2. Tiếng Anh (`en`)
3. Ngôn ngữ bất kỳ có sẵn (fallback)

Sửa thứ tự ưu tiên trong `scripts/fetch_transcript.py` nếu cần.

## 📄 Giấy phép

MIT License - xem file [LICENSE](LICENSE) để biết chi tiết.

## 🙏 Credits

- Lấy transcript bằng [youtube-transcript-api](https://github.com/jdepoix/youtube-transcript-api)
- Phương pháp Belief Archaeology lấy cảm hứng từ hermeneutics (diễn giải học) và tư duy khảo cổ
- Xây dựng cho nền tảng [Google Antigravity](https://blog.google/technology/google-deepmind/introducing-gemini-cli/) AI Agent

---

**Made with 🏛️ by [Minh Đỗ](https://zalo.me/g/igkywu632)**
