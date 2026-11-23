# Contributing to the template

## Layout

```
copier.yml      questions and post-generation tasks
template/       the files of a generated project
  *.jinja       rendered with the answers (the suffix is removed)
  other files   copied as they are
.github/        CI of the template itself
```

Keep as many files as possible free of Jinja: plain files can be linted, type checked and opened by your editor. Put project-specific values in `.env.example.jinja`, `compose.yaml.jinja` or `apps/web/src/lib/site.ts.jinja` rather than in source code.

## Testing a change

Generate a project from your working copy and run its checks. Copier reads the last commit, so commit first (amend or squash later if you like):

```bash
git commit -am "wip"
uvx copier copy --trust --defaults --skip-tasks --vcs-ref HEAD --data project_name="Demo" . /tmp/demo
cd /tmp/demo
git init -q && make setup && make check
```

If ports 5432, 8000 or 3000 are taken, create `/tmp/demo/.env` with `scripts/generate-env.sh` and change the ports before `make setup` (it keeps an existing `.env`).

CI does the same for both values of `use_pgvector`, and also starts the production-like stack.

## Updating dependencies

- API: `cd template/apps/api && uv lock --upgrade`
- Web: `cd template/apps/web && npm update` (or bump `package.json`, then `npm install`)
- After an API change, regenerate `template/apps/web/src/lib/api/schema.d.ts` from a generated project with `make api-types` and copy it back.

## Gotchas

- `template/.env.example.jinja` matches the generated `.gitignore` (`.env.*`): it is tracked in git, but a new file with that name needs `git add -f`.
- GitHub Actions expressions (`${{ ... }}`) inside `.jinja` files must be wrapped in `{% raw %}...{% endraw %}`.
- Release a version with a git tag (`v1.0.0`): `copier copy` uses the latest tag by default.
