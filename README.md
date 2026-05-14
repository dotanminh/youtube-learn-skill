# 🏛️ YouTube-Learn: Belief Archaeology

> **An AI Agent skill that goes beyond summarizing YouTube videos - it excavates the hidden worldviews, beliefs, and mental models of speakers.**

![Version](https://img.shields.io/badge/version-2.1.0-blue)
![License](https://img.shields.io/badge/license-MIT-green)
![Platform](https://img.shields.io/badge/platform-Antigravity%20%7C%20Gemini%20CLI-purple)

## 🤔 Why This Exists

Most AI tools **summarize** YouTube videos. Summaries are cheap - anyone can get bullet points.

**Belief Archaeology** is different. It treats each video transcript as an **archaeological site** - the surface content (what the speaker says) is just the topsoil. The real treasure lies underneath: the **worldviews, assumptions, and mental models** that drive everything the speaker does and says.

### Summary vs. Belief Archaeology

| Approach | Output | Depth |
|----------|--------|-------|
| Summary | "Speaker said X, Y, Z" | Surface |
| **Belief Archaeology** | "Speaker **believes** A, which causes them to do X. This belief works when B, fails when C, and you can apply it by doing D." | Deep |

## ✨ Features

- **8-Phase Analysis Pipeline** - structured, repeatable, quality-controlled
- **Auto Transcript Fetching** - supports Vietnamese, English, and 50+ languages via `youtube-transcript-api`
- **Speaker Profiling** - research the person, not just their words
- **Worldview Extraction** - max 3 core beliefs per video, each with 5-point analysis
- **Vault Integration** - cross-reference findings with your existing knowledge base
- **QA Checklist** - 9-point quality gate, no shortcuts allowed

## 📦 Installation

### For Antigravity / Gemini CLI Users

Copy the skill folder to your skills directory:

```bash
# Clone this repo
git clone https://github.com/dotanminh/youtube-learn-skill.git

# Copy to your Antigravity skills directory
# Windows:
xcopy /E /I youtube-learn-skill "%USERPROFILE%\.gemini\antigravity\skills\youtube-learn"

# macOS/Linux:
cp -r youtube-learn-skill ~/.gemini/antigravity/skills/youtube-learn
```

### Install Dependencies

```bash
pip install youtube-transcript-api
```

> Requires `youtube-transcript-api` v1.2.4 or higher.

## 🚀 Usage

### Quick Start

Just share a YouTube link with your AI agent and say:

```
youtube-learn https://www.youtube.com/watch?v=VIDEO_ID
```

Or use natural language triggers:
- "Học sâu video này"
- "Phân tích worldview"
- "Belief archaeology [URL]"

### Configuration

Edit `SKILL.md` to customize paths for your setup:

```yaml
# Where video analysis folders are stored
storage_root: ~/youtube-learn/      # Change to your preferred path

# Your knowledge base index (for Vault Check)
knowledge_index: ~/knowledge/index.md  # Optional - skip Phase 5 if not set
```

### Standalone Script

The transcript fetcher works independently:

```bash
python scripts/fetch_transcript.py https://www.youtube.com/watch?v=VIDEO_ID output.txt
```

## 🔬 The 8-Phase Pipeline

```
Phase 1: Data Collection     → Fetch transcript + metadata
Phase 2: Speaker Portrait    → Research who's talking
Phase 3: Belief Archaeology  → Extract max 3 worldviews (⚡ CORE)
Phase 4: Synthesis           → Compare vs mainstream, find tensions
Phase 5: Vault Check         → Cross-reference with existing knowledge
Phase 6: Reflection          → 3 questions to internalize
Phase 7: Atomize             → Save to structured library
Phase 8: QA Checklist        → 9-point quality gate
```

### Phase 3 Output Format (Core)

Each worldview is analyzed with 5 dimensions:

| Dimension | Description |
|-----------|-------------|
| 📍 Phenomenon | Original quote + specific context |
| 💡 Hidden Belief | One memorable sentence - like a proverb, not philosophy |
| ✅ Works When | 2 concrete examples anyone can understand |
| ❌ Fails When | 1-2 cases where this worldview breaks down |
| 🎯 Apply To Me | 1 specific, actionable suggestion |

## 📂 Output Structure

Each analyzed video creates a structured folder:

```
youtube-learn/
├── _INDEX.md                          ← Master index (auto-updated)
├── YYYY-MM-DD_video-name/
│   ├── analysis.md                    ← Full 8-phase analysis
│   ├── transcript.txt                 ← Raw transcript (always kept)
│   ├── speaker.md                     ← Speaker profile
│   └── worldviews/
│       └── worldview-[name].md        ← One file per worldview
```

## 📋 Templates

Ready-to-use templates in `references/`:

- `speaker_profile_template.md` - Speaker research format
- `worldview_template.md` - Individual worldview analysis card

## 🛠️ Customization

### Adapting for Your Knowledge System

The skill is designed to work with any personal knowledge management system (Obsidian, Notion, P.A.R.A, Zettelkasten, etc.):

1. **Storage root** - Change the output directory in `SKILL.md`
2. **Vault Check** - Point to your knowledge index file, or disable Phase 5
3. **"Apply To Me"** - Replace with your name/context in Phase 3

### Language Support

The transcript fetcher prioritizes:
1. Vietnamese (`vi`)
2. English (`en`)
3. Any available language (fallback)

Modify the language priority in `scripts/fetch_transcript.py` if needed.

## 📄 License

MIT License - see [LICENSE](LICENSE) for details.

## 🙏 Credits

- Transcript fetching powered by [youtube-transcript-api](https://github.com/jdepoix/youtube-transcript-api)
- Belief Archaeology methodology inspired by philosophical hermeneutics and archaeological thinking
- Built for [Google Antigravity](https://blog.google/technology/google-deepmind/introducing-gemini-cli/) AI Agent platform

---

**Made with 🏛️ by [Minh Đỗ](https://zalo.me/g/igkywu632)**
