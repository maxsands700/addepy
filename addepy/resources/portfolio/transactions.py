"""Transactions resource for the Addepar API."""
import logging
from copy import deepcopy
from typing import Any, Dict, List, Optional, Union

import requests

from ...constants import PortfolioType, TransactionOutputType, TransactionType
from ..base import BaseResource
from ..query import QueryInput, query_parameters

logger = logging.getLogger("addepy")

# All supported transaction types
TRANSACTION_TYPES = {
    "account_fee",
    "account_fee_advisor",
    "account_fee_bank",
    "account_fee_custodian",
    "account_fee_management",
    "account_fee_professional",
    "account_fee_reimbursement",
    "account_fee_reimbursement_advisor",
    "account_fee_reimbursement_bank",
    "account_fee_reimbursement_custodian",
    "account_fee_reimbursement_management",
    "account_fee_reimbursement_professional",
    "adjustment",
    "buy",
    "capital_call",
    "cash_dividend",
    "cash_in_lieu",
    "change_in_unrealized_gain",
    "commitment",
    "commitment_reduction",
    "contribution",
    "conversion",
    "corporate_action",
    "cost_adjustment",
    "cover_short",
    "deposit",
    "distribution",
    "exercise_call",
    "exercise_put",
    "expense",
    "expense_allocated",
    "expiration",
    "fee",
    "fee_reimbursement",
    "fund_redemption",
    "gain",
    "generic_flow",
    "inception",
    "income",
    "income_allocated",
    "interest_expense",
    "interest_income",
    "journal_in",
    "journal_out",
    "loan_issued",
    "loan_taken",
    "lookthrough_adjustment",
    "mark_to_market",
    "node_fee",
    "payment_made_in_lieu_of_dividend",
    "payment_received_in_lieu_of_dividend",
    "proceeds_adjustment",
    "recalled_contribution",
    "redemption",
    "reinvestment",
    "sell",
    "sell_short",
    "snapshot",
    "spinoff",
    "stock_dividend",
    "stock_reverse_split",
    "stock_split",
    "tax",
    "tax_refund",
    "tax_withholding",
    "tax_withholding_refund",
    "transfer",
    "transfer_in",
    "transfer_out",
    "unfunded_adjustment",
    "valuation",
    "withdrawal",
    "write_option",
    "written_exercise_call",
    "written_exercise_put",
    "written_expiration",
}


class TransactionsResource(BaseResource):
    """
    Resource for Addepar Transactions API.

    Tier 1 (CRUD wrappers):
        - get_transaction() - Get a single transaction
        - create_transaction() - Create a single transaction
        - create_transactions() - Bulk create transactions (up to 500)
        - update_transaction() - Update a single transaction
        - update_transactions() - Bulk update transactions (up to 500)
        - delete_transaction() - Delete a single transaction
        - delete_transactions() - Bulk delete transactions (up to 500)
        - get_transaction_owner() - Get the owner entity
        - get_transaction_owned() - Get the owned entity
        - get_transaction_cash_position() - Get the cash position

    Tier 1 (View/Query):
        - get_view_results() - Get transaction view results (sync)
        - query_transactions() - Query transaction data (sync)

    Note: Snapshots and valuations cannot be retrieved/modified via this API.
          Use the Snapshots API instead.
    """

    # =========================================================================
    # Tier 1: CRUD Wrappers
    # =========================================================================

    def get_transaction(self, transaction_id: str) -> Dict[str, Any]:
        """
        Get a single transaction by ID.

        Args:
            transaction_id: The ID of the transaction to retrieve.

        Returns:
            The transaction resource object containing id, type, attributes,
            and relationships.

        Note:
            Cannot be used for snapshots or valuations. Use Snapshots API instead.
        """
        response = self._get(f"/transactions/{transaction_id}")
        data = response.json()
        transaction = data.get("data", {})
        logger.debug(f"Retrieved transaction {transaction_id}")
        return transaction

    def create_transaction(
        self,
        transaction_type: TransactionType,
        currency: str,
        trade_date: str,
        owner_id: Optional[str] = None,
        owned_id: Optional[str] = None,
        *,
        amount: Optional[float] = None,
        units: Optional[float] = None,
        cash_position_id: Optional[str] = None,
        new_owner_id: Optional[str] = None,
        new_owned_id: Optional[str] = None,
        **attributes: Any,
    ) -> Dict[str, Any]:
        """
        Create a single transaction.

        Args:
            transaction_type: Type of transaction (e.g., 'buy', 'sell', 'distribution').
            currency: Three-letter currency code (e.g., 'USD').
            trade_date: Trade date in YYYY-MM-DD format.
            owner_id: ID of the owning entity. Omit for account/node fees when
                the cash position is unknown; the owner relationship is omitted.
            owned_id: ID of the owned entity (security).
            amount: Transaction value. Required for valuations and value-based assets.
            units: Number of shares. Required for share-based assets.
            cash_position_id: Optional ID of the cash position.
            new_owner_id: Receiving owner entity for a transfer.
            new_owned_id: New owned entity for a corporate action.
            **attributes: Additional transaction attributes (e.g., fee, comment,
                description, posted_date, settlement_date, ex_date, etc.).

        Returns:
            The created transaction resource object.

        Raises:
            AddePyError: If transaction creation fails.
        """
        if owned_id is None:
            raise ValueError("owned_id is required")
        if owner_id is None and not (
            transaction_type == "node_fee" or transaction_type.startswith("account_fee")
        ):
            raise ValueError("owner_id is required except for account/node fee transactions")
        tx_attributes: Dict[str, Any] = {
            "type": transaction_type,
            "currency": currency,
            "trade_date": trade_date,
            **attributes,
        }
        if amount is not None:
            tx_attributes["amount"] = amount
        if units is not None:
            tx_attributes["units"] = units

        relationships: Dict[str, Any] = {
            "owned": {"data": {"type": "entities", "id": owned_id}},
        }
        if owner_id is not None:
            relationships["owner"] = {"data": {"type": "entities", "id": owner_id}}
        if cash_position_id is not None:
            relationships["cash_position"] = {
                "data": {"type": "positions", "id": cash_position_id}
            }
        if new_owner_id is not None:
            relationships["new_owner"] = {
                "data": {"type": "entities", "id": new_owner_id}
            }
        if new_owned_id is not None:
            relationships["new_owned"] = {
                "data": {"type": "entities", "id": new_owned_id}
            }

        payload = {
            "data": {
                "type": "transactions",
                "attributes": tx_attributes,
                "relationships": relationships,
            }
        }

        response = self._post("/transactions", json=payload)
        data = response.json()
        transaction = data.get("data", {})
        logger.info(f"Created transaction: {transaction.get('id')}")
        return transaction

    def create_transactions(
        self,
        transactions: List[Dict[str, Any]],
    ) -> List[Dict[str, Any]]:
        """
        Bulk create transactions (up to 500).

        Args:
            transactions: List of transaction dicts. Each must contain:
                - type: Transaction type (e.g., 'buy', 'sell')
                - currency: Three-letter currency code
                - trade_date: YYYY-MM-DD format
                - owner_id: Owning entity ID (omit for account/node fees)
                - owned_id: Owned entity ID
                - Plus optional: amount, units, cash_position_id, new_owner_id,
                  new_owned_id, and other attributes

        Returns:
            List of created transaction resource objects.

        Raises:
            AddePyError: If any transaction creation fails.

        Example:
            transactions = [
                {
                    "type": "buy",
                    "currency": "USD",
                    "trade_date": "2024-01-15",
                    "owner_id": "123",
                    "owned_id": "456",
                    "amount": 10000,
                    "units": 100,
                },
                {
                    "type": "sell",
                    "currency": "USD",
                    "trade_date": "2024-01-16",
                    "owner_id": "123",
                    "owned_id": "456",
                    "amount": 5000,
                    "units": 50,
                },
            ]
            created = client.portfolio.transactions.create_transactions(transactions)
        """
        if not 1 <= len(transactions) <= 500:
            raise ValueError("transactions must contain between 1 and 500 items")
        payload_data = []
        for tx in transactions:
            owned_id = tx["owned_id"]
            owner_id = tx.get("owner_id")
            if owner_id is None and not (
                tx.get("type") == "node_fee" or str(tx.get("type", "")).startswith("account_fee")
            ):
                raise ValueError("owner_id is required except for account/node fee transactions")
            cash_position_id = tx.get("cash_position_id")
            attributes = deepcopy({
                key: value for key, value in tx.items()
                if key not in {"owner_id", "owned_id", "cash_position_id", "new_owner_id", "new_owned_id"}
            })

            relationships: Dict[str, Any] = {
                "owned": {"data": {"type": "entities", "id": owned_id}},
            }
            if owner_id is not None:
                relationships["owner"] = {"data": {"type": "entities", "id": owner_id}}
            if cash_position_id is not None:
                relationships["cash_position"] = {
                    "data": {"type": "positions", "id": cash_position_id}
                }
            for key in ("new_owner", "new_owned"):
                value = tx.get(f"{key}_id")
                if value is not None:
                    relationships[key] = {"data": {"type": "entities", "id": value}}

            payload_data.append({
                "type": "transactions",
                "attributes": attributes,
                "relationships": relationships,
            })

        payload = {"data": payload_data}

        response = self._post("/transactions", json=payload)
        data = response.json()
        created = data.get("data", [])
        logger.info(f"Created {len(created)} transactions")
        return created

    def update_transaction(
        self,
        transaction_id: str,
        **attributes: Any,
    ) -> Dict[str, Any]:
        """
        Update a single transaction.

        Args:
            transaction_id: The ID of the transaction to update.
            **attributes: Attributes to update. Cannot update:
                - vendor_id
                - trade_date (for snapshots/valuations)
                - owner, owned, cash_position relationships

        Returns:
            The updated transaction resource object.

        Note:
            To remove an attribute value, set it to None.
            Cannot be used for snapshots or valuations. Use Snapshots API instead.
        """
        payload = {
            "data": {
                "id": transaction_id,
                "type": "transactions",
                "attributes": attributes,
            }
        }

        response = self._patch(f"/transactions/{transaction_id}", json=payload)
        data = response.json()
        transaction = data.get("data", {})
        logger.info(f"Updated transaction: {transaction_id}")
        return transaction

    def update_transactions(
        self,
        transactions: List[Dict[str, Any]],
    ) -> List[Dict[str, Any]]:
        """
        Bulk update transactions (up to 500).

        Args:
            transactions: List of transaction update dicts. Each must contain:
                - id: The transaction ID to update
                - Plus any attributes to update

        Returns:
            List of updated transaction resource objects.

        Note:
            To remove an attribute value, set it to None.
            Cannot update vendor_id, owner, owned, or cash_position.

        Example:
            updates = [
                {"id": "1001", "comment": "Updated comment"},
                {"id": "1002", "description": None},  # Removes description
            ]
            updated = client.portfolio.transactions.update_transactions(updates)
        """
        if not 1 <= len(transactions) <= 500:
            raise ValueError("transactions must contain between 1 and 500 items")
        payload = {
            "data": [
                {
                    "id": tx["id"],
                    "type": "transactions",
                    "attributes": {k: v for k, v in tx.items() if k != "id"},
                }
                for tx in transactions
            ]
        }

        response = self._patch("/transactions", json=payload)
        data = response.json()
        updated = data.get("data", [])
        logger.info(f"Updated {len(updated)} transactions")
        return updated

    def delete_transaction(self, transaction_id: str) -> None:
        """
        Delete a single transaction.

        Args:
            transaction_id: The ID of the transaction to delete.

        Note:
            Cannot be used for snapshots or valuations. Use Snapshots API instead.
        """
        self._delete(f"/transactions/{transaction_id}")
        logger.info(f"Deleted transaction: {transaction_id}")

    def delete_transactions(self, transaction_ids: List[str]) -> None:
        """
        Bulk delete transactions (up to 500).

        Args:
            transaction_ids: List of transaction IDs to delete.

        Note:
            Cannot be used for snapshots or valuations. Use Snapshots API instead.
        """
        if not 1 <= len(transaction_ids) <= 500:
            raise ValueError("transaction_ids must contain between 1 and 500 items")
        payload = {
            "data": [
                {"id": tx_id, "type": "transactions"}
                for tx_id in transaction_ids
            ]
        }

        self._delete("/transactions", json=payload)
        logger.info(f"Deleted {len(transaction_ids)} transactions")

    # =========================================================================
    # Relationship Methods
    # =========================================================================

    def get_transaction_owner(self, transaction_id: str) -> Dict[str, Any]:
        """
        Get the owner entity of a transaction.

        Args:
            transaction_id: The ID of the transaction.

        Returns:
            The owner entity resource object.
        """
        response = self._get(f"/transactions/{transaction_id}/owner")
        data = response.json()
        entity = data.get("data", {})
        logger.debug(f"Retrieved owner for transaction {transaction_id}")
        return entity

    def get_transaction_owned(self, transaction_id: str) -> Dict[str, Any]:
        """
        Get the owned entity (security) of a transaction.

        Args:
            transaction_id: The ID of the transaction.

        Returns:
            The owned entity resource object.
        """
        response = self._get(f"/transactions/{transaction_id}/owned")
        data = response.json()
        entity = data.get("data", {})
        logger.debug(f"Retrieved owned entity for transaction {transaction_id}")
        return entity

    def get_transaction_cash_position(self, transaction_id: str) -> Dict[str, Any]:
        """
        Get the cash position of a transaction.

        Args:
            transaction_id: The ID of the transaction.

        Returns:
            The cash position resource object.
        """
        response = self._get(f"/transactions/{transaction_id}/cash_position")
        data = response.json()
        position = data.get("data", {})
        logger.debug(f"Retrieved cash position for transaction {transaction_id}")
        return position

    def get_transaction_new_owner(self, transaction_id: str) -> Dict[str, Any]:
        """Get the receiving owner entity for a transfer transaction."""
        return self._get(f"/transactions/{transaction_id}/new_owner").json().get("data", {})

    def get_transaction_new_owned(self, transaction_id: str) -> Dict[str, Any]:
        """Get the new owned entity for a corporate action transaction."""
        return self._get(f"/transactions/{transaction_id}/new_owned").json().get("data", {})

    def get_transaction_owner_relationship(self, transaction_id: str) -> Dict[str, Any]:
        """Get owner linkage containing the entity ID and resource type."""
        return self._get(
            f"/transactions/{transaction_id}/relationships/owner"
        ).json().get("data", {})

    def get_transaction_owned_relationship(self, transaction_id: str) -> Dict[str, Any]:
        """Get owned-entity linkage containing its ID and resource type."""
        return self._get(
            f"/transactions/{transaction_id}/relationships/owned"
        ).json().get("data", {})

    def get_transaction_new_owner_relationship(self, transaction_id: str) -> Dict[str, Any]:
        """Get receiving-owner linkage for a transfer transaction."""
        return self._get(
            f"/transactions/{transaction_id}/relationships/new_owner"
        ).json().get("data", {})

    def get_transaction_new_owned_relationship(self, transaction_id: str) -> Dict[str, Any]:
        """Get new-owned-entity linkage for a corporate action transaction."""
        return self._get(
            f"/transactions/{transaction_id}/relationships/new_owned"
        ).json().get("data", {})

    def get_transaction_cash_account_relationship(self, transaction_id: str) -> Dict[str, Any]:
        """Get cash-position linkage from the documented cash_account route.

        Addepar names the related resource route ``cash_position`` and the
        linkage route ``relationships/cash_account``.
        """
        return self._get(
            f"/transactions/{transaction_id}/relationships/cash_account"
        ).json().get("data", {})

    def get_transaction_files(self, transaction_id: str) -> Dict[str, Any]:
        """Return attachment visibility, management permissions, and items.

        The returned data contains ``visible``, ``can_manage_files``, and
        ``items`` directly, without the standalone Files API's documents
        container. Requires transaction read and Files edit permissions.
        """
        return self._get(f"/transactions/{transaction_id}/files").json().get("data", {})

    def attach_transaction_file(self, transaction_id: str, file_id: str) -> None:
        """Attach an existing file; repeating the association is idempotent.

        Requires transaction read and Files edit permissions. Upload the file
        first using ``client.admin.files.upload_file``.
        """
        self._post(
            f"/transactions/{transaction_id}/files",
            json={"data": {"id": file_id, "type": "files"}},
        )

    def detach_transaction_file(self, transaction_id: str, file_id: str) -> None:
        """Detach a file association, preserving the underlying file record."""
        self._delete(f"/transactions/{transaction_id}/files/{file_id}")

    # =========================================================================
    # View and Query Methods
    # =========================================================================

    def get_view_results(
        self,
        view_id: str,
        portfolio_id: str,
        portfolio_type: PortfolioType,
        start_date: str,
        end_date: str,
        output_type: TransactionOutputType = "CSV",
    ) -> requests.Response:
        """
        Get transaction view results (synchronous).

        Args:
            view_id: ID of the saved transaction view.
            portfolio_id: ID of the portfolio. Use "1" if portfolio_type is FIRM.
            portfolio_type: Type of portfolio. One of: ENTITY, ENTITY_FUNDS, GROUP,
                GROUP_FUNDS, FIRM, FIRM_ACCOUNTS, FIRM_CLIENTS, FIRM_HOUSEHOLDS,
                FIRM_UNVERIFIED_ACCOUNTS.
            start_date: Start date in YYYY-MM-DD format.
            end_date: End date in YYYY-MM-DD format.
            output_type: Output format. One of: CSV, TSV, XLSX. Default: CSV.

        Returns:
            Response object containing the view data. Access via response.content
            for binary (XLSX) or response.text for text (CSV/TSV).

        Note:
            - Transaction Views for "Summary Data" are not supported.
            - For large datasets, use TransactionJobsResource.execute_view_job()
              for async processing.
        """
        params = {
            "portfolio_id": portfolio_id,
            "portfolio_type": portfolio_type.upper(),
            "output_type": output_type.upper(),
            "start_date": start_date,
            "end_date": end_date,
        }

        response = self._get(f"/transactions/views/{view_id}/results", params=params)
        logger.debug(f"Retrieved view {view_id} results")
        return response

    def query_raw(self, query: QueryInput) -> Dict[str, Any]:
        """Execute copied transaction query parameters or JSON text synchronously.

        Also accepts a JSON:API data.attributes envelope. Every query field and
        nested value is preserved without mutating input. Returns the complete
        response, including meta.columns; use transaction_jobs for large exports.
        """
        payload = {"data": {"type": "transaction_query", "attributes": query_parameters(query)}}
        return self._post("/transactions/query", json=payload).json()

    def query_transactions(
        self,
        columns: List[str],
        portfolio_type: PortfolioType,
        portfolio_id: Optional[Union[str, int, List[Union[str, int]]]] = None,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
        *,
        filters: Optional[List[Dict[str, Any]]] = None,
        sorting: Optional[List[Dict[str, Any]]] = None,
        limit: Optional[int] = None,
        include_online_valuations: bool = False,
        include_unverified: bool = False,
        include_deleted: bool = False,
        external_ids: Optional[List[Dict[str, str]]] = None,
    ) -> Dict[str, Any]:
        """
        Query transaction data (synchronous).

        Args:
            columns: List of column attribute keys to return.
                Common columns: trade_date, security, direct_owner, value, type,
                units, currency, fees, description, etc.
            portfolio_type: Type of portfolio. One of: ENTITY, ENTITY_FUNDS, GROUP,
                GROUP_FUNDS, FIRM, FIRM_ACCOUNTS, FIRM_CLIENTS, FIRM_HOUSEHOLDS,
                FIRM_UNVERIFIED_ACCOUNTS.
            portfolio_id: Portfolio ID or list of IDs; omit when using external_ids.
                Use "1" if portfolio_type is FIRM.
            start_date: Start date in YYYY-MM-DD format.
            end_date: End date in YYYY-MM-DD format.
            filters: Optional list of filter objects. Each filter has:
                - attribute: Column to filter on
                - operator: 'include' or 'exclude'
                - type: 'discrete', 'number', 'date', or 'string'
                - values/value/date/number: Filter criteria (depends on type)
            sorting: Optional list of sorting objects. Each has:
                - attribute: Column to sort by
                - ascending: True for ascending, False for descending
                Accepts up to 3 columns. Default sorts by trade_date.
            limit: Max number of transactions to return.
            include_online_valuations: Include online snapshots (default: False).
            include_unverified: Include unverified transactions (default: False).
            include_deleted: Include deleted online transactions (default: False).
            external_ids: External ID dictionaries with external_type_key and
                external_id. Supply exactly one of external_ids and portfolio_id.

        Returns:
            Dictionary with 'meta' (columns) and 'data' (transaction records).

        Note:
            For large datasets, use TransactionJobsResource.execute_query_job()
            for async processing.

        Example:
            results = client.portfolio.transactions.query_transactions(
                columns=["trade_date", "security", "direct_owner", "value"],
                portfolio_type="ENTITY",
                portfolio_id="123",
                start_date="2024-01-01",
                end_date="2024-12-31",
                filters=[{
                    "attribute": "type",
                    "operator": "include",
                    "type": "discrete",
                    "values": ["buy", "sell"],
                }],
                sorting=[{"attribute": "trade_date", "ascending": False}],
            )
        """
        if start_date is None or end_date is None:
            raise ValueError("start_date and end_date are required")
        if isinstance(portfolio_id, list) and not portfolio_id and external_ids is not None:
            portfolio_id = None
        if (portfolio_id is None) == (external_ids is None):
            raise ValueError("Supply exactly one of portfolio_id or external_ids")
        # Normalize portfolio_id to list if needed
        if isinstance(portfolio_id, str):
            portfolio_id = [portfolio_id]

        query_attributes: Dict[str, Any] = {
            "columns": columns,
            "portfolio_type": portfolio_type.upper(),
            "start_date": start_date,
            "end_date": end_date,
            "include_online_valuations": include_online_valuations,
            "include_unverified": include_unverified,
            "include_deleted": include_deleted,
        }
        if portfolio_id is not None:
            query_attributes["portfolio_id"] = portfolio_id
        if external_ids is not None:
            query_attributes["external_ids"] = external_ids

        if filters is not None:
            query_attributes["filters"] = filters
        if sorting is not None:
            query_attributes["sorting"] = sorting
        if limit is not None:
            query_attributes["limit"] = limit

        data = self.query_raw(query_attributes)
        logger.debug(f"Query returned {len(data.get('data', []))} transactions")
        return data
