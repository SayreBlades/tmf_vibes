# TODO - Mock TMF620 Legacy Platform (`some_legacy_platform`)

This document outlines the steps to build a mock legacy system simulating a TMF620 v5.0.0 Product Catalog API for testing the Core TMF Platform.

**Technology:** FastAPI

**Scope:**
*   Implement `GET /productOffering` with pagination (`offset`, `limit`) and field selection (`fields`). **No filtering.**
*   Implement `GET /productOffering/{id}` with field selection (`fields`).
*   Serve 10 static `ProductOffering` examples loaded from JSON files.
*   Return 404 for non-existent IDs.
*   No authentication required.
*   Standard FastAPI CLI startup with port configuration.
*   This project is to be implemented in the `some_legacy_platform` subfolder in the root of the reopsitory. Failure to adhere to this will lead to jail time.

---

## Milestone 1: Project Setup & Basic FastAPI App

Goal: Set up the basic project structure and a running FastAPI application.

*   [x] Create `some_legacy_platform` directory (if not already present).
*   [x] Initialize a standard Python project structure within `some_legacy_platform` (e.g., `src/`, `tests/`, `data/`).
*   [x] Set up a virtual environment (using `uv venv`).
*   [x] Install necessary dependencies (via `pyproject.yaml`): `fastapi`, `uvicorn[standard]`, `pytest`, `pydantic`.
*   [x] Create a basic FastAPI app instance in `src/main.py`.
*   [x] Add a simple health check endpoint (e.g., `GET /health`) that returns HTTP 200 OK.
*   [x] Update the root `Makefile` with convenience commands (e.g., `run-some-legacy-platform` to start the server with `uvicorn`, `test` to run all `pytest` tests within all projects like `some_legacy_platform`, `core_platform`).

## Milestone 2: Static Data Preparation & Loading

Goal: Prepare the sample `ProductOffering` data and load it into the application.

*   [x] Define the structure for 10 sample `ProductOffering` objects, adhering to the TMF620 v5.0.0 schema (`docs/TMF620-Product_Catalog_Management-v5.0.0.oas.yaml`). Ensure each has a unique `id`. (Simplified structure used)
*   [x] Create 10 separate JSON files (e.g., `offering_1.json`, `offering_2.json`, ...) in the `data/` directory, each containing one `ProductOffering` object.
*   [x] Implement a utility function or class in `src/data_loader.py` to load these JSON files into an in-memory data structure (dictionary keyed by `id`) when the module is imported.
*   [x] Integrate loading into FastAPI app startup using `lifespan` in `src/main.py`.
*   [x] Write unit tests (`tests/test_data_loader.py`) for the data loading mechanism to ensure all 10 offerings are loaded correctly.

## Milestone 3: Implement `GET /productOffering/{id}` Endpoint

Goal: Implement the endpoint to retrieve a single `ProductOffering` by its ID.

*   [x] Define a Pydantic model representing the `ProductOffering` structure based on the TMF620 schema (consider placing this in `src/models.py`).
*   [x] Create the FastAPI route for `GET /productOffering/{offering_id}` in `src/main.py` (or a dedicated router file).
*   [x] Implement the logic within the route function to:
    *   [x] Look up the `offering_id` in the loaded static data.
    *   [x] Return the corresponding `ProductOffering` object if found.
    *   [x] Return an HTTP 404 `NotFound` response if the `id` is not found.
*   [x] Implement field selection logic:
    *   [x] Accept the `fields` query parameter (comma-separated string).
    *   [x] If `fields` is provided, parse it and return only the requested top-level fields from the `ProductOffering` object.
    *   [x] If `fields` is not provided, return the full object.
*   [x] Write integration tests (`tests/`) for this endpoint using `pytest` and FastAPI's `TestClient`:
    *   [x] Test retrieving each of the 10 existing offerings by their correct IDs.
    *   [x] Test requesting a non-existent ID and verify the 404 response.
    *   [x] Test retrieving an existing offering with a specific `fields` parameter (e.g., `?fields=id,name`) and verify only those fields are returned.
    *   [x] Test retrieving an existing offering without the `fields` parameter and verify the full object is returned.

## Milestone 4: Implement `GET /productOffering` Endpoint

Goal: Implement the endpoint to list `ProductOffering`s with pagination and field selection.

*   [ ] Create the FastAPI route for `GET /productOffering` in `src/main.py` (or a dedicated router file).
*   [ ] Implement pagination logic:
    *   Accept `offset` (default 0) and `limit` (default e.g., 10) query parameters.
    *   Apply slicing to the list of loaded static offerings based on `offset` and `limit`.
*   [ ] Implement field selection logic:
    *   Accept the `fields` query parameter.
    *   Apply field selection to *each* `ProductOffering` object in the paginated list before returning.
*   [ ] Ensure the response body is a JSON array containing the (potentially field-selected) `ProductOffering` objects for the requested page.
*   [ ] Write integration tests (`tests/`) for this endpoint:
    *   Test listing without parameters (should return the first `limit` items).
    *   Test listing with `limit=2`.
    *   Test listing with `offset=2`.
    *   Test listing with `offset=1`, `limit=2`.
    *   Test listing with `offset` greater than the number of items (should return an empty list).
    *   Test listing with the `fields` parameter (e.g., `?fields=id,name`) and verify the structure of items in the list.
    *   Test listing combining pagination and `fields`.

## Before completing each Milestone:

Goal: Ensure the implemented milestone is clean, tested

*   Ensure all `pytest` tests pass reliably.
*   Run linters and formatters (e.g., `ruff check .`, `ruff format .`) and fix any issues.
*   Add type hints to all functions and methods. Run `mypy` and fix any type errors.
*   Create a simple `README.md` within `some_legacy_platform/` explaining how to install dependencies and run the mock server.
*   Manually test running the server (`make run` or `uvicorn ...`) and accessing the endpoints via `curl` or a browser.
