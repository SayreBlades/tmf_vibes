# Mock TMF620 Legacy Platform (`some_legacy_platform`)

This project provides a simplified mock implementation of the TMF620 Product Catalog Management API (v5.0.0). It is intended for testing the Core TMF Platform proxy component.

## Functionality

*   **API:** Implements a subset of the TMF620 API using FastAPI (`src/some_legacy_platform/main.py`).
*   **Data Source:** Serves static product offering data loaded from JSON files located in the `data/` directory (e.g., `data/offering_1.json`). The data loading logic is in `src/some_legacy_platform/data_loader.py`.
*   **Endpoints:**
    *   `GET /health`: A simple health check endpoint.
    *   `GET /productOffering/{id}`: Retrieves a specific product offering by its ID. Supports the `fields` query parameter for field selection. Returns 404 if the ID is not found.
    *   `GET /productOffering`: Lists product offerings. Supports `offset`, `limit` query parameters for pagination and the `fields` parameter for field selection.
*   **Testing:** Tests for data loading (`tests/test_data_loader.py`) and the API endpoints (`tests/test_api.py`) are included.

## Running the Server

1.  Ensure you have installed dependencies for this sub-project (refer to the root `README.md` and `pyproject.toml`). You might need to activate the virtual environment and run `uv sync --all-extras` within the `some_legacy_platform` directory if you haven't already.
2.  From the **root directory** of the `tmf_vibes` project, run the following command:

    ```bash
    make run-some-legacy-platform
    ```

3.  The server will start on `http://127.0.0.1:8081`. You can access the health check at `http://127.0.0.1:8081/health` and the OpenAPI documentation at `http://127.0.0.1:8081/docs`.
