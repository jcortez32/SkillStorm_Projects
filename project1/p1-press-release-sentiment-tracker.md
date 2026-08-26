# Press Release Sentiment Tracker

## Objective

Develop an investor-relations backend for a firm that tracks how a
company's own public communications read over time — not what outside
analysts say about a company, but whether the company's *own* press
releases are trending more confident or more cautious quarter over
quarter. The system should make it easy to manage tracked companies and
log their press releases, and automatically score each release's tone via
**Amazon Comprehend**, so an analyst can see a sentiment trend line across
a company's communications history instead of re-reading every release
from scratch. Prioritize correctness on the data layer — a release's
sentiment score and detected key phrases are explicit, queryable fields
tied to the exact text they were derived from, with the underlying
confidence preserved. The deliverable is a containerized service that runs
locally via `docker compose up` and exposes a documented REST API, backed
by a real PostgreSQL database and real (in production) calls to an AWS
managed AI service.

## Functional Requirements

### Company Management

- **Add New Company:**
  - Analysts should be able to add a tracked company by specifying its
    ticker symbol, name, and sector.
- **View Companies:**
  - Provide a dashboard endpoint listing all tracked companies with their
    core metadata and press release count.
- **Edit Company:**
  - Allow updating a company's name or sector.
- **Delete Company:**
  - Implement deletion with a confirmation requirement (such as requiring
    the company id in the request body). Decide (and document in your
    README) whether deleting a company cascades to delete its press releases.

### Press Release Management

- **Add Press Release:**
  - Analysts should be able to log a press release by specifying a
    headline, body text, and published date.
- **View Press Releases:**
  - List all press releases for a company, including sentiment
    classification and detected key phrases, with filter support by
    sentiment and date range.
- **Edit Press Release:**
  - Allow correcting a release's headline, body text, or published date.
    Decide (and document in your README) whether editing the body text
    re-triggers sentiment analysis.
- **Delete Press Release:**
  - Implement deletion with a confirmation requirement (such as requiring
    the release id in the request body).

### API Design & Developer Experience

- **Consistent Error Envelopes:**
  - All errors (validation, not-found, conflict, upstream AI-service
    failure) should return a consistent JSON shape with an error code,
    human-readable message, and request_id.
- **Liveness and Readiness:**
  - Expose `/live` and `/ready` endpoints. `/live` confirms the process is
    up; `/ready` confirms downstream dependencies (the database) are
    reachable. Comprehend reachability is *not* part of `/ready` — see
    Edge Case Handling below.
- **Structured Request Logging:**
  - Every request should emit a structured log line containing method,
    path, status code, duration, and correlation id, as machine-parseable JSON.
- **Filtered Listings:**
  - List endpoints should support filter + sort query parameters across
    `sentiment`, `published_at` range, and headline (partial match).

### Edge Case Handling

- **Comprehend Is Unavailable:**
  - Decide how press release submission behaves if sentiment analysis
    fails. Should the release still save with `analysis_status` marked
    `pending` (with a retry endpoint), or should submission be rejected
    outright? Document your choice and reasoning.
- **`MIXED` Sentiment Results:**
  - A press release announcing good quarterly earnings alongside a
    leadership departure may legitimately score `MIXED`. Decide how your
    trend endpoint (below) represents `MIXED` results in an aggregate —
    counted separately, or split proportionally by confidence — and
    document your choice.
- **Future-Dated or Backdated Press Releases:**
  - Decide whether a `published_at` date in the future is allowed (e.g.,
    for scheduling) or rejected, and enforce that decision via Pydantic validation.
- **Very Short Release (Headline Only, No Body):**
  - Decide on (and enforce via Pydantic) a minimum body length for
    reliable sentiment analysis, and document why you picked it.
- **Concurrent Mutations:**
  - Describe what happens if two analysts edit the same press release at
    the same time, or a company is deleted while a new release for it is
    still being analyzed. Document the expected behavior.

### AI-Assisted Feature (Required)

> **Sequencing — build this last.** This feature is a required, graded
> part of the deliverable, not an optional stretch goal. Implement it only
> after the core CRUD service is complete and working end to end — the AI
> pipeline should be layered on top of a finished functional deliverable,
> not built in parallel with it. A complete core with the AI feature added
> last scores well; an AI pipeline bolted onto an incomplete or broken core
> does not.

- **Sentiment Analysis:**
  - When a press release is logged, call Comprehend's `DetectSentiment`
    against the body text and store the classification and confidence scores.
- **Key Phrase Extraction:**
  - Call Comprehend's `DetectKeyPhrases` against the same text and store
    the resulting phrases as a queryable list on the record.
- **Sentiment Trend Over Time:**
  - Add `GET /companies/{id}/sentiment-trend` returning sentiment
    breakdown grouped by a time period you choose (e.g., by month) across
    a company's press release history — the actual "trending more
    confident or more cautious over time" payoff from the Objective, not
    just a sentiment label sitting on each individual release.
- **Isolated, Mockable AWS Client:**
  - All Comprehend calls must go through a single, injectable client
    module (mirroring the shared-session pattern from this course's Week
    3 boto3 material) so your test suite can substitute a fake/mocked
    client and run without live AWS credentials.

## Stretch Goals

Stretch goals are features you want to add to an application, but they
aren't required. For this project, Stretch Goals are a way to go above and
beyond the minimum requirements and I look forward to seeing what unique
features you will add to your project. Here are some examples you might consider:

- **Deploy the App to AWS:**
  - Push your Docker image to Amazon ECR and run the stack on an AWS
    compute service of your choice (App Runner, ECS, or an EC2 instance).
    Document your deployment architecture and any cost/cleanup considerations.
- **Bedrock-Powered Trend Narrative:**
  - Add an endpoint that sends a company's sentiment-trend data to a
    foundation model via Bedrock's Converse API and returns a short
    narrative explaining the trend. This uses content not yet covered in
    lecture at the time this project is assigned — a good stretch goal
    for anyone who wants to explore ahead.
- **SageMaker Custom Model:**
  - Train a simple custom model that predicts short-term stock movement
    correlation with press release sentiment, hosted behind a SageMaker
    endpoint. Also beyond the current curriculum — a good "go deeper" option.
- **Rate Limiting:**
  - Add Flask-Limiter to throttle press release submissions per client
    IP. Choose a sensible limit and document why in your README.
- **Second Entity Relationship:**
  - Extend the model to support a `Competitor` grouping — companies
    tagged into a peer group for side-by-side sentiment comparison.
- **Minimal Web UI:**
  - Add a single HTML page (or React app) that consumes your API and
    renders a company's sentiment trend as a simple chart.
- **Persistent Audit Log:**
  - Record every mutation (create / update / delete) into an audit table
    with timestamp, action, entity, and actor.
- **Bulk Import:**
  - Add an endpoint that accepts a CSV of historical press releases and
    inserts them for a company in one transaction, with all-or-nothing semantics.
- **Cross-Company Sector Comparison:**
  - Add an endpoint comparing average sentiment across all tracked
    companies within the same sector over a given time period.

## Technical Requirements

Must be a backend solution consisting of:

- Python 3.11+
- Flask 3.x with the app-factory pattern and blueprints
- Pydantic v2 for HTTP-boundary validation
- PostgreSQL via SQLAlchemy 2.0 and Flask-Migrate, with a real migration
  history checked into the repo (no `create_all()` in production code paths)
- boto3, authenticated via a dedicated, least-privilege IAM user (never
  root/admin credentials) — the IAM policy JSON granting only
  `comprehend:DetectSentiment` and `comprehend:DetectKeyPhrases` must be
  committed to the repo
- A single, injectable Comprehend client wrapper module used by every
  AI-assisted endpoint — not `boto3.client(...)` called ad hoc from route handlers
- structlog for structured JSON logging with per-request correlation IDs
- pytest with fixtures and parametrize for the test suite; AWS calls must
  be mocked/stubbed in tests (e.g. `unittest.mock` or `botocore.stub.Stubber`)
  so the suite runs without live AWS credentials or network access
- Docker multi-stage Dockerfile + docker-compose.yml for a local
  api + db stack, with a database health check gating the API's startup
- pyproject.toml with a src/ layout and a `[project.optional-dependencies]` dev block
- Code should be available in a private GitHub repository, with the
  instructor added as a collaborator
- Possesses all required CRUD functionality
- Handles edge cases effectively

## Non-Functional Requirements

- Well-documented code (module docstrings + function docstrings on public surfaces)
- Code upholds industry best practices (SOLID / DRY / single-responsibility)
- Type hints on every function signature
- Test coverage on happy + error paths (at least 15 pytest tests, including
  at least one test per Comprehend-backed endpoint using a mocked client)
- Structured logs (no print statements in production code paths)
- Container runnable via a single `docker compose up`
- README with one-line install and one-line run instructions, plus your
  documented decisions for every Edge Case Handling item above
- Pydantic models have explicit field constraints (Literal types, min/max
  length on headline/body text)
- No mutable default arguments; use `field(default_factory=...)` for collections
- Errors raise typed exceptions from a DomainError hierarchy, not generic Exception
- Data model documented as an entity-relationship diagram (ERD) — every
  entity, its fields, and the cardinality of each relationship — checked
  into the repository
- A kanban board with a complete, prioritized backlog is set up **before
  development begins**; work is pulled from the board rather than started ad hoc
