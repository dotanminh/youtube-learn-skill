"""
verify_output.py - youtube-learn skill (v4.0)

QA tu dong cho Phase 8: kiem tra output cua 1 video folder + tinh nhat quan cua _INDEX.md.
Thay the viec agent "tu cham diem" bang kiem tra co bang chung.

Su dung:
  python verify_output.py <video_folder> [--fix]

  --fix : tu dong xoa thu muc temp/ sot lai (khong sua gi khac).

Exit code: 0 = tat ca PASS (co the co WARN), 1 = co it nhat 1 FAIL.
"""
import os
import re
import sys
import json
import shutil
from pathlib import Path

sys.stdout.reconfigure(encoding='utf-8', errors='replace')

FOLDER_PATTERN = re.compile(r'^\d{4}-\d{2}-\d{2}_[a-z0-9][a-z0-9-]*$')
RAW_ID_PATTERN = re.compile(r'^\d{4}-\d{2}-\d{2}_[A-Za-z0-9_-]{11}$')

results = {'pass': 0, 'warn': 0, 'fail': 0}


def report(level, msg):
    icon = {'pass': 'PASS', 'warn': 'WARN', 'fail': 'FAIL'}[level]
    results[level] += 1
    print(f"[{icon}] {msg}")


def check_naming(folder: Path):
    name = folder.name
    if RAW_ID_PATTERN.match(name) and '-' not in name.split('_', 1)[1]:
        report('fail', f"Ten folder '{name}' la raw video ID - phai dat ten kebab tu tieu de video.")
    elif FOLDER_PATTERN.match(name):
        report('pass', f"Ten folder dung chuan: {name}")
    else:
        report('fail', f"Ten folder '{name}' khong theo chuan 'YYYY-MM-DD_ten-video-kebab' (chu thuong, gach ngang).")


def check_required_files(folder: Path):
    for fname in ('analysis.md', 'transcript.txt'):
        path = folder / fname
        if path.exists() and path.stat().st_size > 0:
            report('pass', f"{fname} ton tai ({path.stat().st_size:,} bytes)")
        else:
            report('fail', f"Thieu file bat buoc: {fname}")


def check_transcript_quality(folder: Path):
    path = folder / 'transcript.txt'
    if not path.exists():
        return
    text = path.read_text(encoding='utf-8', errors='replace')
    if len(text.split()) < 50:
        report('warn', "transcript.txt qua ngan (<50 tu) - kiem tra lai viec transcribe.")
    if re.search(r'\[\d{1,2}:\d{2}(:\d{2})?\]', text):
        report('pass', "Transcript co timestamp [MM:SS] - doi chieu duoc voi frames.")
    else:
        report('warn', "Transcript KHONG co timestamp - nen chay lai watch_video.py ban moi.")


def check_frames(folder: Path):
    frames_dir = folder / 'frames'
    if not frames_dir.exists():
        report('warn', "Khong co thu muc frames/ (chap nhan neu video khong tai duoc, chi co transcript).")
        return
    jpgs = list(frames_dir.glob('*.jpg'))
    if jpgs:
        report('pass', f"frames/ co {len(jpgs)} anh.")
    else:
        report('warn', "frames/ ton tai nhung rong.")
    if (frames_dir / 'frames_info.json').exists():
        report('pass', "frames_info.json ton tai (map frame -> timestamp).")


def check_worldviews(folder: Path):
    wv_dir = folder / 'worldviews'
    if not wv_dir.exists():
        report('warn', "Chua co thu muc worldviews/ (co the user chua confirm - Phase 7B).")
        return
    files = list(wv_dir.glob('worldview-*.md'))
    if files:
        report('pass', f"worldviews/ co {len(files)} file.")
    else:
        report('warn', "worldviews/ rong - user chua confirm worldview nao? (Phase 7B)")


def check_analysis_content(folder: Path):
    path = folder / 'analysis.md'
    if not path.exists():
        return
    text = path.read_text(encoding='utf-8', errors='replace')
    checks = [
        ('Niềm tin ẩn', "analysis.md co muc 'Niem tin an'"),
        ('Áp dụng cho Minh', "analysis.md co muc 'Ap dung cho Minh'"),
    ]
    for needle, label in checks:
        if needle in text:
            report('pass', label)
        else:
            report('warn', f"{label} - KHONG tim thay, kiem tra lai Phase 3.")


def check_speaker_profile(folder: Path, root: Path):
    speakers_dir = root / 'speakers'
    folder_name = folder.name
    central_hit = None
    if speakers_dir.exists():
        for f in speakers_dir.glob('*.md'):
            try:
                if folder_name in f.read_text(encoding='utf-8', errors='replace'):
                    central_hit = f
                    break
            except Exception:
                continue
    if central_hit:
        report('pass', f"Speaker profile trung tam da lien ket video nay: speakers/{central_hit.name}")
    elif (folder / 'speaker.md').exists():
        report('warn', "Chi co speaker.md trong folder video - nen cap nhat profile trung tam o speakers/ (Phase 7A).")
    else:
        report('fail', "Khong tim thay speaker profile (ca speakers/ lan speaker.md trong folder).")


def check_temp_leftover(folder: Path, fix: bool):
    temp_dir = folder / 'temp'
    if temp_dir.exists():
        if fix:
            shutil.rmtree(temp_dir, ignore_errors=True)
            if temp_dir.exists():
                report('warn', "temp/ sot lai va KHONG xoa duoc (file lock?) - xoa thu cong.")
            else:
                report('pass', "temp/ sot lai da duoc xoa (--fix).")
        else:
            report('warn', "temp/ sot lai - chay voi --fix de xoa.")
    else:
        report('pass', "Khong co thu muc temp/ sot lai.")


def check_index(folder: Path, root: Path):
    index_path = root / '_INDEX.md'
    if not index_path.exists():
        report('fail', "_INDEX.md khong ton tai o storage root.")
        return
    text = index_path.read_text(encoding='utf-8', errors='replace')
    if folder.name in text:
        report('pass', "_INDEX.md da co entry cho video nay.")
    else:
        report('fail', "_INDEX.md CHUA co entry cho video nay (Phase 7C).")

    # Doi chieu 'Total videos' voi so folder thuc te
    actual = len([d for d in root.iterdir()
                  if d.is_dir() and re.match(r'^\d{4}-\d{2}-\d{2}_', d.name)])
    m = re.search(r'\*\*Total videos:\*\*\s*(\d+)', text)
    if m:
        declared = int(m.group(1))
        if declared == actual:
            report('pass', f"Total videos khop: {actual}.")
        else:
            report('fail', f"Total videos lech: _INDEX.md ghi {declared}, thuc te co {actual} folder.")
    else:
        report('warn', "_INDEX.md khong co dong '**Total videos:**' de doi chieu.")


def main():
    if len(sys.argv) < 2:
        print("Su dung: python verify_output.py <video_folder> [--fix]")
        sys.exit(1)

    folder = Path(sys.argv[1]).resolve()
    fix = '--fix' in sys.argv[2:]

    if not folder.is_dir():
        print(f"Loi: khong tim thay folder '{folder}'")
        sys.exit(1)

    root = folder.parent
    print(f"=== QA verify: {folder.name} ===\n")

    check_naming(folder)
    check_required_files(folder)
    check_transcript_quality(folder)
    check_frames(folder)
    check_worldviews(folder)
    check_analysis_content(folder)
    check_speaker_profile(folder, root)
    check_temp_leftover(folder, fix)
    check_index(folder, root)

    print(f"\n=== Ket qua: {results['pass']} PASS | {results['warn']} WARN | {results['fail']} FAIL ===")
    if results['fail']:
        print("Co muc FAIL - agent PHAI quay lai phase tuong ung truoc khi ket thuc (xem SKILL.md Phase 8).")
        sys.exit(1)
    sys.exit(0)


if __name__ == "__main__":
    main()
