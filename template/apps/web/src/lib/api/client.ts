import "server-only";

import createClient from "openapi-fetch";

import type { paths } from "./schema";

// Only the Next.js server calls the API: the browser talks to Next.js, which forwards
// the request with the access token read from an httpOnly cookie. The token is
// therefore never exposed to client-side JavaScript.
const API_URL = process.env.API_URL ?? "http://localhost:8000";

// Typed API client: paths, parameters and responses come from the API's OpenAPI schema.
// Regenerate the types with `make api-types` after changing an API route or schema.
export const api = createClient<paths>({ baseUrl: API_URL, cache: "no-store" });
