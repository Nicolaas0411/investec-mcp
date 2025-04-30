<h1 align="center">Investec MCP: Banking API for AI Agents</h1>

<p align="center">
  <img src="public/investec_mcp.png" alt="Mem0 and MCP Integration" width="600">
</p>


A [Model Context Protocol (MCP)](https://modelcontextprotocol.io) server implementation that integrates with the Investec Open Banking API, allowing AI agents to access banking information and perform transactions.

## Overview

This project provides an MCP server that enables AI agents to interact with the Investec Open Banking API. It follows the best practices laid out by Anthropic for building MCP servers, allowing seamless integration with any MCP-compatible client like Claude.

## Features

The server provides comprehensive banking tools based on the Investec Open Banking API:

### Account Information
1. **`get_accounts`**: Retrieve all accounts for the authenticated user
2. **`get_account_balance`**: Get the balance for a specific account
3. **`get_account_transactions`**: Get transactions for a specific account with filtering options
4. **`get_pending_transactions`**: Get pending transactions for a specific account

### Profile Management
5. **`get_profiles`**: Get all profiles the user has consented to
6. **`get_profile_accounts`**: Get accounts for a specific profile
7. **`get_profile_beneficiaries`**: Get beneficiaries for a specific profile and account
8. **`get_authorisation_setup_details`**: Get authorization setup details for payments requiring approval

### Beneficiary Management
9. **`get_beneficiaries`**: Get all saved beneficiaries 
10. **`get_beneficiary_categories`**: Get all beneficiary categories

### Transfers and Payments
11. **`transfer_money`**: Transfer money between your own accounts (convenience method)
12. **`transfer_multiple`**: Transfer funds to one or multiple accounts in a batch
13. **`pay_beneficiary`**: Make a payment to a saved beneficiary (convenience method)
14. **`pay_multiple`**: Make payments to multiple beneficiaries in a batch

### Document Management
15. **`get_documents`**: Get a list of documents for an account in a date range
16. **`get_document`**: Get a specific document by type and date

## Prerequisites

- Python 3.12+
- Investec Developer account with API credentials
- Docker if running the MCP server as a container (recommended)

## Installation

### Using uv

1. Clone this repository:
   ```bash
   git clone https://github.com/yourusername/investec-mcp.git
   cd investec-mcp
   ```

2. Install dependencies:
   ```bash
   uv pip install -e .
   ```

3. Create a `.env` file based on `.env.example`:
   ```bash
   cp .env.example .env
   ```

4. Configure your environment variables in the `.env` file with your Investec API credentials

### Using Docker (Recommended)

1. Build the Docker image:
   ```bash
   docker build -t investec/mcp --build-arg PORT=8050 .
   ```

2. Create a `.env` file based on `.env.example` and configure your environment variables

## Configuration

The following environment variables can be configured in your `.env` file:

| Variable | Description | Example |
|----------|-------------|----------|
| `TRANSPORT` | Transport protocol (sse or stdio) | `sse` |
| `HOST` | Host to bind to when using SSE transport | `0.0.0.0` |
| `PORT` | Port to listen on when using SSE transport | `8050` |
| `INVESTEC_CLIENT_ID` | Client ID from Investec Developer Portal | `your-client-id` |
| `INVESTEC_CLIENT_SECRET` | Client Secret from Investec Developer Portal | `your-client-secret` |
| `INVESTEC_API_KEY` | API Key from Investec Developer Portal | `your-api-key` |

## Running the Server

### Using uv

#### SSE Transport

```bash
# Set TRANSPORT=sse in .env then:
uv run python src/main.py
```

The MCP server will run as an API endpoint that you can connect to.

#### Stdio Transport

With stdio, the MCP client itself can spin up the MCP server.

### Using Docker

#### SSE Transport

```bash
docker run --env-file .env -p 8050:8050 investec/mcp
```

The MCP server will run as an API endpoint within the container that you can connect to.

#### Stdio Transport

With stdio, the MCP client itself can spin up the MCP server container.

## Integration with MCP Clients

### SSE Configuration

Once you have the server running with SSE transport, you can connect to it using this configuration:

```json
{
  "mcpServers": {
    "investec": {
      "transport": "sse",
      "url": "http://localhost:8050/sse"
    }
  }
}
```

> **Note for Windsurf users**: Use `serverUrl` instead of `url` in your configuration:
> ```json
> {
>   "mcpServers": {
>     "investec": {
>       "transport": "sse",
>       "serverUrl": "http://localhost:8050/sse"
>     }
>   }
> }
> ```

Make sure to update the port if you are using a value other than the default 8050.

### Python with Stdio Configuration

Add this server to your MCP configuration for Claude Desktop, Windsurf, or any other MCP client:

```json
{
  "mcpServers": {
    "investec": {
      "command": "path/to/python",
      "args": ["path/to/investec-mcp/src/main.py"],
      "env": {
        "TRANSPORT": "stdio",
        "INVESTEC_CLIENT_ID": "your-client-id",
        "INVESTEC_CLIENT_SECRET": "your-client-secret",
        "INVESTEC_API_KEY": "your-api-key"
      }
    }
  }
}
```

### Docker with Stdio Configuration

```json
{
  "mcpServers": {
    "investec": {
      "command": "docker",
      "args": ["run", "--rm", "-i", 
               "-e", "TRANSPORT", 
               "-e", "INVESTEC_CLIENT_ID", 
               "-e", "INVESTEC_CLIENT_SECRET", 
               "-e", "INVESTEC_API_KEY", 
               "investec/mcp"],
      "env": {
        "TRANSPORT": "stdio",
        "INVESTEC_CLIENT_ID": "your-client-id",
        "INVESTEC_CLIENT_SECRET": "your-client-secret",
        "INVESTEC_API_KEY": "your-api-key"
      }
    }
  }
}
```

## Security Considerations

This MCP server requires sensitive banking credentials. Always:

1. Keep your `.env` file secure and never commit it to version control
2. Use secure, private Docker registries if you build and distribute container images
3. Only run the server on secure, trusted networks
4. Consider implementing additional security measures like request rate limiting

## Extending the Server

To add more functionality:

1. Add new methods to the `InvestecClient` class in `utils.py` for additional API endpoints
2. Create new tools using the `@mcp.tool()` decorator in `main.py`
3. Add any additional methods or helpers needed for your specific use case