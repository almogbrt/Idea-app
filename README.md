# IDEA OS — Edith

**Edith** is a business operating system, not a chatbot. It is a single-owner AI
orchestrator that takes natural-language commands and gets real work done across
Google Drive, Gmail, Calendar, and Sheets — via LLM function calling, not regex or
keyword matching. Built as a production FastAPI service designed to run on Google
Cloud Run.

## Architecture

Clean Architecture, strictly layered (dependencies point inward):

```
interfaces/api        FastAPI routers, Pydantic schemas, middleware
        │
orchestrator          Orchestrator, Intent Router (LLM tool-use loop), Agent Registry
        │
application           Use cases + ports (interfaces) — no framework, no SDK imports
        │
domain                Pure entities and value objects
        │
infrastructure         Concrete adapters: Postgres/pgvector, Redis, Anthropic,
                        OpenAI embeddings, Google OAuth + API clients, Secret Manager
```

**Extensibility**: a new Agent is a new folder under `app/agents/<name>/` with an
`agent.py` (subclasses `BaseAgent`), `tools.py` (a list of `Tool` instances with a
JSON-Schema `parameters_schema`), and a `client.py`. Register it in
`app/agents/__init__.py`. Nothing in the orchestrator, intent router, or API layer
ever needs to change — the Intent Router discovers every tool from the
`AgentRegistry` and lets the LLM decide which one(s) to call.

**Intent Router**: there is no regex or if/elif intent matching anywhere. Every
command is sent to Claude with the full set of registered tool schemas via native
tool use; the LLM decides what to call, tools execute, results feed back, and the
loop continues until a final natural-language reply is produced (bounded by
`MAX_TOOL_ITERATIONS`).

**Single-owner system**: Google OAuth2 login is required, but if `OWNER_EMAIL` is
set, only that Google account may ever authenticate — this is a personal system,
not a multi-tenant product.

## Project layout

```
app/
  core/            settings, structured logging, exceptions, JWT/encryption, DI container
  domain/          framework-free entities and value objects
  application/     ports (interfaces) + use cases
  orchestrator/    Orchestrator, IntentRouter, AgentRegistry, BaseAgent
  agents/          google_drive/ gmail/ google_calendar/ google_sheets/ — one Agent each
  infrastructure/  Postgres (SQLAlchemy+pgvector), Redis, Anthropic, OpenAI embeddings,
                    Google OAuth + API client factory, Secret Manager (GCP + env)
  interfaces/
    api/           REST API (v1) — chat, auth, health
    web/           the simple chat UI (static HTML/JS)
alembic/           database migrations
tests/
  unit/            fast, no external services — fakes for every port
  integration/     real Postgres+pgvector / Redis (skipped automatically if unreachable)
deploy/            Dockerfile companions: Cloud Run manifest + deploy script
```

## Local development

Requirements: Python 3.12+, Docker (for Postgres/Redis), a Google Cloud project
with OAuth credentials, an Anthropic API key, an OpenAI API key (embeddings only).

1. Copy `.env.example` to `.env` and fill in the values (see comments inline —
   in particular generate `TOKEN_ENCRYPTION_KEY` and `JWT_SIGNING_KEY` as shown).
2. Start everything:
   ```bash
   docker compose up --build
   ```
   This starts Postgres (with the `pgvector` extension pre-installed), Redis, and
   the app itself, running Alembic migrations automatically before serving.
3. Open `http://localhost:8080` for the chat UI, or `http://localhost:8080/docs`
   for the OpenAPI docs.

### Running without Docker

```bash
pip install -e ".[dev]"
alembic upgrade head            # requires a reachable Postgres with pgvector
uvicorn app.main:app --reload
```

## Google OAuth setup

1. In Google Cloud Console, create an OAuth 2.0 Client ID (Web application).
2. Add `http://localhost:8080/api/v1/auth/google/callback` (and your production
   callback URL) as an authorized redirect URI.
3. Enable the Drive, Gmail, Calendar, and Sheets APIs for the project.
4. Set `GOOGLE_OAUTH_CLIENT_ID` / `GOOGLE_OAUTH_CLIENT_SECRET` in `.env`.
5. Set `OWNER_EMAIL` to your Google account email to restrict login to yourself.

## Testing

```bash
ruff check app tests      # lint
mypy app                  # strict type checking
pytest                    # unit tests (fakes only, no services needed)
pytest tests/integration  # requires Postgres+pgvector and Redis reachable
pytest --cov=app --cov-report=term-missing
```

## Deploying to Cloud Run

1. Create the required secrets in Secret Manager (names must match
   `deploy/cloudrun-service.yaml`): `idea-os-database-url`, `idea-os-redis-url`,
   `idea-os-token-encryption-key`, `idea-os-jwt-signing-key`,
   `idea-os-anthropic-api-key`, `idea-os-openai-api-key`,
   `idea-os-google-oauth-client-id`, `idea-os-google-oauth-client-secret`,
   `idea-os-owner-email`.
2. Provision Cloud SQL (Postgres, with `pgvector` installed) and Memorystore
   (Redis), and a Serverless VPC Access connector so Cloud Run can reach Redis.
3. Run the deploy script:
   ```bash
   PROJECT_ID=my-project REGION=us-central1 ./deploy/deploy.sh
   ```
   This builds and pushes the image, runs Alembic migrations as a one-off Cloud
   Run Job, then deploys the service from `deploy/cloudrun-service.yaml`.

**Bootstrapping note**: the service's own URL isn't known until after the first
deploy, so `GOOGLE_OAUTH_REDIRECT_URI` can't be set correctly up front. Run
`deploy.sh` once to get a URL, then:
1. Add `https://<service-url>/api/v1/auth/google/callback` as an authorized
   redirect URI on the OAuth client in Google Cloud Console.
2. Re-run `deploy.sh` (it now resolves the real service URL automatically) so
   the running service's `GOOGLE_OAUTH_REDIRECT_URI` matches.

Also, while the OAuth consent screen is in "Testing" mode, only the email
addresses listed under **Test users** can complete login — add your own
`OWNER_EMAIL` there or login will be rejected before it ever reaches Edith.

## CI

`.github/workflows/ci.yml` runs lint (`ruff`), strict type-checking (`mypy`),
the full test suite against real Postgres+pgvector and Redis services
(including integration tests), and a Docker build — on every push and pull
request.
