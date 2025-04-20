# tmf_vibes

## Resources

- [Excalidraw](https://excalidraw.com/#room=9bb5a9a19e10793c9ce9,lx0sDFlFuupSXP51WrAORQ)
- [AI Studio](https://aistudio.google.com/app/prompts?state=%7B%22ids%22:%5B%221CSEMj0J1W_OeHfAUOpz8CSvmmFxETTNV%22%5D,%22action%22:%22open%22,%22userId%22:%22102676693169168925003%22,%22resourceKeys%22:%7B%7D%7D&usp=sharing)

## Development Setup

1.  **Clone the repository:**
    ```bash
    git clone <repository-url>
    cd tmf-vibes
    ```

2.  **Create and activate virtual environment (using uv):**
    ```bash
    # Create the virtual environment in .venv directory
    uv venv

    # Activate the environment (example for bash/zsh)
    source .venv/bin/activate
    # On Windows (Command Prompt): .venv\Scripts\activate.bat
    # On Windows (PowerShell): .venv\Scripts\Activate.ps1
    ```
    *Note: Subsequent commands assume the virtual environment is activated.*

3.  **Install dependencies (using uv):**
    ```bash
    # Installs the project in editable mode along with development dependencies
    uv pip install -e ".[dev]"
    ```

4.  **Run tools:**
    Ensure your virtual environment is activated (`source .venv/bin/activate`) before running these commands, or prefix them with `uv run`.

    *   **Tests:**
        ```bash
        uv run pytest
        ```
    *   **Linting & Formatting Check:**
        ```bash
        uv run ruff check .
        ```
    *   **Formatting Apply:**
        ```bash
        uv run ruff format .
        ```
    *   **Type Checking:**
        ```bash
        uv run mypy src
        ```

## Relevant TMF API Specifications for End-to-End Product Ordering Playbook

Here is a list of TMF API specifications relevant to the process of discovering, qualifying, quoting, and ultimately submitting a Product Order request, along with the reason for their relevance:

1.  **TMF622 Product Ordering Management:**
    * The central API for submitting the final, committed product order request after pricing and configuration are determined. Defines the `ProductOrder` and `ProductOrderItem` structures.

2.  **TMF648 Quote Management:**
    * Manages the pre-order phase where specific product configurations, customer eligibility, discounts, promotions, and negotiated terms are applied to calculate a finalized price offer (the Quote) before commitment.

3.  **TMF620 Product Catalog Management:**
    * Defines the sellable `ProductOfferings`, their underlying technical `ProductSpecifications`, associated characteristics, rules, and importantly, the standard `ProductOfferingPrices` which serve as the basis for quoting and ordering.

4.  **TMF632 Party Management:**
    * Manages information about the parties involved, primarily the customer (Individual or Organization). Needed for identification, eligibility checks, and associating the quote/order with the correct entity.

5.  **TMF651 Agreement Management:**
    * Manages commercial agreements with customers or partners, which may contain specific terms (like pricing, SLAs) that influence the available offerings or the final price calculated in a quote. Referenced in TMF622.

6.  **TMF679 Product Offering Qualification (POQ):**
    * Used to check the technical feasibility and availability of a specific product offering for a particular context (e.g., customer, location) *before* generating a quote or order. Helps avoid invalid requests. Referenced in TMF622.

7.  **TMF678 Billing Account Management:**
    * Manages the billing accounts to which charges for the product order will be applied. Orders typically need to be associated with a valid billing account. Referenced in TMF622.

8.  **TMF672 Geographic Address Management:**
    * Manages physical addresses, often required for validating serviceability (via POQ), determining eligibility for certain offers/prices, or specifying delivery/installation locations.

9.  **TMF673 Geographic Site Management:**
    * An alternative or complement to Address Management, focusing on managed sites (buildings, equipment locations) which might be relevant for service delivery points.

10. **TMF669 Party Role Management:**
    * Defines the specific roles (e.g., 'Buyer Contact', 'Technical Contact', 'Seller') that parties play in the context of interactions like quotes or orders. Complements TMF632.

11. **TMF690 Sales Channel Management:**
    * Defines the channels through which offerings are made available (e.g., 'Online', 'Retail', 'Partner'). Offerings and pricing can sometimes be channel-specific. Referenced in TMF620/TMF622.

12. **TMF637 Product Inventory Management:**
    * While not strictly needed *before* ordering, it manages the active product instances resulting *from* a successfully completed order. It becomes relevant for subsequent modification or deletion orders (which would use TMF622).

13. **TMF641 Service Order Management:**
    * Often represents the *downstream* fulfillment process triggered by a TMF622 Product Order, handling the technical provisioning and activation of underlying services. Understanding this relationship helps define the complete end-to-end flow, although direct interaction might be internal to the provider's systems.
