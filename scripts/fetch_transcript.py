"""
YouTube Transcript Fetcher - youtube-learn skill
Requires: pip install youtube-transcript-api
Compatible: youtube-transcript-api v1.2.4+

Usage:
  python fetch_transcript.py <video_id_or_url> [output_file]

Examples:
  python fetch_transcript.py dQw4w9WgXcQ
  python fetch_transcript.py https://www.youtube.com/watch?v=dQw4w9WgXcQ transcript.txt
  python fetch_transcript.py https://youtu.be/dQw4w9WgXcQ output/transcript.txt
"""
import urllib.request
import re
import sys
import json
from youtube_transcript_api import YouTubeTranscriptApi

# Fix Windows console encoding for Vietnamese/Unicode output
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')


def extract_video_id(input_str):
    """Extract video ID from URL or return as-is if already an ID."""
    patterns = [
        r'(?:v=|\/v\/|youtu\.be\/|\/embed\/)([a-zA-Z0-9_-]{11})',
        r'^([a-zA-Z0-9_-]{11})$'
    ]
    for pattern in patterns:
        match = re.search(pattern, input_str)
        if match:
            return match.group(1)
    return None


def get_metadata(video_id):
    """Fetch video title and channel from YouTube page."""
    url = f"https://www.youtube.com/watch?v={video_id}"
    try:
        html = urllib.request.urlopen(url).read().decode('utf-8')
        title_match = re.search(r'<title>(.*?)</title>', html)
        title = title_match.group(1).replace(' - YouTube', '') if title_match else 'Unknown'
        channel_match = re.search(r'"ownerChannelName":"(.*?)"', html)
        channel = channel_match.group(1) if channel_match else 'Unknown'
        return {'title': title, 'channel': channel, 'video_id': video_id}
    except Exception as e:
        return {'title': 'Unknown', 'channel': 'Unknown', 'video_id': video_id, 'error': str(e)}


def fetch_transcript(video_id, output_file=None):
    """Fetch transcript using youtube-transcript-api v1.2.4+ API."""
    api = YouTubeTranscriptApi()
    lang_used = None

    # Try Vietnamese first, then English
    try:
        transcript = api.fetch(video_id, languages=['vi', 'en'])
        lang_used = 'vi/en (auto-selected)'
    except Exception:
        # Fallback: list all available and pick first
        try:
            transcript_list = api.list(video_id)
            available = []
            for t in transcript_list:
                available.append(f"{t.language} ({t.language_code})")
            print(f"Available languages: {', '.join(available)}")
            first = next(iter(transcript_list))
            transcript = first.fetch()
            lang_used = first.language_code
        except Exception as e:
            return {'error': str(e), 'transcript': None}

    # Build full text
    full_text = ' '.join([entry.text for entry in transcript])

    # Save to file if specified
    if output_file:
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(full_text)

    return {
        'transcript': full_text,
        'entries': len(transcript),
        'words': len(full_text.split()),
        'language': lang_used,
        'output_file': output_file
    }


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python fetch_transcript.py <video_id_or_url> [output_file]")
        sys.exit(1)

    video_id = extract_video_id(sys.argv[1])
    if not video_id:
        print(f"Error: Cannot extract video ID from '{sys.argv[1]}'")
        sys.exit(1)

    output_file = sys.argv[2] if len(sys.argv) > 2 else 'transcript.txt'

    print(f"Video: https://youtube.com/watch?v={video_id}")

    meta = get_metadata(video_id)
    print(f"Title: {meta['title']}")
    print(f"Channel: {meta['channel']}")

    result = fetch_transcript(video_id, output_file)
    if result.get('error'):
        print(f"Error: {result['error']}")
        sys.exit(1)

    print(f"Language: {result['language']}")
    print(f"Entries: {result['entries']} | Words: {result['words']}")
    print(f"Saved to: {result['output_file']}")
