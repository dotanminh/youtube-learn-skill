---
name: youtube-learn
description: Phân tích video (YouTube, LinkedIn, Facebook, X, TikTok) theo hướng Belief Archaeology, kết hợp Multimodal phân tích hình ảnh và thế giới quan của người nói.
version: 3.1.0
status: approved
zone: B
keywords: [youtube, learn, belief, worldview, archaeology, transcript, speaker, multimodal, frames, watch]
created: 2026-05-06
updated: 2026-07-04
---

# YouTube-Learn (Multimodal) - Belief Archaeology

> Triết lý: Em là nhà khảo cổ, không phải máy tóm tắt. Transcript và hình ảnh video = địa tầng bề mặt.
> Thứ cần học là **niềm tin và thế giới quan** tạo ra những hiện tượng đó.

## Dependencies
- `ffmpeg` (Cài đặt sẵn trên hệ thống và có trong PATH)
- `yt-dlp` (pip install yt-dlp)
- `youtube-transcript-api` (pip install youtube-transcript-api)
- Script: `scripts/watch_video.py`
- Yêu cầu một API Key: `KYMA_API_KEY`, `GROQ_API_KEY`, `GEMINI_API_KEY` hoặc `ATLASCLOUD_API_KEY` (để dịch giọng nói thành văn bản cho các video ngoài YouTube). Atlas Cloud là provider tùy chọn cuối cùng và không thay đổi thứ tự provider mặc định.

## When to Use
User chia sẻ link video (YouTube, LinkedIn, Facebook, X, TikTok, Reddit...) và muốn phân tích sâu.
**Trigger:** "youtube-learn [URL]", "học sâu video này", "phân tích worldview", "belief archaeology", "xem video này"

## Procedure

### Phase 1 - Data Collection (Thu thập dữ liệu)
1. Tạo folder video: `D:\1_MINH DO\3_Resources\youtube-learn\YYYY-MM-DD_ten-video-ngan-gon\`
2. Dùng `run_command` chạy script `scripts/watch_video.py` để tải video, trích xuất frames ảnh và transcript:
   ```
   python "<skill_dir>/scripts/watch_video.py" <video_url> "<video_folder>"
   ```
3. Script tự động:
   - Tải âm thanh và video (chất lượng thấp để tối ưu hiệu năng).
   - Dùng `ffmpeg` cắt các khung hình ảnh tĩnh (mặc định `.jpg`) lưu vào thư mục `<video_folder>/frames/`. Số lượng frames **tự động tính theo thời lượng video**:
     - Công thức: `min(max(8, int(thời_lượng_phút x 0.8)), 24)`
     - Sàn tối thiểu: 8 frames (video ngắn dưới 10 phút)
     - Trần tối đa: 24 frames (video dài trên 30 phút)
     - Ví dụ: 20 phút → 16 frames | 30 phút → 24 frames | 60 phút → 24 frames
   - Dùng mô hình Speech-to-Text (Kyma / Groq / Gemini, hoặc Atlas Cloud Seed ASR 2.0 khi cấu hình `ATLASCLOUD_API_KEY`) dịch âm thanh thành transcript. Atlas chỉ gửi một yêu cầu ASR cho mỗi lần chạy và giới hạn retry ở bước GET prediction. Tự động fallback về `youtube-transcript-api` nếu là YouTube để đảm bảo luôn có transcript.
4. Đọc file `<video_folder>/transcript.txt` bằng `view_file` để phân tích văn bản.
5. Kiểm tra xem thư mục `<video_folder>/frames/` có được tạo ra không. Nếu có, hãy dùng `view_file` để xem các ảnh khung hình này để phân tích các yếu tố trực quan (slide, sơ đồ, code, giao diện).

### Phase 2 - Speaker Portrait (Chân dung người chia sẻ)
1. Dùng `search_web` tra cứu speaker: danh tính, thành tựu, quote đặc trưng.
2. Ưu tiên thứ ÍT NGƯỜI BIẾT - không lặp Wikipedia paragraph đầu.
3. Output: tên, top 5 thành tựu, điều khiến họ khác biệt, quote + bản dịch.

### Phase 3 - Belief Archaeology ⚡ (CORE - quan trọng nhất)
Chọn **tối đa 3 worldviews** quan trọng nhất. Mỗi worldview phân tích theo 5 mục:

| Mục | Nội dung |
|-----|----------|
| 📍 Hiện tượng | Quote gốc + bối cảnh cụ thể (kết hợp mô tả hình ảnh hoặc slide từ các ảnh frames nếu có) |
| 💡 Niềm tin ẩn | 1 câu dễ nhớ NHƯ TỤC NGỮ - cái gì phải đúng trong đầu họ thì họ mới nói vậy |
| ✅ Đúng khi | 2 ví dụ cụ thể, học sinh cũng hiểu |
| ❌ Sai khi | 1-2 trường hợp worldview này thất bại |
| 🎯 Áp dụng cho Minh | 1 gợi ý actionable cụ thể nhất |

> **RULE:** 
> - "Niềm tin ẩn" PHẢI viết như tục ngữ, KHÔNG được viết kiểu triết học phức tạp.
> - Nếu video có các ảnh frames, Agent **bắt buộc** phải tích hợp các chi tiết trực quan từ ảnh (như sơ đồ kiến trúc, slide chữ, demo chạy thử) vào phần mô tả "Hiện tượng" và "Ví dụ" để làm phong phú bài phân tích.

### Phase 4 - Synthesis (Tổng hợp)
- Bảng 3 niềm tin cốt lõi của nhân vật.
- So sánh với mainstream: họ nhìn thế giới khác phần đông ở điểm nào?
- Tension nội tại: worldview của họ có mâu thuẫn với chính nó không?

### Phase 5 - Vault Check (Đối chiếu Knowledge Base)
1. Đọc `D:\1_MINH DO\3_Resources\knowledge_index.md`
2. Dùng `grep_search` tìm KI liên quan đến worldviews vừa phân tích
3. Phân loại: 🟢 Củng cố / 🔴 Mâu thuẫn / 🟡 Mở rộng / 🔵 Hoàn toàn mới

### Phase 6 - Câu hỏi suy ngẫm
- Đưa 3 câu hỏi để user internalize.
- Hỏi: worldview nào tâm đắc nhất? Muốn lưu gì vào Worldview Library?

### Phase 7 - Atomize (Lưu trữ)
**Storage root:** `D:\1_MINH DO\3_Resources\youtube-learn\`
**Naming convention:** `YYYY-MM-DD_ten-video-ngan-gon\`

Mỗi video tạo 1 folder riêng chứa TẤT CẢ dữ liệu liên quan:
```
youtube-learn/
├── _INDEX.md                              ← Bản đồ tổng (agent TỰ ĐỘNG cập nhật)
├── YYYY-MM-DD_ten-video/
│   ├── analysis.md                        ← Bản phân tích 8 Phase (Phase 1-6)
│   ├── transcript.txt                     ← Transcript gốc (LUÔN giữ lại)
│   ├── speaker.md                         ← Speaker Profile
│   ├── worldviews/
│   │   └── worldview-[ten-ngan].md        ← Mỗi worldview 1 file
│   └── frames/                            ← Thư mục chứa các khung hình ảnh tĩnh (JPG)
```

- **7A - Speaker Profile:** TỰ ĐỘNG lưu vào `youtube-learn/[video-folder]/speaker.md` - không cần user duyệt. Dùng template: `references/speaker_profile_template.md`
- **7B - Worldview Library:** PHẢI HỎI user trước -> user confirm worldview nào thì mới lưu vào `youtube-learn/[video-folder]/worldviews/worldview-[tên].md`. Dùng template: `references/worldview_template.md`
- **7C - Cập nhật _INDEX.md:** TỰ ĐỘNG thêm entry mới vào cả 3 bảng (Videos, Speakers, Worldviews) trong `youtube-learn/_INDEX.md`

### Phase 8 - QA Checklist
Kiểm tra 10 tiêu chí. Fail bất kỳ mục nào -> quay lại phase đó, KHÔNG bỏ qua:
1. Transcript đầy đủ (không bị cắt giữa chừng)?
2. Speaker Portrait có nguồn xác minh (không bịa)?
3. Mỗi worldview có đủ 5 mục phân tích?
4. "Niềm tin ẩn" viết kiểu tục ngữ (không triết học)?
5. "Đúng khi" có ví dụ cụ thể (không trừu tượng)?
6. "Áp dụng cho Minh" actionable (có thể làm ngay)?
7. Vault Check đã đối chiếu với KI existing?
8. Speaker Profile đã lưu/update?
9. `_INDEX.md` đã được cập nhật (3 bảng: Videos, Speakers, Worldviews)?
10. Đã xem và kết hợp dữ liệu từ các ảnh trong thư mục `frames/` để phân tích trực quan chưa (nếu video có frames)?

## Pitfalls
- **KHÔNG tóm tắt video** - mục đích là đào sâu worldview, không phải summary.
- **KHÔNG viết "Niềm tin ẩn" dài dòng** - phải ngắn gọn như tục ngữ dân gian.
- **KHÔNG bỏ qua QA** - mỗi tiêu chí fail phải quay lại phase tương ứng.
- **KHÔNG lưu Worldview mà chưa được user confirm** (Phase 7B).
- **Speaker Profile được phép auto-save** (Phase 7A) - đây là factual data.
- **KHÔNG lưu rải rác** - tất cả output của 1 video PHẢI nằm trong cùng 1 folder `youtube-learn/[video-folder]/`.
- **KHÔNG quên cập nhật `_INDEX.md`** - đây là bản đồ tra cứu nhanh khi có nhiều video.
- **KHÔNG được bỏ qua các ảnh trong thư mục `frames/`** - nếu ảnh được trích xuất thành công, bắt buộc phải xem chúng để nắm bắt bối cảnh đồ họa (slide, sơ đồ, code).

### ⛔ CRITICAL RULE: P.A.R.A TRƯỚC, ARTIFACT SAU
- **PHẢI** ghi TRỰC TIẾP vào `D:\1_MINH DO\3_Resources\youtube-learn\[video-folder]\analysis.md` TRƯỚC.
- **SAU ĐÓ** tạo artifact (`.gemini/brain/`) làm bản render đẹp để user xem trong conversation.
- Artifact PHẢI có ghi chú đầu file: "Bản gốc lưu tại: [link P.A.R.A]" để user biết nguồn bền vững.
- **KHÔNG BAO GIỜ** chỉ tạo artifact mà không ghi P.A.R.A - artifact là ephemeral, mất khi sang chat mới.
