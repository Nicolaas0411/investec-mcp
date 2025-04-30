"""
Account information tools for the Investec MCP server.
"""
from mcp.server.fastmcp import Context
import json
from typing import Optional


async def register_account_tools(mcp):
    """Register all account information related tools with the MCP server."""
    
    @mcp.tool()
    async def get_accounts(ctx: Context) -> str:
        """Get all accounts for the authenticated user.

        This tool returns information about all accounts available to the user including 
        account number, name, product name, reference name, and KYC compliance status.

        Args:
            ctx: The MCP server provided context which includes the Investec client
        """
        try:
            investec_client = ctx.request_context.lifespan_context.investec_client
            accounts = await investec_client.get_accounts()
            return json.dumps(accounts, indent=2)
        except Exception as e:
            return f"Error retrieving accounts: {str(e)}"

    @mcp.tool()
    async def get_account_balance(ctx: Context, account_id: str) -> str:
        """Get the balance for a specific account.

        This tool returns the current, available, budget, straight, and cash balances for the specified account.

        Args:
            ctx: The MCP server provided context which includes the Investec client
            account_id: The ID of the account to retrieve the balance for
        """
        try:
            investec_client = ctx.request_context.lifespan_context.investec_client
            balance = await investec_client.get_account_balance(account_id)
            return json.dumps(balance, indent=2)
        except Exception as e:
            return f"Error retrieving account balance: {str(e)}"

    @mcp.tool()
    async def get_account_transactions(
        ctx: Context, 
        account_id: str, 
        from_date: Optional[str] = None, 
        to_date: Optional[str] = None,
        transaction_type: Optional[str] = None,
        include_pending: bool = False
    ) -> str:
        """Get transactions for a specific account with optional filtering.

        This tool returns the list of transactions for the specified account with various filtering options.

        Args:
            ctx: The MCP server provided context which includes the Investec client
            account_id: The ID of the account to retrieve transactions for
            from_date: Optional start date in format YYYY-MM-DD
            to_date: Optional end date in format YYYY-MM-DD
            transaction_type: Optional transaction type filter (e.g., "FeesAndInterest")
            include_pending: Whether to include pending transactions
        """
        try:
            investec_client = ctx.request_context.lifespan_context.investec_client
            transactions = await investec_client.get_account_transactions(
                account_id, from_date, to_date, transaction_type, include_pending
            )
            return json.dumps(transactions, indent=2)
        except Exception as e:
            return f"Error retrieving account transactions: {str(e)}"

    @mcp.tool()
    async def get_pending_transactions(ctx: Context, account_id: str) -> str:
        """Get pending transactions for a specific account.

        This tool returns only the pending transactions for the specified account.

        Args:
            ctx: The MCP server provided context which includes the Investec client
            account_id: The ID of the account to retrieve pending transactions for
        """
        try:
            investec_client = ctx.request_context.lifespan_context.investec_client
            pending_transactions = await investec_client.get_pending_transactions(account_id)
            return json.dumps(pending_transactions, indent=2)
        except Exception as e:
            return f"Error retrieving pending transactions: {str(e)}"