# IDEA OS — Edith

**Edith** is a business operating system, not a chatbot. It is a single-owner AI
orchestrator that takes natural-language commands and gets real work done across
Google Drive, Gmail, Calendar, Sheets, and a built-in Projects/Clients/Tasks
workspace — via LLM function calling, not regex or keyword matching. The
dashboard UI (a real, data-backed IDEA OS-branded interface, not a demo) reads
and writes the same data Edith manages through chat. Built as a production
FastAPI service designed to run on Google Cloud Run.

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

**Workspace (Clients/Projects/Tasks)**: the one first-party domain concept beyond
the Google agents. It's a real `project_management` Agent (same pattern as the
Google agents — tools resolve a project/task by partial name match, since a chat
command doesn't carry a UUID), so Edith can create/update it through natural
language. The dashboard's REST endpoints (`/api/v1/{clients,projects,tasks,
dashboard/summary,dashboard/activity}`) read and write the exact same tables
directly, bypassing the LLM loop — a checkbox click shouldn't cost an LLM call.
Long-term memory retrieval/storage is best-effort: a down or misconfigured
embeddings provider degrades gracefully instead of blocking Edith from
responding at all.

## Project layout

```
app/
  core/            settings, structured logging, exceptions, JWT/encryption, DI container
  domain/          framework-free entities and value objects
  application/     ports (interfaces) + use cases
  orchestrator/    Orchestrator, IntentRouter, AgentRegistry, BaseAgent
  agents/          google_drive/ gmail/ google_calendar/ google_sheets/ project_management/
  infrastructure/  Postgres (SQLAlchemy+pgvector), Redis, Anthropic, OpenAI embeddings,
                    Google OAuth + API client factory, Secret Manager (GCP + env)
  interfaces/
    api/           REST API (v1) — chat, auth, health, workspace (dashboard/clients/
                    projects/tasks)
    web/           the IDEA OS dashboard UI (static HTML/JS, real data)
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

### Deploying via GitHub Actions (recommended)

`.github/workflows/deploy.yml` runs the exact same `deploy/deploy.sh` script
above, triggered manually from the Actions tab (`workflow_dispatch`) instead of
from your own machine — no local `gcloud` install needed. One-time setup,
easiest done from **Cloud Shell** in the Cloud Console (it has `gcloud`
pre-installed and already authenticated as you):

```bash
PROJECT_ID=idet-502218
gcloud iam service-accounts create idea-os-deployer --project "$PROJECT_ID"

for ROLE in run.admin iam.serviceAccountUser artifactregistry.writer \
            cloudsql.client secretmanager.secretAccessor vpcaccess.user \
            storage.admin; do
  gcloud projects add-iam-policy-binding "$PROJECT_ID" \
    --member="serviceAccount:idea-os-deployer@${PROJECT_ID}.iam.gserviceaccount.com" \
    --role="roles/${ROLE}"
done

gcloud iam service-accounts keys create idea-os-deployer-key.json \
  --iam-account="idea-os-deployer@${PROJECT_ID}.iam.gserviceaccount.com"
```

Then in the GitHub repo: **Settings → Secrets and variables → Actions → New
repository secret**, name it `GCP_SA_KEY`, and paste the full contents of
`idea-os-deployer-key.json` as the value. Delete the local key file afterwards
(`rm idea-os-deployer-key.json`) — it's only needed once, to seed the secret.

`PROJECT_ID` is already set to `idet-502218` at the top of `deploy.yml`;
change it there if the project ever changes.

## CI

`.github/workflows/ci.yml` runs lint (`ruff`), strict type-checking (`mypy`),
the full test suite against real Postgres+pgvector and Redis services
(including integration tests), and a Docker build — on every push and pull
request.
