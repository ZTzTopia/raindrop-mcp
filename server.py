from typing import Annotated, Literal

from fastmcp import FastMCP
from pydantic import Field

from raindrop import (
    create_collection,
    create_raindrop,
    delete_collection,
    delete_collections,
    delete_raindrop,
    get_collection,
    get_collections,
    get_group,
    get_groups,
    get_raindrop,
    get_raindrops,
    get_root_collections,
    get_total_collections,
    get_user,
    update_collection,
    update_raindrop,
)
from type import CollectionItem, RaindropItem

mcp = FastMCP(
    name='Raindrop MCP Server',
    instructions="""
    This is a server for Raindrop.io integration.
    """,
    version='0.1.0',
    include_tags=['Raindrops', 'Bookmarks', 'Collections', 'Groups', 'User'],
)


@mcp.tool(
    description="Get the current user's information from Raindrop.io",
    tags=['User'],
)
def raindrop_get_user():
    """
    Get the current user's information from Raindrop.io.

    :return: User information or an error message.
    """
    user_info = get_user()
    return (
        user_info.model_dump_json()
        if user_info
        else {'error': 'Failed to retrieve user information.'}
    )


@mcp.tool(
    description='Get the total number of collections for a specific type',
    tags=['Collections'],
)
def raindrop_get_total_collections(
    collection_type: Literal['all', 'unsorted', 'trash'] = 'all',
):
    """
    Get the total number of collections for a specific type.

    :param collection_type: Type of collections to count ('all', 'unsorted', 'trash').
    :return: Total count of collections.
    """
    total_collections = get_total_collections(collection_type)
    return total_collections


@mcp.tool(
    description='Get the list of groups associated with the current user',
    tags=['Groups'],
)
def raindrop_get_groups():
    """
    Get the list of groups associated with the current user.

    :return: List of groups or an error message.
    """
    groups = get_groups()
    return (
        [group.model_dump() for group in groups]
        if groups
        else {'error': 'No groups found.'}
    )


@mcp.tool(
    description='Get a specific group by name',
    tags=['Groups'],
)
def raindrop_get_group(name: str):
    """
    Get a specific group by name.

    :param name: Name of the group to retrieve.
    :return: Group information or an error message.
    """
    group = get_group(name)
    return group.model_dump_json() if group else {'error': f'Group "{name}" not found.'}


@mcp.tool(
    description='Get the root collections of the current user',
    tags=['Collections'],
)
def raindrop_get_root_collections():
    """
    Fetch root collections.

    :return: List of root collections or an error message.
    """
    collections = get_root_collections()
    return (
        [collection.model_dump() for collection in collections]
        if collections
        else {'error': 'Failed to retrieve root collections.'}
    )


@mcp.tool(
    description='Get all collections including children (always use this before creating a collection or raindrop)',
    tags=['Collections'],
)
def raindrop_get_collections():
    """
    Fetch all collections, including children.

    :return: List of all collections or an error message.
    """
    collections = get_collections()
    return (
        [collection.model_dump() for collection in collections]
        if collections
        else {'error': 'Failed to retrieve collections.'}
    )


@mcp.tool(description='Get a specific collection by ID', tags=['Collections'])
def raindrop_get_collection(
    collection_id: Annotated[
        int,
        Field(
            description='Execute a query on Collection to retrieve the ID; if none is found, abort.'
        ),
    ],
):
    """
    Get a specific collection by ID.

    :param collection_id: ID of the collection to retrieve.
    :return: Collection information or an error message.
    """
    collection = get_collection(collection_id)
    return (
        collection.model_dump_json()
        if collection
        else {'error': f'Collection with ID "{collection_id}" not found.'}
    )


@mcp.tool(
    description='Create a new collection',
    tags=['Collections'],
)
def raindrop_create_collection(
    title: str,
    parent_id: Annotated[
        int,
        Field(
            description='Execute a query on Collection to retrieve the ID; if none is found, abort.'
        ),
    ] = None,
):
    """
    Create a new collection.

    :param title: Title of the new collection.
    :param parent_id: ID of the parent collection (optional).
    :return: Created collection information or an error message.
    """
    collection = create_collection(
        CollectionItem(title=title, parentId=parent_id if parent_id else None)
    )
    return (
        collection.model_dump_json()
        if collection
        else {'error': 'Failed to create collection.'}
    )


@mcp.tool(description='Update an existing collection', tags=['Collections'])
def raindrop_update_collection(
    collection_id: Annotated[
        int,
        Field(
            description='Execute a query on Collection to retrieve the ID; if none is found, abort.'
        ),
    ],
    title: str,
):
    """
    Update an existing collection.

    :param collection_id: ID of the collection to update.
    :param title: New title for the collection (optional).
    :return: Updated collection information or an error message.
    """
    collection = update_collection(collection_id, CollectionItem(title=title))
    return (
        collection.model_dump_json()
        if collection
        else {'error': f'Failed to update collection with ID "{collection_id}".'}
    )


@mcp.tool(
    description='Move a collection to other collection',
    tags=['Collections'],
)
def raindrop_move_collection(
    collection_id: Annotated[
        int,
        Field(
            description='Execute a query on Collection to retrieve the ID; if none is found, abort.'
        ),
    ],
    parent_id: Annotated[
        int,
        Field(
            description='Execute a query on Collection to retrieve the ID; if none is found, abort.'
        ),
    ],
):
    """
    Move a collection to another collection.

    :param collection_id: ID of the collection to move.
    :param parent_id: ID of the parent collection to move to.
    :return: Success message or an error message.
    """
    collection = update_collection(collection_id, CollectionItem(parentId=parent_id))
    return (
        {'message': f'Collection with ID "{collection_id}" moved successfully.'}
        if collection
        else {'error': f'Failed to move collection with ID "{collection_id}".'}
    )


@mcp.tool(
    description='Delete a specific collection',
    tags=['Collections'],
)
def raindrop_delete_collection(
    collection_id: Annotated[
        int,
        Field(
            description='Execute a query on Collection to retrieve the ID; if none is found, abort.'
        ),
    ],
):
    """
    Delete a specific collection.

    :param collection_id: ID of the collection to delete.
    :return: Success message or an error message.
    """
    success = delete_collection(collection_id)
    return (
        {'message': f'Collection with ID "{collection_id}" deleted successfully.'}
        if success
        else {'error': f'Failed to delete collection with ID "{collection_id}".'}
    )


@mcp.tool(
    description='Delete multiple collections',
    tags=['Collections'],
)
def raindrop_delete_collections(
    collection_ids: Annotated[
        list[int],
        Field(
            description='Execute a query on Collection to retrieve the IDs; if none are found, abort.'
        ),
    ],
):
    """
    Delete multiple collections.

    :param collection_ids: List of IDs of the collections to delete.
    :return: Success message or an error message.
    """
    success = delete_collections(collection_ids)
    return (
        {'message': 'Collections deleted successfully.'}
        if success
        else {'error': 'Failed to delete collections.'}
    )


@mcp.tool(
    description='Get a specific raindrop by ID',
    tags=['Raindrops', 'Bookmarks'],
    annotations={'raindrop_id': 'ID of the raindrop to retrieve.'},
)
def raindrop_get_raindrop(raindrop_id: int):
    """
    Get a specific raindrop by ID.

    :param raindrop_id: ID of the raindrop to retrieve.
    :return: Raindrop information or an error message.
    """
    raindrop = get_raindrop(raindrop_id)
    return (
        raindrop.model_dump_json()
        if raindrop
        else {'error': f'Raindrop with ID "{raindrop_id}" not found.'}
    )


# # TODO: https://help.raindrop.io/using-search#operators
@mcp.tool(
    description='Search for raindrops',
    tags=['Raindrops', 'Bookmarks'],
    annotations={
        'collection_id': 'ID of the collection to search in (0 for all, -1 for unsorted, -99 for trash).',
        'search': 'Search term.',
        'page': 'Page number for pagination.',
        'perpage': 'Number of items per page.',
        'nested': 'Whether to include nested items.',
    },
)
def raindrop_search_raindrops(
    collection_id: int = 0,
    search: str = '',
    page: int = 0,
    perpage: int = 20,
    nested: bool = False,
):
    """
    Search for raindrops.

    :param collection_id: ID of the collection to search in (0 for all).
    :param search: Search term.
    :param page: Page number for pagination.
    :param perpage: Number of items per page.
    :param nested: Whether to include nested items.
    :return: List of raindrops or an error message.
    """
    raindrops = get_raindrops(collection_id, search, page, perpage, nested)
    return (
        [raindrop.model_dump() for raindrop in raindrops]
        if raindrops
        else {'error': 'No raindrops found.'}
    )


@mcp.tool(
    description='Create a new raindrop',
    tags=['Raindrops', 'Bookmarks'],
    annotations={
        'collection_id': 'ID of the collection to add the raindrop to (default: 0).',
        'link': 'Link of the raindrop.',
        'tags': 'List of tags for the raindrop (optional).',
    },
)
def raindrop_create_raindrop(
    collection_id: int = 0, link: str = None, tags: list = None
):
    """
    Create a new raindrop.

    :param collection_id: ID of the collection to add the raindrop to.
    :param link: Link of the raindrop.
    :param tags: List of tags for the raindrop (optional).
    :return: Created raindrop information or an error message.
    """
    raindrop = create_raindrop(
        RaindropItem(link=link, collectionId=collection_id, tags=tags or [])
    )
    return (
        raindrop.model_dump_json()
        if raindrop
        else {'error': 'Failed to create raindrop.'}
    )


@mcp.tool(
    description='Update an existing raindrop',
    tags=['Raindrops', 'Bookmarks'],
)
def raindrop_update_raindrop(
    raindrop_id: int,
    collection_id: int = None,
    link: str = None,
    tags: list = None,
):
    raindrop = update_raindrop(
        raindrop_id,
        RaindropItem(
            link=link,
            collectionId=collection_id if collection_id else None,
            tags=tags or [],
        ),
    )
    return (
        raindrop.model_dump_json()
        if raindrop
        else {'error': f'Failed to update raindrop with ID "{raindrop_id}".'}
    )


@mcp.tool(
    description='Delete a specific raindrop',
    tags=['Raindrops', 'Bookmarks'],
)
def raindrop_delete_raindrop(
    id: int,
):
    success = delete_raindrop(id)
    return (
        {'message': f'Raindrop with ID "{id}" deleted successfully.'}
        if success
        else {'error': f'Failed to delete raindrop with ID "{id}".'}
    )


if __name__ == '__main__':
    mcp.run()
