# syntax=docker/dockerfile:1

# --- Dependencies: installed once, reused by the dev and build stages ---
FROM node:26-alpine AS deps
ENV NEXT_TELEMETRY_DISABLED=1
WORKDIR /app
# Run as the image's built-in non-root "node" user
RUN chown node:node /app
USER node
COPY --chown=node:node package.json package-lock.json ./
RUN --mount=type=cache,target=/home/node/.npm,uid=1000,gid=1000 \
    npm ci --no-audit --no-fund

# --- Development: `next dev` with hot reload (used by compose.override.yaml) ---
FROM deps AS dev
COPY --chown=node:node . .
EXPOSE 3000
CMD ["npm", "run", "dev", "--", "--hostname", "0.0.0.0"]

# --- Build: compile the production bundle ---
FROM deps AS build
COPY --chown=node:node . .
RUN npm run build

# --- Runtime: only the standalone server, no source code or dev dependencies ---
FROM node:26-alpine AS runtime
ENV NODE_ENV=production \
    NEXT_TELEMETRY_DISABLED=1 \
    HOSTNAME=0.0.0.0 \
    PORT=3000
WORKDIR /app
COPY --from=build --chown=node:node /app/public ./public
COPY --from=build --chown=node:node /app/.next/standalone ./
COPY --from=build --chown=node:node /app/.next/static ./.next/static
USER node
EXPOSE 3000
CMD ["node", "server.js"]
