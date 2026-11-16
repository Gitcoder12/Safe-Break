# Claude Code project guidance

@AGENTS.md

For task-specific procedures, read `SKILLS.md` and load the relevant skill from `.claude/skills/`. The canonical skill text is maintained under `.agents/skills/`; Claude discovery files are pointers and must remain in sync with canonical paths.

Do not assume a skill grants permission to perform external actions. Follow the user's explicit authorization and the repository's safety boundaries.