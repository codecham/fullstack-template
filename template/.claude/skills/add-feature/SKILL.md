---
name: add-feature
description: Add a new resource or feature end to end in this project (database model, migration, API endpoints with tests, typed client, Next.js page). Use when the user asks to add a feature, entity, resource or CRUD.
---

# Add a feature end to end

Follow these steps in order. Use the `users` feature as the reference for every layer. Example resource below: `Note` owned by a user.

## 1. Model and migration (`apps/api`)

1. Create `app/models/note.py` with a `Note(TimestampMixin, Base)` model. Use `uuid.UUID` primary keys like `User`, and a `ForeignKey("users.id", ondelete="CASCADE")` for ownership.
2. Export it from `app/models/__init__.py`.
3. Run `make migration m="create notes table"`, read the generated file in `migrations/versions/`, fix it if needed, then `make migrate`.

## 2. Schemas and service

1. `app/schemas/note.py`: `NoteCreate` (input, with `Field` constraints) and `NoteRead` (`model_config = ConfigDict(from_attributes=True)`).
2. `app/services/notes.py`: plain functions taking `db: Session` first. Always filter by the owner (`Note.user_id == user.id`) so users only reach their own data. Raise domain exceptions for expected failures.

## 3. Routes

1. `app/routes/notes.py` with `router = APIRouter(prefix="/notes", tags=["notes"])`. Protect endpoints with the `CurrentUser` dependency. Return `NoteRead`, declare status codes (`201` on create, `204` on delete) and map service exceptions to `HTTPException` (`404` for another user's note, never `403`, so ids do not leak).
2. Register the router in `app/main.py`.

## 4. Tests

Create `tests/routes/test_notes.py` (Arrange / Act / Assert, fixtures `client` and `db`): the happy path, validation errors (`422`), missing token (`401`) and access to another user's resource (`404`). Run `make test`.

## 5. Frontend (`apps/web`)

1. Run `make api-types` so the typed client knows the new endpoints.
2. Add a page under `src/app/` (for example `src/app/notes/page.tsx`). Read the session and data inside a `<Suspense>` boundary, redirect to `/login` when `getCurrentUser()` returns null, as in `src/app/account/page.tsx`.
3. Call the API with `api` from `@/lib/api/client`, passing the bearer token server-side (see `getCurrentUser` in `src/lib/auth/session.ts`; add a small helper there if several calls need the token).
4. Put mutations in a server action file next to the page; revalidate or redirect after a change.
5. Add a link in the navigation if useful.

## 6. Finish

Run `make check` and fix everything it reports. Summarize the endpoints and pages you added.
