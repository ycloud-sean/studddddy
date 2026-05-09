---
name: fastapi-study-workflow
description: "Use in this FastAPI learning repository whenever Codex continues a new learning day/topic, creates tutorial files, summarizes notes, generates HTML notes, or commits/pushes learning artifacts. Enforces project file layout: tutorial Markdown in the corresponding day/topic folder, HTML notes at repo root, no immediate note generation during new learning, and Chinese commit/push after note summarization."
---

# FastAPI Study Workflow

## Core Rules

Apply these rules before creating, moving, committing, or pushing learning files in this repository.

1. When starting a new learning day or topic, create a corresponding folder at the repository root, for example `day4/` or `day-request-body/`.
2. Put tutorial Markdown files inside that corresponding folder, for example `day4/day4-fastapi-tutorial.md`.
3. Do not generate an HTML notes file immediately when learning new content.
4. Generate or update HTML notes only when the user explicitly says they want to summarize, organize, or generate notes, such as “总结笔记”, “整理笔记”, or “生成笔记”.
5. Put all HTML notes in the repository root, for example `day4-fastapi-notes.html`.
6. After finishing note summarization, automatically create a Chinese commit and push it to the remote repository.
7. Keep the skill itself under `.agents/skills/` so it can be committed and pushed with the project.

## New Learning Workflow

When the user says to continue learning a new day/topic:

1. Determine the day/topic from the request or the learning plan.
2. Create the corresponding folder if it does not exist.
3. Write the tutorial Markdown file inside that folder.
4. Create or update runnable practice code only when useful for the lesson. Follow the existing code folder style if present, such as `my_day04/main.py`.
5. Do not create a root HTML notes file in this step.
6. Tell the user which tutorial and code files were created, and mention that notes will be generated after they ask for summarization.

## Note Summarization Workflow

When the user asks to summarize or organize notes:

1. Read the relevant tutorial Markdown file from the corresponding day/topic folder.
2. Use the current conversation context, especially questions and answers from this lesson, to enrich the notes.
3. Generate or update the HTML notes file at the repository root.
4. Keep the HTML note consistent with existing visual style unless the user requests a different style.
5. Verify the relevant code and files before committing.
6. Stage only files related to this learning unit and the skill change if the skill itself was edited.
7. Commit with a concise Chinese commit message.
8. Push the current branch to the remote repository.

## File Layout

Use this layout for future learning units:

```text
.
├── day4/
│   └── day4-fastapi-tutorial.md
├── day4-fastapi-notes.html
├── my_day04/
│   └── main.py
└── .agents/
    └── skills/
        └── fastapi-study-workflow/
            ├── SKILL.md
            └── agents/
                └── openai.yaml
```

If an older lesson already uses a different layout, do not rewrite unrelated history unless the user asks. Apply this layout to new work and to files touched for the current lesson.

## Commit And Push Rules

When committing after note summarization:

1. Check `git status --short` first.
2. Avoid staging unrelated user changes.
3. Use a single commit for the learning unit when possible.
4. Use Chinese commit messages, for example `整理 Day 4 FastAPI 请求体笔记`.
5. Push with `git push origin <current-branch>` unless the repository has a different clear convention.
6. If push fails because of a transient network issue, retry once after checking local commit state.

## Guardrails

- Do not put tutorial Markdown files in the repository root for new lessons.
- Do not put HTML notes inside day/topic folders.
- Do not invent a summary from memory alone; read the tutorial Markdown and use the actual conversation context.
- Do not auto-commit during the “new learning” step unless the user explicitly asks.
- Do not delete or move unrelated existing files to force this layout.
