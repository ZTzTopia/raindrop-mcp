import os
from typing import Literal

import requests

from type import (
    Collection,
    CollectionItem,
    CollectionItems,
    Group,
    Raindrop,
    RaindropItem,
    User,
)

URL = 'https://api.raindrop.io/rest/v1'
RAINDROP_ACCESS_TOKEN = os.getenv('RAINDROP_ACCESS_TOKEN')

session = requests.Session()
session.headers = {'Authorization': f'Bearer {RAINDROP_ACCESS_TOKEN}'}


def make_request(method, endpoint, **kwargs):
    response = session.request(method, f'{URL}/{endpoint}', **kwargs)
    if response.status_code == 200:
        data = response.json()
        return data

    return None


def get_user() -> User | None:
    data = make_request('GET', 'user')
    return User(**data) if data else None


def get_total_collections(
    collection_type: Literal['all', 'unsorted', 'trash'] = 'all',
) -> dict | None:
    stats = make_request('GET', 'user/stats')
    if not stats:
        return None

    id_map = {'all': 0, 'unsorted': -1, 'trash': -99}

    target_id = id_map.get(collection_type)
    return {
        'count': next(
            (
                item.get('count', 0)
                for item in stats.get('items', [])
                if item.get('_id') == target_id
            ),
            0,
        )
    }


def get_groups() -> list[Group] | None:
    user = get_user()
    return user.user.groups if user else None


def get_group(name: str):
    """
    Get a specific group by name.
    """
    groups = get_groups()
    return (
        next((group for group in groups if group.title == name), None)
        if groups
        else None
    )


def get_root_collections(
    flat: bool = False,
) -> list[Group] | list[CollectionItem] | None:
    """Fetch root collections, optionally grouped."""
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

    return groups


def get_collections() -> list[Group] | None:
    """Fetch all collections, including children."""
    data = make_request('GET', 'collections/childrens')
    if not data:
        return None

    collections = CollectionItems(**data)

    root_collections = get_root_collections(True)
    if not root_collections:
        return None

    collections_map = {item.id: item for item in root_collections}
    collections_map.update({item.id: item for item in collections.items})

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

    # FIXME: We need another request to user endpoint to make this items
    #       available in groups.
    if groups:
        ungrouped_items = [
            c for c in root_items if all(c.id not in g.items for g in groups)
        ]
        groups[0].items.extend(ungrouped_items)

    return groups


def get_collection(id: int) -> CollectionItem | None:
    """Fetch a specific collection by ID."""
    data = make_request('GET', f'collection/{id}')
    return Collection(**data).item if data else None


def create_collection(collection: CollectionItem) -> CollectionItem | None:
    """Create a new collection."""
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
    """Delete a specific collection."""
    data = make_request('DELETE', f'collection/{id}')
    return True if data else False


def delete_collections(ids: list):
    """Delete multiple collections."""
    payload = {'ids': ids}
    data = make_request('DELETE', 'collections', json=payload)
    return True if data else False


def get_raindrop(raindrop_id: int) -> RaindropItem | None:
    """Fetch a specific raindrop by ID."""
    data = make_request('GET', f'raindrop/{raindrop_id}')
    return Raindrop(**data).item if data else None


# TODO: Create tree structure for nested raindrops
def get_raindrops(
    id: int = 0,
    search: str = '',
    page: int = 0,
    perpage: int = 20,
    nested: bool = False,
):
    """Fetch raindrops from a specific collection."""
    params = {'search': search, 'page': page, 'perpage': perpage, 'nested': nested}
    data = make_request('GET', f'raindrops/{id}', params=params)
    return (
        [RaindropItem(**item) for item in data['items']]
        if data and 'items' in data
        else None
    )


def create_raindrop(raindrop: RaindropItem) -> RaindropItem | None:
    """Create a new raindrop."""
    data = make_request(
        'POST',
        'raindrop',
        json=raindrop.model_dump(exclude_unset=True, exclude_none=True),
    )
    return Raindrop(**data).item if data else None


def update_raindrop(raindrop_id: int, raindrop: RaindropItem) -> RaindropItem | None:
    """Update an existing raindrop."""
    data = make_request(
        'PUT',
        f'raindrop/{raindrop_id}',
        json=raindrop.model_dump(exclude_unset=True, exclude_none=True),
    )
    return Raindrop(**data).item if data else None


def delete_raindrop(raindrop_id: int):
    """Delete a specific raindrop."""
    data = make_request('DELETE', f'raindrop/{raindrop_id}')
    return True if data else False
