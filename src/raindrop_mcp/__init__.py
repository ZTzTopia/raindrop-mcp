from typing import Annotated

from fastmcp import FastMCP
from pydantic import Field

from raindrop_mcp.model import (
    CollectionItem,
    RaindropCreate,
    RaindropsUpdate,
    RaindropUpdate,
)
from raindrop_mcp.raindrop import (
    create_collection,
    create_raindrop,
    # create_raindrops,
    delete_collection,
    delete_collections,
    delete_raindrop,
    delete_raindrops,
    delete_tags,
    get_collection,
    get_collections,
    get_group,
    get_groups,
    get_raindrop,
    get_raindrops,
    get_root_collections,
    get_tags,
    get_total_raindrops,
    get_user,
    merge_tags,
    rename_tag,
    update_collection,
    update_raindrop,
    update_raindrops,
)

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
    user_info = get_user()
    return (
        user_info.model_dump_json(exclude_unset=True, exclude_none=True)
        if user_info
        else {'error': 'Failed to retrieve user information.'}
    )


@mcp.tool(
    description='Get the total number of raindrops for a specific collection',
    tags=['Collections'],
)
def raindrop_get_total_raindrops(
    collection_id: Annotated[
        int,
        Field(
            description='ID of the collection to get the total count for (0 for all, -1 for unsorted, -99 for trash).'
        ),
    ],
):
    total_raindrops = get_total_raindrops(collection_id)
    return total_raindrops


@mcp.tool(
    description='Get the list of groups associated with the current user',
    tags=['Groups'],
)
def raindrop_get_groups():
    groups = get_groups()
    return (
        [group.model_dump(exclude_unset=True, exclude_none=True) for group in groups]
        if groups
        else {'error': 'No groups found.'}
    )


@mcp.tool(
    description='Get a specific group by name',
    tags=['Groups'],
)
def raindrop_get_group(
    name: Annotated[str, Field(description='Name of the group to retrieve.')],
):
    group = get_group(name)
    return (
        group.model_dump_json(exclude_unset=True, exclude_none=True)
        if group
        else {'error': f'Group "{name}" not found.'}
    )


@mcp.tool(
    description='Get the root collections of the current user',
    tags=['Collections'],
)
def raindrop_get_root_collections():
    collections = get_root_collections()
    return (
        [
            collection.model_dump(exclude_unset=True, exclude_none=True)
            for collection in collections
        ]
        if collections
        else {'error': 'Failed to retrieve root collections.'}
    )


@mcp.tool(
    description='Get all collections including children (always use this before creating a collection or raindrop)',
    tags=['Collections'],
)
def raindrop_get_collections():
    collections = get_collections()
    return (
        [
            collection.model_dump(exclude_unset=True, exclude_none=True)
            for collection in collections
        ]
        if collections
        else {'error': 'Failed to retrieve collections.'}
    )


@mcp.tool(description='Get a specific collection by ID', tags=['Collections'])
def raindrop_get_collection(
    collection_id: Annotated[
        int,
        Field(
            description='ID of the collection to retrieve (0 for root, -1 for unsorted, -99 for trash).'
        ),
    ],
):
    collection = get_collection(collection_id)
    return (
        collection.model_dump_json(exclude_unset=True, exclude_none=True)
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
            description='ID of the parent collection (0 for root, -1 for unsorted, -99 for trash).'
        ),
    ] = None,
):
    collection = create_collection(
        CollectionItem(title=title, parentId=parent_id if parent_id else None)
    )
    return (
        collection.model_dump_json(exclude_unset=True, exclude_none=True)
        if collection
        else {'error': 'Failed to create collection.'}
    )


@mcp.tool(description='Update an existing collection', tags=['Collections'])
def raindrop_update_collection(
    collection_id: Annotated[
        int,
        Field(description='ID of the collection to update.'),
    ],
    title: str,
):
    collection = update_collection(collection_id, CollectionItem(title=title))
    return (
        collection.model_dump_json(exclude_unset=True, exclude_none=True)
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
        Field(description='ID of the collection to move.'),
    ],
    parent_id: Annotated[
        int,
        Field(
            description='ID of the parent collection to move the collection to (0 for root, -1 for unsorted, -99 for trash).'
        ),
    ],
):
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
        Field(description='ID of the collection to delete.'),
    ],
):
    success = delete_collection(collection_id)
    return (
        {'message': f'Collection with ID "{collection_id}" deleted successfully.'}
        if success
        else {'error': f'Failed to delete collection with ID "{collection_id}".'}
    )


@mcp.tool(
    description='Bulk delete collections',
    tags=['Collections'],
)
def raindrop_delete_collections(
    collection_ids: Annotated[
        list[int],
        Field(description='List of collection IDs to delete.'),
    ],
):
    success = delete_collections(collection_ids)
    return (
        {'message': 'Collections deleted successfully.'}
        if success
        else {'error': 'Failed to delete collections.'}
    )


@mcp.tool(
    description='Get a specific raindrop by identifier.',
    tags=['Raindrops', 'Bookmarks'],
)
def raindrop_get_raindrop(
    raindrop_id: Annotated[
        int,
        Field(description='ID of the raindrop to retrieve.'),
    ],
):
    raindrop = get_raindrop(raindrop_id)
    return (
        raindrop.model_dump_json(exclude_unset=True, exclude_none=True)
        if raindrop
        else {'error': f'Raindrop with ID "{raindrop_id}" not found.'}
    )


# TODO: https://help.raindrop.io/using-search#operators
@mcp.tool(
    description="""
    Get a list of raindrops based on various search criteria.

    apple iphone, Find items that contains such words in title, description, domain or in web page content.
    "sample", Find items that contains exact phrase in title, description, domain or in web page content.
    #coffee, Find items that have a certain tag.
    """,
    tags=['Raindrops', 'Bookmarks'],
)
def raindrop_get_raindrops(
    collection_id: Annotated[
        int,
        Field(
            description='ID of the collection to search in (0 for all, -1 for unsorted, -99 for trash).'
        ),
    ] = 0,
    search: Annotated[str | None, Field(description='Search term.')] = None,
    page: Annotated[
        int | None, Field(description='Page number for pagination.')
    ] = None,
    perpage: Annotated[
        int | None, Field(description='Number of items per page.')
    ] = None,
    nested: Annotated[
        bool, Field(description='Whether to include nested items.')
    ] = False,
):
    raindrops = get_raindrops(collection_id, search, page, perpage, nested)
    return (
        [
            raindrop.model_dump(exclude_unset=True, exclude_none=True)
            for raindrop in raindrops
        ]
        if raindrops
        else {'error': 'No raindrops found.'}
    )


@mcp.tool(
    description='Create a new raindrop.',
    tags=['Raindrops', 'Bookmarks'],
)
def raindrop_create_raindrop(
    link: Annotated[
        str,
        Field(description='Link of the raindrop to create.'),
    ],
    collection_id: Annotated[
        int | None,
        Field(
            description='ID of the collection to create the raindrop in (-1 for unsorted, -99 for trash).'
        ),
    ] = None,
    tags: Annotated[
        list[str] | None,
        Field(description='List of tags for the raindrop.'),
    ] = None,
    important: Annotated[
        bool | None,
        Field(description='Whether to mark the raindrop as important.'),
    ] = None,
):
    raindrop = create_raindrop(
        RaindropCreate(
            link=link,
            collectionId=collection_id,
            tags=tags,
            important=important,
            pleaseParse={'weight': 1},
        )
    )
    return (
        raindrop.model_dump_json(exclude_unset=True, exclude_none=True)
        if raindrop
        else {'error': 'Failed to create raindrop.'}
    )


# @mcp.tool(
#     description='Bulk create raindrops',
#     tags=['Raindrops', 'Bookmarks'],
# )
# def raindrop_create_raindrops(
#     raindrops: Annotated[
#         list[RaindropItem],
#         Field(description='List of raindrops to create.'),
#     ],
# ):
#     created_raindrops = create_raindrops(raindrops)
#     return (
#         [raindrop.model_dump(exclude_unset=True, exclude_none=True) for raindrop in created_raindrops]
#         if created_raindrops
#         else {'error': 'Failed to create raindrops.'}
#     )


@mcp.tool(
    description='Update an existing raindrop',
    tags=['Raindrops', 'Bookmarks'],
)
def raindrop_update_raindrop(
    raindrop_id: Annotated[
        int,
        Field(description='ID of the raindrop to update.'),
    ],
    link: Annotated[
        str | None,
        Field(description='Link of the raindrop to update.'),
    ] = None,
    tags: Annotated[
        list[str] | None,
        Field(description='List of tags for the raindrop.'),
    ] = None,
    important: Annotated[
        bool | None,
        Field(description='Whether to mark the raindrop as important.'),
    ] = None,
):
    raindrop = update_raindrop(
        raindrop_id,
        RaindropUpdate(
            link=link,
            tags=tags,
            important=important,
            pleaseParse={'weight': 1} if link else None,
        ),
    )
    return (
        raindrop.model_dump_json(exclude_unset=True, exclude_none=True)
        if raindrop
        else {'error': f'Failed to update raindrop with ID "{raindrop_id}".'}
    )


@mcp.tool(
    description='Bulk update raindrops in a collection',
    tags=['Raindrops', 'Bookmarks'],
)
def raindrop_update_raindrops(
    collection_id: Annotated[
        int,
        Field(
            description='ID of the collection to update raindrops in. (0 for all but trash excluded).'
        ),
    ],
    raindrop_ids: Annotated[
        list[int] | None,
        Field(description='List of raindrop IDs to update.'),
    ] = None,
    tags: Annotated[
        list[str] | None,
        Field(description='List of tags to apply to the raindrops.'),
    ] = None,
    important: Annotated[
        bool | None,
        Field(description='Whether to mark the raindrops as important.'),
    ] = None,
    search: Annotated[
        str | None,
        Field(description='Search term to filter raindrops to update.'),
    ] = None,
    nested: Annotated[
        bool, Field(description='Whether to include nested items in the update.')
    ] = False,
):
    modified = update_raindrops(
        collection_id,
        RaindropsUpdate(
            ids=raindrop_ids,
            tags=tags,
            important=important,
        ),
        nested,
        search,
    )
    return {
        'modified': modified if modified else {'error': 'Failed to update raindrops.'}
    }


@mcp.tool(
    description='Move a raindrop to another collection',
    tags=['Raindrops', 'Bookmarks'],
)
def raindrop_move_raindrop(
    raindrop_id: Annotated[
        int,
        Field(description='ID of the raindrop to move.'),
    ],
    collection_id: Annotated[
        int,
        Field(
            description='ID of the collection to move the raindrop to (-1 for unsorted, -99 for trash).'
        ),
    ],
):
    raindrop = update_raindrop(raindrop_id, RaindropUpdate(collectionId=collection_id))
    return (
        {'message': f'Raindrop with ID "{raindrop_id}" moved successfully.'}
        if raindrop
        else {'error': f'Failed to move raindrop with ID "{raindrop_id}".'}
    )


@mcp.tool(
    description='Bulk move raindrops to another collection',
    tags=['Raindrops', 'Bookmarks'],
)
def raindrop_move_raindrops(
    collection_id: Annotated[
        int,
        Field(
            description='ID of the collection to move raindrops to (0 for all but trash excluded).'
        ),
    ],
    target_collection_id: Annotated[
        int,
        Field(
            description='ID of the target collection to move the raindrops to. (-1 for unsorted, -99 for trash).'
        ),
    ],
    search: Annotated[
        str | None,
        Field(description='Search term to filter raindrops to move.'),
    ] = None,
    raindrop_ids: Annotated[
        list[int] | None,
        Field(description='List of raindrop IDs to move.'),
    ] = None,
    nested: Annotated[
        bool, Field(description='Whether to include nested items in the move.')
    ] = False,
):
    modified = update_raindrops(
        collection_id,
        RaindropsUpdate(ids=raindrop_ids, collectionId=target_collection_id),
        nested=nested,
        search=search,
    )
    return (
        {'modified': modified} if modified else {'error': 'Failed to move raindrops.'}
    )


@mcp.tool(
    description='Delete a specific raindrop',
    tags=['Raindrops', 'Bookmarks'],
)
def raindrop_delete_raindrop(
    raindrop_id: Annotated[int, Field(description='ID of the raindrop to delete.')],
    permanent: Annotated[
        bool, Field(description='Whether to permanently delete the raindrop.')
    ] = False,
):
    success = delete_raindrop(raindrop_id, permanent)
    return (
        {'message': f'Raindrop with ID "{raindrop_id}" deleted successfully.'}
        if success
        else {'error': f'Failed to delete raindrop with ID "{raindrop_id}".'}
    )


@mcp.tool(
    description='Bulk delete raindrops',
    tags=['Raindrops', 'Bookmarks'],
)
def raindrop_delete_raindrops(
    collection_id: Annotated[
        int,
        Field(
            description='ID of the collection containing the raindrops to delete (0 for all but trash excluded, -99 to delete from trash).'
        ),
    ],
    search: Annotated[
        str | None,
        Field(description='Search term to filter raindrops to delete.'),
    ] = None,
    raindrop_ids: Annotated[
        list[int] | None,
        Field(description='List of raindrop IDs to delete.'),
    ] = None,
    permanent: Annotated[
        bool,
        Field(description='Whether to permanently delete the raindrops.'),
    ] = False,
):
    modified = delete_raindrops(collection_id, False, search, raindrop_ids, permanent)
    return (
        {'modified': modified} if modified else {'error': 'Failed to delete raindrops.'}
    )


@mcp.tool(
    description='Get tags for a collection',
    tags=['Raindrops', 'Bookmarks'],
)
def raindrop_get_tags(
    collection_id: Annotated[
        int,
        Field(
            description='ID of the collection to get tags for (0 for all, -1 for unsorted, -99 for trash).'
        ),
    ] = 0,
):
    tags = get_tags(collection_id)
    return (
        [tag.model_dump(exclude_unset=True, exclude_none=True) for tag in tags]
        if tags
        else {'error': 'No tags found.'}
    )


@mcp.tool(
    description='Rename a tag',
    tags=['Raindrops', 'Bookmarks'],
)
def raindrop_rename_tag(
    replace: Annotated[
        str,
        Field(description='Tag to replace.'),
    ],
    tags: Annotated[
        str,
        Field(description='New tag name.'),
    ],
    collection_id: Annotated[
        int,
        Field(
            description='ID of the collection to rename the tag in (0 for all, -1 for unsorted, -99 for trash).'
        ),
    ] = 0,
):
    success = rename_tag(replace, tags, collection_id)
    return (
        {'message': f'Tag "{replace}" renamed to "{tags}" successfully.'}
        if success
        else {'error': f'Failed to rename tag "{replace}".'}
    )


@mcp.tool(
    description='Merge tags',
    tags=['Raindrops', 'Bookmarks'],
)
def raindrop_merge_tags(
    replace: Annotated[
        str,
        Field(description='Tag to replace.'),
    ],
    tags: Annotated[
        list[str],
        Field(description='List of tags to merge.'),
    ],
    collection_id: Annotated[
        int,
        Field(
            description='ID of the collection to merge tags in (0 for all, -1 for unsorted, -99 for trash).'
        ),
    ] = 0,
):
    success = merge_tags(replace, tags, collection_id)
    return (
        {'message': 'Tags merged successfully.'}
        if success
        else {'error': 'Failed to merge tags.'}
    )


@mcp.tool(
    description='Delete a tag',
    tags=['Raindrops', 'Bookmarks'],
)
def raindrop_delete_tag(
    tags: Annotated[
        list[str],
        Field(description='List of tags to delete.'),
    ],
    collection_id: Annotated[
        int,
        Field(
            description='ID of the collection to delete the tag from (0 for all, -1 for unsorted, -99 for trash).'
        ),
    ] = 0,
):
    success = delete_tags(tags, collection_id)
    return (
        {'message': 'Tags deleted successfully.'}
        if success
        else {'error': 'Failed to delete tags.'}
    )


def main():
    mcp.run()
