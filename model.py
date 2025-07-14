from typing import Any

from pydantic import BaseModel, Field, field_validator, model_serializer


class RaindropBaseModel(BaseModel):
    result: bool

    @classmethod
    @field_validator('result')
    def check_result(cls, value):
        if not value:
            raise ValueError('Request failed')

        return value


class User(RaindropBaseModel):
    class Data(BaseModel):
        id: int = Field(alias='_id', default=None)
        fullName: str
        email: str
        name: str
        groups: list['Group'] = []

    user: Data


class Parent(BaseModel):
    id: int = Field(alias='$id', default=None)

    @model_serializer
    def ser_model(self) -> dict[str, Any]:
        return {'$id': self.id} if self.id else {}


class Group(BaseModel):
    title: str
    collections: list[int] = []
    items: list['CollectionItem'] | None = None


class CollectionItem(BaseModel):
    id: int = Field(alias='_id', default=None)
    count: int = None
    title: str | None = None
    order: int = 0
    sort: int = 0
    public: bool = False
    parent: Parent | None = None
    parentId: int | None = None
    items: list['CollectionItem'] | None = None


class Collection(RaindropBaseModel):
    item: CollectionItem


class CollectionItems(RaindropBaseModel):
    items: list[CollectionItem] = []


class RaindropItem(BaseModel):
    id: int = Field(alias='_id', default=None)
    link: str
    title: str = None
    excerpt: str = None
    note: str = None
    tags: list[str] = []
    collection: Parent = None
    collectionId: int = 0


class Raindrop(RaindropBaseModel):
    item: RaindropItem
