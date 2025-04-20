# Specification: Core TMF Platform - Product Catalog Proxy (Initial Phase)

## 1. Overview

This document specifies the initial implementation phase for the core TMF platform component of a new TMF-based e-commerce solution. The overall solution consists of three layers:

1.  **Web Client:** The user-facing e-commerce interface.
2.  **Core TMF Platform:** An abstraction layer providing standardized TMF APIs.
3.  **Underlying Legacy Systems:** Existing BSS/OSS systems providing data and functionality (initially mocked or represented by a single TMF-compliant system).

This initial phase focuses on implementing a narrow use case within the **Product Catalog** domain. The core TMF platform will act as a proxy for specific TMF620 Product Catalog Management API operations, retrieving data from an underlying system.

While the initial implementation targets a single, TMF-compliant underlying system for broadband products, the design of the core platform must anticipate future expansion to integrate with multiple, potentially non-TMF-compliant (e.g., SOAP/XML) legacy systems managing different product types (e.g., mobile services). This initial proxy serves as the foundation for that abstraction layer.

## 2. Architecture

*   **Layer 1 (Web Client):** Consumes the TMF APIs exposed by the Core TMF Platform. (Details outside the scope of this initial spec).
*   **Layer 2 (Core TMF Platform):**
    *   Exposes a subset of the TMF620 Product Catalog Management API northbound.
    *   Acts as a proxy, forwarding requests to the appropriate underlying system(s).
    *   Handles authentication towards underlying systems.
    *   Performs schema validation on responses from underlying TMF systems.
    *   Implements standardized error handling towards the web client.
    *   **Initial Scope:** Proxies requests to a single underlying TMF620-compliant system for broadband products.
    *   **Future Scope:** Designed to evolve into an abstraction layer over multiple, diverse legacy systems, potentially requiring data aggregation and transformation logic.
*   **Layer 3 (Underlying Legacy Systems):**
    *   **Initial Scope:** A single system exposing a TMF620 v5.0.0 compliant API for broadband product catalog data.
    *   **Future Scope:** Multiple systems with potentially diverse interfaces (TMF REST, SOAP, custom APIs, databases, etc.).

## 3. Core Platform API (Northbound)

The core platform shall expose the following TMF620 v5.0.0 compliant API endpoints to the web client:

*   **`GET /productOffering`**
    *   **Description:** Lists product offerings based on filter criteria.
    *   **Compliance:** Adheres strictly to the TMF620 v5.0.0 specification (`docs/TMF620-Product_Catalog_Management-v5.0.0.oas.yaml`) regarding path, method, query parameters (including filtering, pagination (`offset`, `limit`), and field selection (`fields`)), and successful (HTTP 200 OK) response structures.
    *   **Behavior:** Proxies the request, including all query parameters, to the underlying legacy system.
*   **`GET /productOffering/{id}`**
    *   **Description:** Retrieves the details of a specific product offering by its ID.
    *   **Compliance:** Adheres strictly to the TMF620 v5.0.0 specification (`docs/TMF620-Product_Catalog_Management-v5.0.0.oas.yaml`) regarding path, method, path parameters (`id`), query parameters (`fields`), and successful (HTTP 200 OK) response structures.
    *   **Behavior:** Proxies the request, including the ID and query parameters, to the underlying legacy system.

## 4. Core Platform Logic (Proxying)

*   **Request Forwarding:** For the initial implementation, the core platform directly forwards the incoming northbound request parameters (query parameters for list, path/query parameters for retrieve) to the corresponding southbound request to the legacy broadband system.
*   **Data Modification:** No modification, filtering, or aggregation of request or response data is performed in this initial phase. The platform acts as a pass-through proxy for successful operations.

## 5. Southbound Communication (to Legacy System)

*   **Target System:** Initially, a single legacy system providing broadband product catalog data via a TMF620 v5.0.0 compliant API. The base URL for this system needs to be configurable.
*   **Request Mapping:**
    *   `GET /productOffering` (northbound) maps to `GET /productOffering` (southbound).
    *   `GET /productOffering/{id}` (northbound) maps to `GET /productOffering/{id}` (southbound).
*   **Parameter Passing:** All query parameters received on the northbound API are passed directly to the southbound API request.

## 6. Authentication (Southbound)

*   **Mechanism:** HTTP Basic Authentication shall be used for requests from the core platform to the legacy system.
*   **Credential Retrieval:** The username and password for Basic Authentication shall be obtained by calling a mock function within the core platform. This function requires no input arguments for the initial implementation.
*   **Header Injection:** The core platform must construct the `Authorization` header with the retrieved credentials (e.g., `Authorization: Basic <base64(username:password)>`) and include it in every southbound request to the legacy system.

## 7. Schema Validation

*   **Target:** The core platform MUST validate the response body of *successful* (HTTP 200 OK) responses received from the underlying TMF legacy system.
*   **Schema:** Validation MUST be performed against the standard TMF620 v5.0.0 OpenAPI specification definitions (`docs/TMF620-Product_Catalog_Management-v5.0.0.oas.yaml`).
*   **Failure Action:** If schema validation fails, the core platform MUST trigger the specific error handling defined in Section 8.

## 8. Error Handling (Northbound)

The core platform MUST implement the following error handling strategy when responding to the web client:

*   **Scenario 1: Legacy System Response Fails Schema Validation**
    *   **HTTP Status Code:** `502 Bad Gateway`
    *   **Response Body:** Empty.
*   **Scenario 2: Legacy System Returns HTTP Error (4xx or 5xx)**
    *   **HTTP Status Code:** `502 Bad Gateway`
    *   **Response Body:** Empty.
*   **Scenario 3: Network/Connection Error Communicating with Legacy System** (e.g., timeout, connection refused)
    *   **HTTP Status Code:** `502 Bad Gateway`
    *   **Response Body:** Empty.
*   **Scenario 4: Successful Response from Legacy System (HTTP 200 OK) AND Schema Validation Passes**
    *   **HTTP Status Code:** `200 OK`
    *   **Response Body:** The validated response body received from the legacy system (passed through unmodified).

**Note:** No details about the underlying system errors or validation failures should be leaked to the web client in the 502 responses. Appropriate logging should be implemented within the core platform for debugging purposes.

## 9. Future Considerations

*   **Multiple Legacy Systems:** The core platform architecture should facilitate adding support for more underlying systems in the future. This will likely involve:
    *   A routing mechanism to direct requests to the correct system based on product type or other criteria.
    *   Adapter/connector components for different legacy system interface types (SOAP, custom REST, etc.).
    *   Potential data aggregation logic if a single northbound request requires data from multiple southbound systems.
    *   Potential data transformation logic to map legacy data models to the TMF620 model.
*   **Caching:** Introduce caching mechanisms to improve performance and reduce load on legacy systems.
*   **Enhanced Filtering/Modification:** Implement business logic within the core platform to filter or modify data (e.g., hide internal products, enrich data).
*   **More Sophisticated Authentication:** Support different authentication mechanisms for various legacy systems.

## 10. Testing Plan

*   **Unit Testing:**
    *   Test the Basic Authentication credential retrieval (mocking the function) and header construction logic.
    *   Test the schema validation logic using sample valid and invalid TMF620 response payloads.
    *   Test the request forwarding logic (ensuring parameters are passed correctly).
    *   Test the error handling logic for each defined scenario (validation failure, legacy error, network error).
*   **Integration Testing (Requires Mock Legacy System):**
    *   Set up a mock TMF620 service simulating the legacy system.
    *   **Happy Path:**
        *   Send `GET /productOffering` and `GET /productOffering/{id}` requests to the core platform.
        *   Verify the mock legacy system receives the correct request (path, parameters, Basic Auth header).
        *   Configure the mock to return a valid TMF620 response.
        *   Verify the core platform returns HTTP 200 OK and the correct, validated response body.
    *   **Error Paths:**
        *   Configure the mock to return an invalid TMF620 response body -> Verify core platform returns 502 / empty body.
        *   Configure the mock to return an HTTP 4xx or 5xx error -> Verify core platform returns 502 / empty body.
        *   Simulate network timeout/connection error to the mock -> Verify core platform returns 502 / empty body.

## 11. References

*   **TMF620 Product Catalog Management API User Guide:** `docs/TMF620_Product_Catalog_userguide.md`
*   **TMF620 Product Catalog Management API OpenAPI Specification:** `docs/TMF620-Product_Catalog_Management-v5.0.0.oas.yaml`
*   **(Future)** Other relevant TMF API specifications as needed (e.g., TMF622 Product Ordering, TMF632 Party Management).
