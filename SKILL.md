---
name: youtube-learn
description: Analyze YouTube videos through Belief Archaeology - excavate hidden worldviews and beliefs instead of summarizing content. Trigger when user shares a YouTube link and wants deep learning.
version: 2.1.0
keywords: [youtube, learn, belief, worldview, archaeology, transcript, speaker]
created: 2026-05-06
updated: 2026-05-14
---

# YouTube-Learn - Belief Archaeology

> Philosophy: You are an archaeologist, not a summarizer. Transcript = surface layer.
> What we need to learn are the **beliefs and worldviews** that produce those phenomena.

## Dependencies
- `youtube-transcript-api` (pip install youtube-transcript-api) - v1.2.4+
- Script: `scripts/fetch_transcript.py`

## Configuration

Customize these paths in your environment before using:

```
STORAGE_ROOT = ~/youtube-learn/              # Where video analysis folders are stored
KNOWLEDGE_INDEX = ~/knowledge/index.md       # Your knowledge base index (for Vault Check, optional)
```

## When to Use
User shares a YouTube link and wants deep analysis - not just a summary.
**Trigger:** "youtube-learn [URL]", "deep learn this video", "analyze worldview", "belief archaeology"

## Procedure

### Phase 1 - Data Collection
1. Create video folder: `<STORAGE_ROOT>/YYYY-MM-DD_short-video-name/`
2. Use `run_command` to execute the transcript script:
   ```
   python "<skill_dir>/scripts/fetch_transcript.py" <video_id_or_url> "<video_folder>/transcript.txt"
   ```
3. Script auto-handles: extract video ID from URL, fetch title + channel, get transcript
4. Language priority: Vietnamese -> English -> any available language
5. Read saved `transcript.txt` file using `view_file` for analysis
6. If script returns error (no transcript) -> inform user, ask if they want to analyze from description
7. **DO NOT use browser_subagent** - API script is faster and more stable
8. **Transcript MUST be saved in the video folder** (not in scratch or artifact dirs)

### Phase 2 - Speaker Portrait
1. Use `search_web` to research speaker: identity, achievements, signature quotes
2. Prioritize LESSER-KNOWN facts - don't repeat Wikipedia's first paragraph
3. Output: name, top 5 achievements, what makes them different, quote + translation

### Phase 3 - Belief Archaeology ⚡ (CORE - most important)
Select **maximum 3 worldviews** that matter most. Analyze each with 5 dimensions:

| Dimension | Content |
|-----------|---------|
| 📍 Phenomenon | Original quote + specific context |
| 💡 Hidden Belief | 1 memorable sentence LIKE A PROVERB - what must be true in their mind for them to say this |
| ✅ Works When | 2 concrete examples anyone can understand |
| ❌ Fails When | 1-2 cases where this worldview breaks down |
| 🎯 Apply To Me | 1 most specific actionable suggestion |

> **RULE:** "Hidden Belief" MUST read like a proverb, NOT complex philosophy.

### Phase 4 - Synthesis
- Table of 3 core beliefs
- Compare vs mainstream: how do they see the world differently from most people?
- Internal tension: do their worldviews contradict each other?

### Phase 5 - Vault Check (Cross-reference Knowledge Base)
1. Read your knowledge index file (configured in `KNOWLEDGE_INDEX`)
2. Use `grep_search` to find existing knowledge items related to the extracted worldviews
3. Classify: 🟢 Reinforces / 🔴 Contradicts / 🟡 Extends / 🔵 Completely new
4. Skip this phase if no knowledge index is configured

### Phase 6 - Reflection Questions
- Provide 3 questions for the user to internalize
- Ask: which worldview resonates most? What do you want to save to your Worldview Library?

### Phase 7 - Atomize (Storage)

**Storage root:** `<STORAGE_ROOT>/`
**Naming convention:** `YYYY-MM-DD_short-video-name/`

Each video creates 1 dedicated folder containing ALL related data:
```
youtube-learn/
├── _INDEX.md                              <- Master index (agent auto-updates)
├── YYYY-MM-DD_video-name/
│   ├── analysis.md                        <- Full 8-phase analysis
│   ├── transcript.txt                     <- Raw transcript (ALWAYS keep)
│   ├── speaker.md                         <- Speaker profile
│   └── worldviews/
│       └── worldview-[short-name].md      <- One file per worldview
```

- **7A - Speaker Profile:** AUTO-SAVE to `<STORAGE_ROOT>/[video-folder]/speaker.md` - no user approval needed. Use template: `references/speaker_profile_template.md`
- **7B - Worldview Library:** MUST ASK user first -> only save the worldviews user confirms to `<STORAGE_ROOT>/[video-folder]/worldviews/worldview-[name].md`. Use template: `references/worldview_template.md`
- **7C - Update _INDEX.md:** AUTO-ADD new entry to all 3 tables (Videos, Speakers, Worldviews) in `<STORAGE_ROOT>/_INDEX.md`

### Phase 8 - QA Checklist
Check 9 criteria. Fail ANY item -> go back to that phase, DO NOT skip:
1. Transcript is complete (not cut off mid-way)?
2. Speaker Portrait has verified sources (no fabrication)?
3. Each worldview has all 5 analysis dimensions?
4. "Hidden Belief" reads like a proverb (not academic)?
5. "Works When" has concrete examples (not abstract)?
6. "Apply To Me" is actionable (can be done immediately)?
7. Vault Check cross-referenced with existing knowledge?
8. Speaker Profile has been saved/updated?
9. `_INDEX.md` has been updated (3 tables: Videos, Speakers, Worldviews)?

## Pitfalls
- **DO NOT summarize the video** - the goal is excavating worldviews, not creating a summary
- **DO NOT write verbose "Hidden Beliefs"** - must be concise like folk proverbs
- **DO NOT skip QA** - each failed criterion requires going back to the corresponding phase
- **DO NOT save Worldviews without user confirmation** (Phase 7B)
- **Speaker Profile CAN be auto-saved** (Phase 7A) - it's factual data
- **DO NOT scatter files** - all output for 1 video MUST be in the same folder
- **DO NOT forget to update `_INDEX.md`** - it's the quick-lookup map when you have many videos

### ⛔ CRITICAL RULE: SAVE TO PERSISTENT STORAGE
- **ALWAYS** save analysis to your configured `STORAGE_ROOT`, not temporary/ephemeral directories
- Reason: Files in temp directories are lost when starting a new chat session
