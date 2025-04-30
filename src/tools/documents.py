"""
Document management tools for the Investec MCP server.
"""
from mcp.server.fastmcp import Context
import json


async def register_document_tools(mcp):
    """Register all document management related tools with the MCP server."""
    
    @mcp.tool()
    async def get_documents(ctx: Context, account_id: str, from_date: str, to_date: str) -> str:
        """Get a list of documents for a specific account within a date range.

        This tool returns all available documents for the specified account within the given date range.

        Args:
            ctx: The MCP server provided context which includes the Investec client
            account_id: The ID of the account to retrieve documents for
            from_date: Start date in format YYYY-MM-DD
            to_date: End date in format YYYY-MM-DD
        """
        try:
            investec_client = ctx.request_context.lifespan_context.investec_client
            documents = await investec_client.get_documents(account_id, from_date, to_date)
            return json.dumps(documents, indent=2)
        except Exception as e:
            return f"Error retrieving documents: {str(e)}"

    @mcp.tool()
    async def get_document(ctx: Context, account_id: str, document_type: str, document_date: str) -> str:
        """Get a specific document.

        This tool retrieves a specific document by type and date for the specified account.

        Args:
            ctx: The MCP server provided context which includes the Investec client
            account_id: The ID of the account
            document_type: The type of document (e.g., "Statement" or "TaxCertificate")
            document_date: The date of the document in format YYYY-MM-DD
        """
        try:
            investec_client = ctx.request_context.lifespan_context.investec_client
            document = await investec_client.get_document(account_id, document_type, document_date)
            return json.dumps(document, indent=2)
        except Exception as e:
            return f"Error retrieving document: {str(e)}"