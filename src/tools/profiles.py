"""
Profile management tools for the Investec MCP server.
"""
from mcp.server.fastmcp import Context
import json


async def register_profile_tools(mcp):
    """Register all profile management related tools with the MCP server."""
    
    @mcp.tool()
    async def get_profiles(ctx: Context) -> str:
        """Get all profiles consented to by the authenticated user.

        This tool returns information about all profiles the user has access to.

        Args:
            ctx: The MCP server provided context which includes the Investec client
        """
        try:
            investec_client = ctx.request_context.lifespan_context.investec_client
            profiles = await investec_client.get_profiles()
            return json.dumps(profiles, indent=2)
        except Exception as e:
            return f"Error retrieving profiles: {str(e)}"

    @mcp.tool()
    async def get_profile_accounts(ctx: Context, profile_id: str) -> str:
        """Get accounts for a specific profile.

        This tool returns all accounts associated with the specified profile.

        Args:
            ctx: The MCP server provided context which includes the Investec client
            profile_id: The ID of the profile to retrieve accounts for
        """
        try:
            investec_client = ctx.request_context.lifespan_context.investec_client
            profile_accounts = await investec_client.get_profile_accounts(profile_id)
            return json.dumps(profile_accounts, indent=2)
        except Exception as e:
            return f"Error retrieving profile accounts: {str(e)}"

    @mcp.tool()
    async def get_authorisation_setup_details(ctx: Context, profile_id: str, account_id: str) -> str:
        """Get authorisation setup details for a specific profile and account.

        This tool returns the authorisation setup details needed for payments requiring authorisation.

        Args:
            ctx: The MCP server provided context which includes the Investec client
            profile_id: The ID of the profile
            account_id: The ID of the account
        """
        try:
            investec_client = ctx.request_context.lifespan_context.investec_client
            auth_details = await investec_client.get_authorisation_setup_details(profile_id, account_id)
            return json.dumps(auth_details, indent=2)
        except Exception as e:
            return f"Error retrieving authorisation setup details: {str(e)}"

    @mcp.tool()
    async def get_profile_beneficiaries(ctx: Context, profile_id: str, account_id: str) -> str:
        """Get beneficiaries for a specific profile and account.

        This tool returns all beneficiaries associated with the specified profile and account.

        Args:
            ctx: The MCP server provided context which includes the Investec client
            profile_id: The ID of the profile
            account_id: The ID of the account
        """
        try:
            investec_client = ctx.request_context.lifespan_context.investec_client
            profile_beneficiaries = await investec_client.get_profile_beneficiaries(profile_id, account_id)
            return json.dumps(profile_beneficiaries, indent=2)
        except Exception as e:
            return f"Error retrieving profile beneficiaries: {str(e)}"