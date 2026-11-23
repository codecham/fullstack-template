# Contributing

Thanks for helping! Here is how to work on this project.

## Setup

```bash
make setup
```

See the README for prerequisites. `make help` lists every command.

## Workflow

1. Create a branch from `main`: `git switch -c feat/short-description`.
2. Make your change, with tests for any API behavior you add or change.
3. If you changed a model: `make migration m="..."`, review the file, `make migrate`.
4. If you changed an API route or schema: `make api-types` and commit the regenerated types.
5. Run `make check` until it passes. The git hooks also run the fast checks on commit and the type checks on push.
6. Open a pull request. CI runs the same checks and builds the Docker images.

## Conventions

- Code, comments and docs in English.
- Commit messages follow [Conventional Commits](https://www.conventionalcommits.org): `feat:`, `fix:`, `docs:`, `refactor:`, `test:`, `chore:`.
- Keep pull requests small and focused. See [CLAUDE.md](CLAUDE.md) for the architecture and coding conventions.
