# Episode scripts

Draft scripts for Day 1 and all 87 lessons of course v8, in the course's two-minute format
(Section 4 of `../AI_Engineering_Course_Razeen_v8.md`).

| File | Contents |
|---|---|
| `day-001.md` | The Day 1 journey video (not one of the 87) |
| `module-00.md` … `module-15.md` | One section per episode, headed `## E012 · B · Title` |

## Conventions
- **`> ` lines are spoken.** The tracker's word counter counts only these. Targets: 220–260 words
  for Concept (C) episodes, 180–240 for Build (B) episodes.
- **`*Screen: …*` lines** say what's on screen. "You on camera" marks the hook and takeaway.
- **`[CAPTURE: …]`** marks a number, output or model answer that must come from your real run.
  Record the demo, then replace the placeholder with what actually happened. Never present an
  invented result as real output (course Section 14).
- **Day numbers** are added to the title when you publish ("Day 23 · …"), not in the script.

## Loading them into the tracker

```powershell
.venv\Scripts\python -m app.cli load-scripts course/scripts
```

This fills the Script card of every episode that doesn't have a script yet. Add `--overwrite` to
replace scripts you've already edited in the tracker (it asks for nothing, so be sure).

These are drafts. Rewrite lines in your own words before recording; you'll sound more natural.
