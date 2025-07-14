# Raindrop MCP Server

This project provides a server for integrating with [Raindrop.io](https://raindrop.io), a bookmarking and collection management service. It uses the FastMCP framework to expose tools for interacting with Raindrop.io's API.

## Features

- Fetch user information.
- Manage collections (create, update, delete, move).
- Manage raindrops (create, update, delete, search).
- Fetch groups and collections.
- Search for raindrops.

### Tools

The server exposes the following tools:

- **User Tools**:
  - `raindrop_get_user`: Fetch the current user's information.

- **Collection Tools**:
  - `raindrop_get_total_collections`: Get the total number of collections.
  - `raindrop_get_root_collections`: Fetch root collections.
  - `raindrop_get_collections`: Fetch all collections.
  - `raindrop_get_collection`: Fetch a specific collection by ID.
  - `raindrop_create_collection`: Create a new collection.
  - `raindrop_update_collection`: Update an existing collection.
  - `raindrop_move_collection`: Move a collection to another collection.
  - `raindrop_delete_collection`: Delete a specific collection.
  - `raindrop_delete_collections`: Delete multiple collections.

- **Raindrop Tools**:
  - `raindrop_get_raindrop`: Fetch a specific raindrop by ID.
  - `raindrop_search_raindrops`: Search for raindrops.
  - `raindrop_create_raindrop`: Create a new raindrop.
  - `raindrop_update_raindrop`: Update an existing raindrop.
  - `raindrop_delete_raindrop`: Delete a specific raindrop.

## Acknowledgments

- [Raindrop.io](https://raindrop.io) for their API.
- [FastMCP](https://github.com/fastmcp) for the framework used in this project.
