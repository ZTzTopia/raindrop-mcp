from typing import Annotated, Optional

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
    delete_collections,
    delete_raindrop,
    delete_raindrops,
    delete_tags,
    get_collection,
    get_collections,
    get_groups,
    get_raindrop,
    get_raindrops,
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
    description='Get the list of groups associated with the current user, optionally filtered by name',
    tags=['Groups'],
)
def raindrop_get_groups(
    name: Annotated[
        Optional[str],
        Field(description='Name of the group to filter by.'),
    ] = None,
):
    groups = get_groups()
    if not groups:
        return {'error': 'No groups found.'}

    if name:
        groups = [g for g in groups if g.title == name]
        if not groups:
            return {'error': f'Group "{name}" not found.'}

    return [group.model_dump(exclude_unset=True, exclude_none=True) for group in groups]


@mcp.tool(
    description='Get all collections or specific collections by ID',
    tags=['Collections'],
)
def raindrop_get_collections(
    collection_ids: Annotated[
        Optional[list[int]],
        Field(description='List of collection IDs to retrieve. If not provided, returns all collections.'),
    ] = None,
):
    if collection_ids:
        results = []
        for cid in collection_ids:
            collection = get_collection(cid)
            if collection:
                results.append(collection.model_dump(exclude_unset=True, exclude_none=True))
        return results if results else {'error': 'No collections found for the provided IDs.'}
    
    collections = get_collections()
    return (
        [
            collection.model_dump(exclude_unset=True, exclude_none=True)
            for collection in collections
        ]
        if collections
        else {'error': 'Failed to retrieve collections.'}
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


@mcp.tool(description='Update an existing collection (rename or move)', tags=['Collections'])
def raindrop_update_collection(
    collection_id: Annotated[
        int,
        Field(description='ID of the collection to update.'),
    ],
    title: Annotated[
        Optional[str],
        Field(description='New title for the collection.'),
    ] = None,
    parent_id: Annotated[
        Optional[int],
        Field(description='New parent ID to move the collection to.'),
    ] = None,
):
    update_data = CollectionItem()
    if title is not None:
        update_data.title = title
    if parent_id is not None:
        update_data.parentId = parent_id

    collection = update_collection(collection_id, update_data)
    return (
        collection.model_dump_json(exclude_unset=True, exclude_none=True)
        if collection
        else {'error': f'Failed to update collection with ID "{collection_id}".'}
    )


@mcp.tool(
    description='Delete collections (single or bulk)',
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


# TODO: https://help.raindrop.io/using-search#operators
@mcp.tool(
    description="""
    Get raindrops. Can retrieve by specific IDs OR search within a collection.
    
    If `raindrop_ids` is provided, fetches those specific raindrops.
    Otherwise, searches in `collection_id` using `search` term.

    Search examples:
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
            description='ID of the collection to search in (0 for all, -1 for unsorted, -99 for trash). Ignored if raindrop_ids is provided.'
        ),
    ] = 0,
    raindrop_ids: Annotated[
        Optional[list[int]],
        Field(description='List of specific raindrop IDs to retrieve.'),
    ] = None,
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
    if raindrop_ids:
        results = []
        for rid in raindrop_ids:
            raindrop = get_raindrop(rid)
            if raindrop:
                results.append(raindrop.model_dump(exclude_unset=True, exclude_none=True))
        return results if results else {'error': 'No raindrops found for the provided IDs.'}

    raindrops_response = get_raindrops(collection_id, search, page, perpage, nested)
    if not raindrops_response:
        return {'error': 'No raindrops found.'}

    return {
        'items': [
            raindrop.model_dump(exclude_unset=True, exclude_none=True)
            for raindrop in raindrops_response.items
        ],
        'count': raindrops_response.count,
    }


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


@mcp.tool(
    description='Update an existing raindrop (change properties or move)',
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
    collection_id: Annotated[
        Optional[int],
        Field(description='ID of the collection to move the raindrop to.'),
    ] = None,
):
    raindrop = update_raindrop(
        raindrop_id,
        RaindropUpdate(
            link=link,
            tags=tags,
            important=important,
            collectionId=collection_id,
            pleaseParse={'weight': 1} if link else None,
        ),
    )
    return (
        raindrop.model_dump_json(exclude_unset=True, exclude_none=True)
        if raindrop
        else {'error': f'Failed to update raindrop with ID "{raindrop_id}".'}
    )


@mcp.tool(
    description='Bulk update raindrops in a collection (change properties or move)',
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
    target_collection_id: Annotated[
        Optional[int],
        Field(description='ID of the target collection to move the raindrops to.'),
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
            collectionId=target_collection_id,
        ),
        nested,
        search,
    )
    return {
        'modified': modified if modified else {'error': 'Failed to update raindrops.'}
    }


@mcp.tool(
    description='Delete raindrops (single or bulk)',
    tags=['Raindrops', 'Bookmarks'],
)
def raindrop_delete_raindrops(
    raindrop_ids: Annotated[
        list[int],
        Field(description='List of raindrop IDs to delete.'),
    ],
    collection_id: Annotated[
        Optional[int],
        Field(
            description='ID of the collection containing the raindrops (0 for all but trash excluded). Required for bulk deletion optimization, but optional if deleting by ID one by one.'
        ),
    ] = None,
    search: Annotated[
        str | None,
        Field(description='Search term to filter raindrops to delete (requires collection_id).'),
    ] = None,
    permanent: Annotated[
        bool,
        Field(description='Whether to permanently delete the raindrops.'),
    ] = False,
):
    # If collection_id is provided, use the bulk endpoint
    if collection_id is not None:
        modified = delete_raindrops(collection_id, False, search, raindrop_ids, permanent)
        return (
            {'modified': modified} if modified else {'error': 'Failed to delete raindrops.'}
        )
    
    # If no collection_id, delete one by one (less efficient but flexible)
    if raindrop_ids:
        count = 0
        for rid in raindrop_ids:
            if delete_raindrop(rid, permanent):
                count += 1
        return {'modified': count}
    
    return {'error': 'Either collection_id or raindrop_ids must be provided.'}


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
    description='Update tags (rename or merge)',
    tags=['Raindrops', 'Bookmarks'],
)
def raindrop_update_tags(
    target_tag: Annotated[
        str,
        Field(description='The new tag name (target).'),
    ],
    source_tags: Annotated[
        list[str],
        Field(description='List of tags to be renamed or merged into the target tag.'),
    ],
    collection_id: Annotated[
        int,
        Field(
            description='ID of the collection to update tags in (0 for all, -1 for unsorted, -99 for trash).'
        ),
    ] = 0,
):
    # If only one source tag, it's a rename
    if len(source_tags) == 1:
        success = rename_tag(source_tags[0], target_tag, collection_id)
        return (
            {'message': f'Tag "{source_tags[0]}" renamed to "{target_tag}" successfully.'}
            if success
            else {'error': f'Failed to rename tag "{source_tags[0]}".'}
        )
    
    # If multiple source tags, it's a merge
    success = merge_tags(target_tag, source_tags, collection_id)
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
