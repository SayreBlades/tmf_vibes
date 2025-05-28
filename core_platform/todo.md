# TODO - Core TMF Platform (Layer 2)

This document outlines the implementation of the Core TMF Platform acting as a proxy layer between web clients and legacy systems, starting with the TMF620 Product Catalog API.

**Technology:** FastAPI, HTTPX, Pydantic, OpenAPI

**Scope:**
- Implement `GET /productOffering` proxy with pagination and field selection
- Implement `GET /productOffering/{id}` proxy with field selection
- HTTP Basic Auth with configurable credentials
- Strict TMF620 schema validation
- Zipkin distributed tracing
- Structured JSON logging
- Configuration via YAML files
- Integration testing using existing `some_legacy_platform` mock

---

## Milestone 1: Project Setup & Basic FastAPI App

Goal: Establish the core project structure and basic API framework.

*   [x] Create `core_platform` directory structure mirroring `some_legacy_platform`
*   [x] Set up virtual environment with `uv`
*   [x] Install core dependencies: `fastapi`, `httpx`, `pydantic`, `python-multipart`, `pyyaml`
*   [x] Create base FastAPI app in `src/core_platform/main.py` with:
    *   Health check endpoint (`GET /health`)
    *   Empty router for product catalog endpoints
*   [x] Add Makefile commands for:
    *   `run-core` - Start development server
    *   `test-core` - Run test suite
    *   `check` - Run linters/formatters

---

## Milestone 2: Configuration & Authentication

Goal: Implement configurable authentication and legacy system URL management.

*   [ ] Design YAML config file format for:
    *   Authentication credentials (multiple pairs)
    *   Legacy system endpoints
    *   Default location: `./config/config.yaml`
*   [ ] Implement config loader in `src/core_platform/config.py`:
    *   Environment variable override support
*   [ ] Add HTTP Basic Auth middleware:
    *   Validate against configured credentials
    *   Reject invalid credentials with 401

---

## Milestone 3: Proxy Implementation

Goal: Implement core proxy functionality for TMF620 endpoints.

*   [ ] Create HTTP client for legacy system in `src/core_platform/client.py`:
    *   Async requests using HTTPX
    *   Proper timeout handling
    *   Base URL from configuration
*   [ ] Implement `GET /productOffering` proxy:
    *   Forward all query parameters
    *   Pass-through pagination
    *   Maintain headers where appropriate
*   [ ] Implement `GET /productOffering/{id}` proxy:
    *   Validate ID format
    *   perform field selection locally (do not forward)
*   [ ] Write integration tests using `some_legacy_platform` mock:
    *   Test parameter forwarding
    *   Verify header propagation
    *   Test error scenarios

---

## Milestone 4: Validation & Error Handling

Goal: Implement response validation and comprehensive error handling.

*   [ ] Generate Pydantic models from TMF620 OpenAPI spec
*   [ ] Implement strict response validation from the legacy API swagger:
    *   Reject invalid responses with 502
    *   Log validation failures
*   [ ] Enhance error handling:
    *   Timeout detection (504)
    *   Legacy system errors (502)
    *   Schema validation failures (502)
*   [ ] Add integration tests for:
    *   Invalid response formats
    *   Legacy system error conditions
    *   Timeout scenarios

---

## Milestone 5: Observability & Operations

Goal: Add logging, tracing and operational features.

*   [ ] Implement JSON-formatted logging:
    *   Request/response logging
    *   Error logging with stack traces
    *   Correlation IDs
*   [ ] Add Zipkin distributed tracing:
    *   Trace outgoing legacy calls
    *   Include auth/proxy spans
    *   Configure sampling rate

---

## Before Completing Each Milestone:

*   Ensure all `pytest` tests pass
*   Run linters and formatters (`ruff check .`, `ruff format .`)
*   Verify type checking (`mypy src`)
*   Update README.md with new features
*   Manual test against running `some_legacy_platform` instance
