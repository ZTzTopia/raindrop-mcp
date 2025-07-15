# Raindrop MCP Server

This project provides a server for integrating with [Raindrop.io](https://raindrop.io), a bookmarking and collection management service. It uses the FastMCP framework to expose tools for interacting with Raindrop.io's API.

## Features

- Fetch user information.
- Manage collections (create, update, delete, move).
- Manage raindrops (create, update, delete, search).
- Fetch groups and collections.
- Search for raindrops.
- Manage tags (rename, merge, delete).

### Tools

The server exposes the following tools:

- **User Tools**:
  - `raindrop_get_user`: Fetch the current user's information.

- **Groups Tools**:
  - `raindrop_get_groups`: Get all groups for the current user.
  - `raindrop_get_group`: Get a specific group by name.

- **Collection Tools**:
  - `raindrop_get_top_collections`: Get top-level collections.
  - `raindrop_get_collections`: Get all collections including children.
  - `raindrop_get_collection`: Fetch a specific collection by ID.
  - `raindrop_create_collection`: Create a new collection.
  - `raindrop_update_collection`: Update an existing collection.
  - `raindrop_move_collection`: Move a collection to another collection.
  - `raindrop_delete_collection`: Delete a specific collection.
  - `raindrop_delete_collections`: Delete multiple collections.

- **Raindrop Tools**:
  - `raindrop_get_total_raindrops`: Get the total number of raindrops for a collection.
  - `raindrop_get_raindrop`: Fetch a specific raindrop by ID.
  - `raindrop_get_raindrops`: Get raindrops with search capabilities.
  - `raindrop_create_raindrop`: Create a new raindrop.
  - `raindrop_update_raindrop`: Update an existing raindrop.
  - `raindrop_move_raindrop`: Move a raindrop to another collection.
  - `raindrop_update_raindrops`: Bulk update raindrops in a collection.
  - `raindrop_move_raindrops`: Bulk move raindrops to another collection.
  - `raindrop_delete_raindrop`: Delete a specific raindrop.
  - `raindrop_delete_raindrops`: Bulk delete raindrops.

- **Tag Tools**:
  - `raindrop_get_tags`: Get tags for a collection.
  - `raindrop_rename_tag`: Rename a tag.
  - `raindrop_merge_tags`: Merge tags.
  - `raindrop_delete_tag`: Delete a tag.

## Acknowledgments

- [Raindrop.io](https://raindrop.io) for their API.
- [FastMCP](https://gofastmcp.com) for the framework used in this project.