"""
MCP server tools for interfacing with Investec Banking API.
"""
from .accounts import register_account_tools
from .profiles import register_profile_tools
from .beneficiaries import register_beneficiary_tools
from .payments import register_payment_tools
from .documents import register_document_tools


async def register_all_tools(mcp):
    """
    Register all MCP server tools for the Investec Banking API.
    
    Args:
        mcp: The MCP server instance to register tools with
    """
    await register_account_tools(mcp)
    await register_profile_tools(mcp)
    await register_beneficiary_tools(mcp)
    await register_payment_tools(mcp)
    await register_document_tools(mcp)