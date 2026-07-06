import os
import sys
import re
import json
import subprocess
import shutil
from pathlib import Path

# Cấu hình encoding utf-8 cho console để hiển thị tiếng Việt trên Windows
sys.stdout.reconfigure(encoding='utf-8', errors='replace')

def get_env_key():
    """Lấy các API Key từ biến môi trường."""
    keys = {
        'kyma': os.environ.get('KYMA_API_KEY'),
        'groq': os.environ.get('GROQ_API_KEY'),
        'gemini': os.environ.get('GEMINI_API_KEY') or os.environ.get('GOOGLE_AI_KEY')
    }
    return keys

def extract_video_id(url):
    """Trích xuất ID video từ URL YouTube."""
    patterns = [
        r'(?:v=|\/v\/|youtu\.be\/|\/embed\/|\/live\/)([a-zA-Z0-9_-]{11})',
        r'^([a-zA-Z0-9_-]{11})$'
    ]
    for pattern in patterns:
        match = re.search(pattern, url)
        if match:
            return match.group(1)
    return None

def run_command(cmd):
    """Chạy command dòng lệnh và trả về output, log lỗi nếu có."""
    try:
        result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, encoding='utf-8', errors='replace', shell=True)
        if result.returncode != 0:
            return None, result.stderr
        return result.stdout.strip(), None
    except Exception as e:
        return None, str(e)

def check_dependencies():
    """Kiểm tra ffmpeg và yt-dlp có sẵn không."""
    ffmpeg_exists = shutil.which('ffmpeg') is not None
    if not ffmpeg_exists:
        print("Cảnh báo: Không tìm thấy 'ffmpeg' trong PATH. Việc trích xuất frames ảnh sẽ bị bỏ qua.")
    
    # Kiểm tra yt-dlp có cài đặt trong python chưa
    try:
        import yt_dlp
        yt_dlp_installed = True
    except ImportError:
        yt_dlp_installed = False
        print("Cảnh báo: Chưa cài đặt thư viện python 'yt-dlp'. Sẽ thử gọi qua command-line nếu có sẵn.")
        
    return ffmpeg_exists, yt_dlp_installed

def download_video_and_audio(url, output_dir):
    """Tải video và audio bằng yt-dlp."""
    print(f"Đang phân tích và tải video từ: {url}")
    
    # Tạo thư mục tạm để tải
    temp_dir = Path(output_dir) / "temp"
    temp_dir.mkdir(parents=True, exist_ok=True)
    
    # Đặt tên file video và audio tạm theo template của yt-dlp
    video_temp_tmpl = str(temp_dir / "video.%(ext)s")
    audio_temp_tmpl = str(temp_dir / "audio.%(ext)s")
    
    # Cấu hình headers và args để tránh lỗi HTTP 403 Forbidden của YouTube
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
    }
    
    # Tải video chất lượng thấp để trích xuất frame nhanh và nhẹ
    ydl_opts_video = {
        'format': 'worstvideo[ext=mp4]/mp4/worst[ext=mp4]/worst',
        'outtmpl': video_temp_tmpl,
        'quiet': True,
        'no_warnings': True,
        'http_headers': headers,
        'extractor_args': {
            'youtube': {
                'player_client': ['android', 'web']
            }
        }
    }
    
    ydl_opts_audio = {
        'format': 'bestaudio/best',
        'outtmpl': audio_temp_tmpl,
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '128',
        }],
        'quiet': True,
        'no_warnings': True,
        'http_headers': headers,
        'extractor_args': {
            'youtube': {
                'player_client': ['android', 'web']
            }
        }
    }
    
    try:
        import yt_dlp
        
        # Lấy thông tin video trước
        with yt_dlp.YoutubeDL({'quiet': True}) as ydl:
            info = ydl.extract_info(url, download=False)
            title = info.get('title', 'Unknown')
            channel = info.get('uploader', info.get('channel', 'Unknown'))
            duration = info.get('duration', 0)
            
        print(f"Tiêu đề: {title}")
        print(f"Kênh: {channel}")
        print(f"Thời lượng: {duration} giây")
        
        # Tải video
        print("Đang tải video...")
        with yt_dlp.YoutubeDL(ydl_opts_video) as ydl:
            ydl.download([url])
            
        # Tải audio
        print("Đang tải âm thanh...")
        with yt_dlp.YoutubeDL(ydl_opts_audio) as ydl:
            ydl.download([url])
            
        # Tìm file thực tế được tải
        all_files = [p.name for p in temp_dir.glob('*')]
        print(f"Các file tải về trong thư mục tạm: {all_files}")
        
        downloaded_video = None
        for p in temp_dir.glob("video.*"):
            if p.suffix.lower() in ['.mp4', '.mkv', '.webm', '.flv']:
                downloaded_video = p
                break
                
        downloaded_audio = None
        for p in temp_dir.glob("audio.*"):
            if p.suffix.lower() in ['.mp3', '.m4a', '.wav', '.ogg']:
                downloaded_audio = p
                break
                
        return {
            'title': title,
            'channel': channel,
            'duration': duration,
            'video_path': downloaded_video,
            'audio_path': downloaded_audio,
            'success': True
        }
    except Exception as e:
        return {'success': False, 'error': str(e)}

def extract_frames(video_path, duration, output_dir, count=8):
    """Trích xuất N frame ảnh tĩnh từ video bằng ffmpeg."""
    if not video_path or not os.path.exists(video_path):
        print("Không tìm thấy file video để trích xuất frames.")
        return []
        
    print(f"Đang trích xuất {count} frames từ video...")
    frames_dir = Path(output_dir) / "frames"
    frames_dir.mkdir(parents=True, exist_ok=True)
    
    # Tính toán các mốc thời gian để cắt ảnh
    # Tránh giây thứ 0 và giây cuối cùng để tránh màn hình đen
    if duration <= 10:
        times = [i * (duration / (count + 1)) for i in range(1, count + 1)]
    else:
        # Cắt trong khoảng từ 5% đến 95% thời lượng video
        start_sec = duration * 0.05
        end_sec = duration * 0.95
        step = (end_sec - start_sec) / (count - 1) if count > 1 else 0
        times = [start_sec + i * step for i in range(count)]
        
    extracted_files = []
    for i, t in enumerate(times):
        frame_path = frames_dir / f"frame_{i+1:02d}.jpg"
        # Lệnh ffmpeg trích xuất nhanh bằng cách dùng -ss trước -i
        cmd = f'ffmpeg -y -ss {t:.2f} -i "{video_path}" -vframes 1 -q:v 2 "{frame_path}"'
        stdout, stderr = run_command(cmd)
        if os.path.exists(frame_path):
            extracted_files.append(str(frame_path))
            
    print(f"Đã trích xuất thành công {len(extracted_files)} frames ảnh vào thư mục {frames_dir}")
    return extracted_files

def transcribe_audio_api(audio_path, keys):
    """Dịch âm thanh thành văn bản qua các API dịch vụ."""
    if not audio_path or not os.path.exists(audio_path):
        return None, "Không tìm thấy file âm thanh để transcribe."
        
    import requests
    
    # 1. Thử Kyma API
    if keys['kyma']:
        print("Đang dịch âm thanh bằng Kyma API...")
        url = "https://api.kymaapi.com/v1/audio/transcriptions"
        headers = {"Authorization": f"Bearer {keys['kyma']}"}
        try:
            with open(audio_path, 'rb') as f:
                files = {
                    'file': (os.path.basename(audio_path), f, 'audio/mpeg'),
                    'model': (None, 'whisper-1')
                }
                response = requests.post(url, headers=headers, files=files, timeout=120)
                if response.status_code == 200:
                    return response.json().get('text'), None
                else:
                    print(f"Kyma API lỗi (Status {response.status_code}): {response.text}")
        except Exception as e:
            print(f"Lỗi khi gọi Kyma API: {e}")
            
    # 2. Thử Groq API
    if keys['groq']:
        print("Đang dịch âm thanh bằng Groq API...")
        url = "https://api.groq.com/openai/v1/audio/transcriptions"
        headers = {"Authorization": f"Bearer {keys['groq']}"}
        try:
            with open(audio_path, 'rb') as f:
                files = {
                    'file': (os.path.basename(audio_path), f, 'audio/mpeg'),
                    'model': (None, 'whisper-large-v3-turbo')
                }
                response = requests.post(url, headers=headers, files=files, timeout=120)
                if response.status_code == 200:
                    return response.json().get('text'), None
                else:
                    print(f"Groq API lỗi (Status {response.status_code}): {response.text}")
        except Exception as e:
            print(f"Lỗi khi gọi Groq API: {e}")
            
    # 3. Thử Gemini API (Upload file audio và dùng model Gemini Flash)
    if keys['gemini']:
        print("Đang dịch âm thanh bằng Gemini API...")
        try:
            import google.generativeai as genai
            genai.configure(api_key=keys['gemini'])
            
            # Upload file
            print("Đang tải file audio lên Gemini...")
            audio_file = genai.upload_file(path=audio_path)
            print(f"Đã tải lên thành công: {audio_file.name}")
            
            # Sử dụng gemini-1.5-flash để trích xuất transcript
            model = genai.GenerativeModel("gemini-1.5-flash")
            prompt = "Hãy dịch và ghi lại toàn bộ nội dung giọng nói từ file âm thanh này thành văn bản transcript hoàn chỉnh, giữ nguyên ngôn ngữ gốc (ưu tiên tiếng Việt/tiếng Anh) và không thêm bớt bình luận."
            response = model.generate_content([audio_file, prompt])
            
            # Xóa file sau khi xử lý
            try:
                genai.delete_file(name=audio_file.name)
            except Exception:
                pass
                
            return response.text, None
        except Exception as e:
            print(f"Lỗi khi gọi Gemini API: {e}")
            
    return None, "Không có API key hợp lệ hoặc tất cả dịch vụ API đều gặp lỗi."

def get_youtube_transcript_fallback(video_id):
    """Fallback lấy phụ đề YouTube miễn phí qua youtube-transcript-api."""
    print("Đang chạy fallback lấy phụ đề YouTube gốc...")
    try:
        from youtube_transcript_api import YouTubeTranscriptApi
        api = YouTubeTranscriptApi()
        # Thử tiếng Việt trước, sau đó tiếng Anh
        try:
            transcript = api.fetch(video_id, languages=['vi', 'en'])
        except Exception:
            # Lấy phụ đề đầu tiên có sẵn
            transcript_list = api.list(video_id)
            first = next(iter(transcript_list))
            transcript = first.fetch()
            
        full_text = ' '.join([entry['text'] if isinstance(entry, dict) else entry.text for entry in transcript])
        return full_text, None
    except Exception as e:
        return None, str(e)

def main():
    if len(sys.argv) < 3:
        print("Sử dụng: python watch_video.py <URL_video> <Thư_mục_đầu_ra>")
        sys.exit(1)
        
    url = sys.argv[1]
    output_dir = sys.argv[2]
    
    # Tạo thư mục đầu ra
    Path(output_dir).mkdir(parents=True, exist_ok=True)
    
    # Kiểm tra công cụ hệ thống
    ffmpeg_exists, yt_dlp_installed = check_dependencies()
    
    # Lấy các API Key
    keys = get_env_key()
    
    # 1. Tải video và audio
    dl_result = download_video_and_audio(url, output_dir)
    if not dl_result['success']:
        print(f"Lỗi khi tải video: {dl_result.get('error')}")
        # Nếu là YouTube, thử dùng youtube-transcript-api lấy trực tiếp không cần tải
        video_id = extract_video_id(url)
        if video_id:
            text, err = get_youtube_transcript_fallback(video_id)
            if text:
                print("Lấy transcript thành công qua YouTube Transcript API (Fallback).")
                with open(Path(output_dir) / "transcript.txt", "w", encoding="utf-8") as f:
                    f.write(text)
                sys.exit(0)
        sys.exit(1)
        
    # 2. Tính số frames động theo thời lượng video
    # Công thức: min(max(8, int(duration_phút * 0.8)), 24)
    # Ví dụ: 10 phút → 8, 20 phút → 16, 30 phút → 24, 60 phút → 24 (trần)
    duration_minutes = dl_result['duration'] / 60
    dynamic_frame_count = min(max(8, int(duration_minutes * 0.8)), 24)
    
    # Cắt ảnh bằng ffmpeg nếu có
    actual_frames_extracted = 0
    if ffmpeg_exists and dl_result['video_path']:
        print(f"Thời lượng: {duration_minutes:.1f} phút → Sẽ trích xuất {dynamic_frame_count} frames ảnh.")
        extracted = extract_frames(
            video_path=dl_result['video_path'],
            duration=dl_result['duration'],
            output_dir=output_dir,
            count=dynamic_frame_count
        )
        actual_frames_extracted = len(extracted)
        
    # 3. Transcribe audio sang transcript
    transcript_text = None
    transcribe_error = None
    
    # Thử dịch qua API trước
    if any(keys.values()):
        transcript_text, transcribe_error = transcribe_audio_api(dl_result['audio_path'], keys)
        
    # Nếu API lỗi hoặc không có API key, thử fallback cho YouTube
    if not transcript_text:
        video_id = extract_video_id(url)
        if video_id:
            transcript_text, fallback_error = get_youtube_transcript_fallback(video_id)
            if fallback_error:
                transcribe_error = f"API Error: {transcribe_error}. Fallback Error: {fallback_error}"
        else:
            transcribe_error = transcribe_error or "Không có API key để dịch video từ nguồn này."
            
    # Lưu transcript
    if transcript_text:
        transcript_path = Path(output_dir) / "transcript.txt"
        with open(transcript_path, "w", encoding="utf-8") as f:
            f.write(transcript_text)
        print(f"Đã lưu transcript vào: {transcript_path}")
    else:
        print(f"Lỗi dịch âm thanh: {transcribe_error}")
        
    # Dọn dẹp thư mục tạm
    temp_dir = Path(output_dir) / "temp"
    if temp_dir.exists():
        try:
            shutil.rmtree(temp_dir, ignore_errors=True)
        except Exception as e:
            print(f"Cảnh báo: Không thể xóa thư mục tạm '{temp_dir}': {e}")
        
    # Trả về kết quả JSON để Agent dễ phân tích nếu cần
    result_summary = {
        'title': dl_result['title'],
        'channel': dl_result['channel'],
        'duration': dl_result['duration'],
        'has_transcript': transcript_text is not None,
        'frames_count': actual_frames_extracted
    }
    print(f"WATCH_RESULT_JSON: {json.dumps(result_summary)}")

if __name__ == "__main__":
    main()
