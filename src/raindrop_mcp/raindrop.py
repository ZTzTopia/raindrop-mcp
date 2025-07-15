import os

import requests

from raindrop_mcp.model import (
    Collection,
    CollectionItem,
    CollectionItems,
    Group,
    RaindropCreate,
    RaindropResponse,
    RaindropsResponse,
    RaindropsUpdate,
    RaindropUpdate,
    Tag,
    Tags,
    UpdateDeleteRaindropsResponse,
    User,
)

URL = 'https://api.raindrop.io/rest/v1'
RAINDROP_ACCESS_TOKEN = os.getenv('RAINDROP_ACCESS_TOKEN')

session = requests.Session()
session.headers = {'Authorization': f'Bearer {RAINDROP_ACCESS_TOKEN}'}


def make_request(method, endpoint, **kwargs) -> dict | None:
    response = session.request(method, f'{URL}/{endpoint}', **kwargs)
    response.raise_for_status()

    data = response.json()
    return data


def get_user() -> User | None:
    data = make_request('GET', 'user')
    return User(**data).user if data else None


def get_groups() -> list[Group] | None:
    user = get_user()
    return user.groups if user else None


def get_group(name: str):
    groups = get_groups()
    return (
        next((group for group in groups if group.title == name), None)
        if groups
        else None
    )


def get_top_collections(
    flat: bool = False,
) -> list[Group] | list[CollectionItem] | None:
    data = make_request('GET', 'collections')
    if not data:
        return None

    collections = CollectionItems(**data)
    if flat:
        return collections.items

    groups = get_groups()
    if not groups:
        return None

    for group in groups:
        group.items = [c for c in collections.items if c.id in group.collections]
        group.collections = None

    # FIXME: We need another request to user endpoint after creating collection
    #       to make this item available in groups.
    if groups:
        ungrouped_items = [
            c for c in collections.items if all(c.id not in g.items for g in groups)
        ]
        groups[0].items.extend(ungrouped_items)

    return groups


def get_collections() -> list[Group] | None:
    data = make_request('GET', 'collections/all')
    if not data:
        return None

    collections = CollectionItems(**data)
    if not collections.items:
        return None

    collections_map = {item.id: item for item in collections.items}

    root_items: list[CollectionItem] = []
    for item in collections_map.values():
        parent = item.parent
        if not parent:
            root_items.append(item)
            continue

        parent_id = parent.id
        if parent_id and parent_id in collections_map:
            parent = collections_map[parent_id]
            if not parent.items:
                parent.items = []

            parent.items.append(item)
            continue

        root_items.append(item)

    groups = get_groups()
    if not groups:
        return None

    for group in groups:
        group.items = [c for c in root_items if c.id in group.collections]
        group.collections = None

    # FIXME: We need another request to user endpoint after creating collection
    #       to make this item available in groups.
    if groups:
        ungrouped_items = [
            c for c in root_items if all(c.id not in g.items for g in groups)
        ]
        groups[0].items.extend(ungrouped_items)

    return groups


def get_collection(id: int) -> CollectionItem | None:
    data = make_request('GET', f'collection/{id}')
    return Collection(**data).item if data else None


def get_total_raindrops(
    collection_id: int = 0,
) -> dict | None:
    stats = make_request('GET', 'user/stats')
    if not stats:
        return None

    if collection_id not in [0, -1, -99]:
        collection = get_collection(collection_id)
        return {
            'count': collection.count if collection else 0,
        }

    return {
        'count': next(
            (
                item.get('count', 0)
                for item in stats.get('items', [])
                if item.get('_id') == collection_id
            ),
            0,
        )
    }


def create_collection(collection: CollectionItem) -> CollectionItem | None:
    data = make_request(
        'POST',
        'collection',
        json=collection.model_dump(exclude_unset=True, exclude_none=True),
    )
    return Collection(**data).item if data else None


def update_collection(id: int, collection: CollectionItem) -> CollectionItem | None:
    data = make_request(
        'PUT',
        f'collection/{id}',
        json=collection.model_dump(exclude_unset=True, exclude_none=True),
    )
    return Collection(**data).item if data else None


def delete_collection(id: int):
    data = make_request('DELETE', f'collection/{id}')
    return True if data else False


def delete_collections(ids: list):
    payload = {'ids': ids}
    data = make_request('DELETE', 'collections', json=payload)
    return True if data else False


def get_raindrop(raindrop_id: int):
    data = make_request('GET', f'raindrop/{raindrop_id}')
    return RaindropResponse(**data).item if data else None


def get_raindrops(
    collection_id: int = 0,
    search: str | None = None,
    page: int | None = None,
    perpage: int | None = None,
    nested: bool = False,
):
    params = {'nested': nested}
    if search:
        params['search'] = search
    if page is not None:
        params['page'] = page
    if perpage is not None:
        params['perpage'] = perpage

    data = make_request('GET', f'raindrops/{collection_id}', params=params)
    return RaindropsResponse(**data).items if data else None


def create_raindrop(raindrop: RaindropCreate):
    data = make_request(
        'POST',
        'raindrop',
        json=raindrop.model_dump(exclude_unset=True, exclude_none=True),
    )
    return RaindropResponse(**data).item if data else None


# def create_raindrops(raindrop: list[RaindropItem]) -> list[RaindropItem] | None:
#     data = make_request(
#         'POST',
#         'raindrops',
#         json={
#             'items': [
#                 item.model_dump(exclude_unset=True, exclude_none=True)
#                 for item in raindrop
#             ]
#         },
#     )
#     return [Raindrop(**item) for item in data] if data else None


def update_raindrop(raindrop_id: int, raindrop: RaindropUpdate):
    data = make_request(
        'PUT',
        f'raindrop/{raindrop_id}',
        json=raindrop.model_dump(exclude_unset=True, exclude_none=True),
    )
    return RaindropResponse(**data).item if data else None


def update_raindrops(
    collection_id: int,
    raindrop: RaindropsUpdate,
    nested: bool = False,
    search: str | None = None,
):
    params = {'search': search, 'nested': nested} if search else {}
    data = make_request(
        'PUT',
        f'raindrops/{collection_id}',
        params=params,
        json=raindrop.model_dump(exclude_unset=True, exclude_none=True),
    )
    return UpdateDeleteRaindropsResponse(**data).modified if data else None


def delete_raindrop(
    raindrop_id: int,
    permanent: bool = False,
):
    data = make_request('DELETE', f'raindrop/{raindrop_id}')
    if permanent:
        if not data:
            raise ValueError('Failed to delete raindrop, no data returned.')

        data = make_request('DELETE', f'raindrop/{raindrop_id}')

    return True if data else False


def delete_raindrops(
    collection_id: int,
    nested: bool = False,
    search: str | None = None,
    raindrop_ids: list[int] | None = None,
    permanent: bool = False,
):
    params = {'search': search, 'nested': nested} if search else {}
    payload = {'ids': raindrop_ids} if raindrop_ids else {}

    data = make_request(
        'DELETE', f'raindrops/{collection_id}', params=params, json=payload
    )
    if permanent:
        if not data:
            raise ValueError('Failed to delete raindrops, no data returned.')

        data = make_request('DELETE', 'raindrops/-99', params=params, json=payload)

    return UpdateDeleteRaindropsResponse(**data).modified if data else None


def get_tags(
    collection_id: int = 0,
) -> list[Tag] | None:
    endpoint = 'tags' if collection_id == 0 else f'tags/{collection_id}'
    data = make_request('GET', endpoint)
    return Tags(**data).items if data else None


def rename_tag(
    replace: str,
    tags: str,
    collection_id: int = 0,
) -> bool:
    endpoint = 'tags' if collection_id == 0 else f'tags/{collection_id}'
    payload = {'replace': replace, 'tags': [tags]}
    data = make_request('PUT', endpoint, json=payload)
    return True if data else False


def merge_tags(
    replace: str,
    tags: list[str],
    collection_id: int = 0,
) -> bool:
    endpoint = 'tags' if collection_id == 0 else f'tags/{collection_id}'
    payload = {'tags': tags, 'replace': replace}
    data = make_request('PUT', endpoint, json=payload)
    return True if data else False


def delete_tags(
    tags: list[str],
    collection_id: int = 0,
) -> bool:
    endpoint = 'tags' if collection_id == 0 else f'tags/{collection_id}'
    payload = {'tags': tags}
    data = make_request('DELETE', endpoint, json=payload)
    return True if data else False
