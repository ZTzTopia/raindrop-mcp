# Raindrop MCP Server

This project provides a server for integrating with [Raindrop.io](https://raindrop.io), a bookmarking and collection management service. It uses the FastMCP framework to expose tools for interacting with Raindrop.io's API.

## Features

- Fetch user information.
- Manage collections (create, update, delete, move).
- Manage raindrops (create, update, delete, search).
- Fetch groups and collections.
- Search for raindrops.
- Manage tags (rename, merge, delete).

## Installation

### Using uv (Recommended)

```bash
git clone https://github.com/ZTzTopia/raindrop-mcp
cd raindrop-mcp

uv venv create
uv venv activate
uv sync
```

## Development

To run the server in development mode with hot-reloading and the MCP Inspector:

```bash
# Run in dev mode using uv
uv run --with fastmcp fastmcp dev --server-spec src/raindrop_mcp/__init__.py
```

## Configuration

Add the server to your Claude Desktop configuration file:

**MacOS**: `~/Library/Application Support/Claude/claude_desktop_config.json`

```json
{
  "mcpServers": {
    "raindrop": {
      "command": "uv",
      "args": [
        "--directory",
        "/ABSOLUTE/PATH/TO/raindrop-mcp",
        "run",
        "raindrop-mcp"
      ],
      "env": {
        "RAINDROP_ACCESS_TOKEN": "YOUR_TEST_TOKEN_HERE"
      }
    }
  }
}
```

## Tools

The server exposes the following optimized tools:

- **User Tools**:
  - `raindrop_get_user`: Fetch the current user's information.

- **Groups Tools**:
  - `raindrop_get_groups`: Get all groups or filter by name.

- **Collection Tools**:
  - `raindrop_get_collections`: Get all collections or specific ones by ID.
  - `raindrop_create_collection`: Create a new collection.
  - `raindrop_update_collection`: Update (rename/move) an existing collection.
  - `raindrop_delete_collections`: Delete collections (single or bulk).

- **Raindrop Tools**:
  - `raindrop_get_total_raindrops`: Get the total number of raindrops for a collection.
  - `raindrop_get_raindrops`: Get raindrops by ID or search within a collection.
  - `raindrop_create_raindrop`: Create a new raindrop.
  - `raindrop_update_raindrop`: Update (properties/move) an existing raindrop.
  - `raindrop_update_raindrops`: Bulk update (properties/move) raindrops.
  - `raindrop_delete_raindrops`: Delete raindrops (single or bulk).

- **Tag Tools**:
  - `raindrop_get_tags`: Get tags for a collection.
  - `raindrop_update_tags`: Rename or merge tags.
  - `raindrop_delete_tag`: Delete tags.

## Acknowledgments

- [Raindrop.io](https://raindrop.io) for their API.
- [FastMCP](https://gofastmcp.com) for the framework used in this project.
