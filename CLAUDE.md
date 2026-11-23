# CLAUDE.md

This repository is a **Copier template**, not an application. `template/` holds the files of a generated project; `copier.yml` holds the questions and post-generation tasks.

- Read CONTRIBUTING.md for the layout and the test loop (generate into a temp folder, then `make check` there).
- Files ending in `.jinja` are rendered with the answers; keep Jinja out of source code where possible.
- `template/CLAUDE.md` is the guide shipped to generated projects: keep it in sync when conventions change.
- Never claim a change works without generating a project and running `make check` in it.
- Everything in English; Conventional Commits.
