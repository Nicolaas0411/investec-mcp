"""
Transfer and payment tools for the Investec MCP server.
"""
from mcp.server.fastmcp import Context
import json
from typing import List, Dict, Any, Optional


async def register_payment_tools(mcp):
    """Register all transfer and payment related tools with the MCP server."""
    
    @mcp.tool()
    async def transfer_multiple(
        ctx: Context, 
        from_account_id: str, 
        transfer_list: List[Dict[str, Any]],
        profile_id: Optional[str] = None
    ) -> str:
        """Transfer funds to one or multiple accounts.

        This tool transfers money to one or more accounts from a source account.

        Args:
            ctx: The MCP server provided context which includes the Investec client
            from_account_id: The ID of the source account
            transfer_list: List of transfers to make, each containing beneficiaryAccountId, amount, myReference, and theirReference
            profile_id: Optional profile ID
        """
        try:
            investec_client = ctx.request_context.lifespan_context.investec_client
            transfer_result = await investec_client.transfer_multiple(
                from_account_id, transfer_list, profile_id
            )
            return json.dumps(transfer_result, indent=2)
        except Exception as e:
            return f"Error performing transfers: {str(e)}"

    @mcp.tool()
    async def pay_multiple(ctx: Context, account_id: str, payment_list: List[Dict[str, Any]]) -> str:
        """Pay funds to one or multiple beneficiaries.

        This tool makes payments to one or more saved beneficiaries from the specified account.

        Args:
            ctx: The MCP server provided context which includes the Investec client
            account_id: The ID of the source account
            payment_list: List of payments to make, each containing beneficiaryId, amount, myReference, theirReference,
                         and optionally authoriserAId, authoriserBId, authPeriodId, and fasterPayment
        """
        try:
            investec_client = ctx.request_context.lifespan_context.investec_client
            payment_result = await investec_client.pay_multiple(account_id, payment_list)
            return json.dumps(payment_result, indent=2)
        except Exception as e:
            return f"Error making payments: {str(e)}"

    @mcp.tool()
    async def transfer_money(ctx: Context, from_account_id: str, to_account_id: str, amount: float, reference: str) -> str:
        """Transfer money between accounts.

        This tool transfers money between two accounts owned by the authenticated user.

        Args:
            ctx: The MCP server provided context which includes the Investec client
            from_account_id: The ID of the source account
            to_account_id: The ID of the destination account
            amount: The amount to transfer
            reference: A reference for the transaction
        """
        try:
            investec_client = ctx.request_context.lifespan_context.investec_client
            transfer_result = await investec_client.transfer_money(
                from_account_id, to_account_id, amount, reference
            )
            return json.dumps(transfer_result, indent=2)
        except Exception as e:
            return f"Error transferring money: {str(e)}"

    @mcp.tool()
    async def pay_beneficiary(ctx: Context, account_id: str, beneficiary_id: str, amount: float, reference: str) -> str:
        """Pay a saved beneficiary.

        This tool makes a payment to a saved beneficiary from the specified account.

        Args:
            ctx: The MCP server provided context which includes the Investec client
            account_id: The ID of the source account
            beneficiary_id: The ID of the beneficiary to pay
            amount: The amount to pay
            reference: A reference for the payment
        """
        try:
            investec_client = ctx.request_context.lifespan_context.investec_client
            payment_result = await investec_client.pay_beneficiary(
                account_id, beneficiary_id, amount, reference
            )
            return json.dumps(payment_result, indent=2)
        except Exception as e:
            return f"Error paying beneficiary: {str(e)}"