---
name: fastapi-study-workflow
description: "用于这个 FastAPI 学习仓库。当 Codex 继续新的学习 day/topic、创建教程 Markdown、练习代码、总结笔记、生成 HTML 笔记、提交或 push 学习产物时使用。约束项目文件布局和语言：每天一个 my_dayXX 目录，教程 MD 和当天代码放在同一目录中，教程 MD 必须用中文写，HTML 笔记放在仓库根目录，新学习内容时不要立即生成笔记，总结笔记完成后使用中文 commit 并 push。"
---

# FastAPI 学习流程

## 核心规则

在这个仓库里创建、移动、提交或推送学习文件前，先执行这些规则。

1. 每次开始新的学习 day 时，在仓库根目录创建当天文件夹，命名格式使用 `my_dayXX`，例如 `my_day04/`。
2. 教程 Markdown 文件必须和当天代码放在同一个 `my_dayXX/` 文件夹中，例如 `my_day04/day4-fastapi-tutorial.md` 和 `my_day04/main.py`。
3. 教程 Markdown 的面向人说明必须使用中文。代码标识符、文件名、导入路径、API 路径和命令示例保持正常技术写法。
4. 学习新内容时，不要立即生成 HTML 笔记文件。
5. 只有当用户明确说“总结笔记”、“整理笔记”、“生成笔记”等需求时，才生成或更新 HTML 笔记。
6. 所有 HTML 笔记都放在仓库根目录，例如 `day4-fastapi-notes.html`。
7. 笔记整理完成后，自动使用中文 commit message 提交代码，并 push 到远程仓库。
8. 这个 skill 自身必须放在 `.agents/skills/` 下，方便随项目一起提交和推送。
9. 后续维护这个 skill 时，除 `name`、路径、命令、代码标识符等技术内容外，说明文字也必须使用中文。

## 学习新内容流程

当用户说继续学习新的 day 或 topic 时：

1. 根据用户请求或学习计划确认 day 编号。
2. 如果当天文件夹不存在，先按 `my_dayXX` 格式创建文件夹，例如 Day 4 使用 `my_day04/`。
3. 在当天 `my_dayXX/` 文件夹里编写教程 Markdown 文件，并用中文写面向人的解释内容。
4. 如果本节课需要可运行代码，也放在同一个 `my_dayXX/` 文件夹里，例如 `my_day04/main.py`。
5. 这个阶段不要创建根目录 HTML 笔记文件。
6. 回复用户时说明创建了哪些教程和代码文件，并提醒笔记会在用户要求总结后再生成。

## 笔记整理流程

当用户要求总结、整理或生成笔记时：

1. 读取对应 `my_dayXX/` 文件夹中的教程 Markdown 文件。
2. 结合当前对话上下文，尤其是本节课里的问答内容，整理进笔记。
3. 在仓库根目录生成或更新 HTML 笔记文件。
4. HTML 笔记风格默认延续现有笔记样式，除非用户要求换风格。
5. 提交前先验证相关代码和文件。
6. 只暂存当前学习单元相关文件；如果本 skill 也被修改，再一起暂存 skill 相关文件。
7. 使用简洁中文 commit message 提交。
8. 将当前分支 push 到远程仓库。

## 文件布局

后续学习单元使用这个布局：

```text
.
├── day4-fastapi-notes.html
├── my_day04/
│   ├── day4-fastapi-tutorial.md
│   └── main.py
└── .agents/
    └── skills/
        └── fastapi-study-workflow/
            ├── SKILL.md
            └── agents/
                └── openai.yaml
```

如果旧课程已经用了不同布局，不要为了统一格式去改无关历史文件。这个规则默认应用到新的学习内容，以及当前任务会触碰到的学习文件。对于已有课程，如果同一天同时存在教程 MD 和代码，也应整理到同一个 `my_dayXX/` 文件夹中。

## 提交和推送规则

笔记整理后提交时：

1. 先运行 `git status --short`。
2. 不要暂存无关的用户改动。
3. 一个学习单元尽量使用一个提交。
4. commit message 使用中文，例如 `整理 Day 4 FastAPI 请求体笔记`。
5. 默认使用 `git push origin <current-branch>`，除非仓库里有更明确的推送约定。
6. 如果 push 因网络短暂异常失败，先确认本地提交状态，再重试一次。

## 防护规则

- 新课程的教程 Markdown 不要放在仓库根目录，也不要放在单独的 `dayXX/` 文件夹中。
- 当天代码和当天教程 Markdown 不要拆在两个目录里；统一放进对应 `my_dayXX/` 文件夹。
- 教程 Markdown 的说明内容不要写英文，除非用户明确要求英文。
- HTML 笔记不要放进 day/topic 文件夹。
- 不要只凭记忆生成笔记；必须读取教程 Markdown，并结合真实对话上下文。
- 学习新内容阶段不要自动 commit，除非用户明确要求。
- 不要为了强行套用新布局而删除或移动无关旧文件。
