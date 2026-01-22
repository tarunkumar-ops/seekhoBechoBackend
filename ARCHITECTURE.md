## Architecture Rules (API-Only)

- No Django templates, no `render()`, no server-side HTML.
- Follow Clean Architecture / Hexagonal with DDD structure.
- Dependency direction: `interfaces → application → domain`; `infrastructure` only flows into container wiring. Inner layers must not import outer layers.

### Directories and Responsibilities
- `config/`: Django settings, ASGI/WSGI, root URLs only.
- `src/shared/`: Pure Python cross-cutting utilities (exceptions, logging helpers, datetime/money). No Django/DRF/Redis/ES.
- `src/domain/`: Core business logic (entities, value objects, domain services/events). Pure Python only; no HTTP, ORM, Redis, ES, Celery, external APIs.
- `src/application/`: Use cases, DTOs, ports (interfaces). Can import domain/shared. No ORM/Redis/ES/HTTP/DRF here.
- `src/application/ports/`: Interfaces only; no implementations or framework imports.
- `src/infrastructure/`: Technical implementations (ORM models, Redis, ES, payment, auth, messaging). Implements ports. No business rules. Domain must never import this.
- `src/interfaces/`: I/O layers.
  - `api/`: DRF views/serializers/routing. Thin: HTTP → DTO → use case → response. No business logic or ORM/Redis calls.
  - `cli/`: Management commands; same thin rules.
- `src/container.py`: Composition root. Only place to instantiate infrastructure and connect ports to implementations. Views must not create infrastructure directly.
- `src/tests/`: Enforce boundaries (domain pure, application mocks ports, infrastructure integration, API end-to-end).

### Technology Boundaries
- Redis: infrastructure only via a `CachePort`; decisions in application; domain unaware.
- Elasticsearch: infrastructure only via a `SearchPort`; triggered by use cases; domain unaware.
- Database/ORM: Django models only in `infrastructure/persistence`; ORM usage only in repository implementations. Forbidden in domain/application/interfaces.

### API Flow (Always)
HTTP request → API view → DTO → Use case → Domain logic → Ports → Infrastructure → Response.

### Forbidden Patterns
- Business logic in views.
- ORM queries in use cases.
- Django imports in domain.
- Redis/ES clients outside infrastructure.
- Domain importing infrastructure.
- “Fat models” with business logic.
