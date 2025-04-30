"""
Beneficiary management tools for the Investec MCP server.
"""
from mcp.server.fastmcp import Context
import json


async def register_beneficiary_tools(mcp):
    """Register all beneficiary management related tools with the MCP server."""
    
    @mcp.tool()
    async def get_beneficiaries(ctx: Context) -> str:
        """Get all beneficiaries for the authenticated user.

        This tool returns information about all saved beneficiaries including 
        beneficiary ID, name, account number, and bank name.

        Args:
            ctx: The MCP server provided context which includes the Investec client
        """
        try:
            investec_client = ctx.request_context.lifespan_context.investec_client
            beneficiaries = await investec_client.get_beneficiaries()
            return json.dumps(beneficiaries, indent=2)
        except Exception as e:
            return f"Error retrieving beneficiaries: {str(e)}"

    @mcp.tool()
    async def get_beneficiary_categories(ctx: Context) -> str:
        """Get all beneficiary categories available.

        This tool returns all available categories for beneficiaries.

        Args:
            ctx: The MCP server provided context which includes the Investec client
        """
        try:
            investec_client = ctx.request_context.lifespan_context.investec_client
            categories = await investec_client.get_beneficiary_categories()
            return json.dumps(categories, indent=2)
        except Exception as e:
            return f"Error retrieving beneficiary categories: {str(e)}"