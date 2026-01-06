from typing import Optional
from pydantic import BaseModel, Field, field_validator


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
        id: Optional[int] = Field(alias='_id', default=None)
        fullName: str
        email: str
        name: str
        groups: list['Group'] = []

    user: Data


class Parent(BaseModel):
    id: Optional[int] = Field(alias='$id', default=None)


class Group(BaseModel):
    title: str
    collections: list[int] = []
    items: Optional[list['CollectionItem']] = None


class CollectionItem(BaseModel):
    id: Optional[int] = Field(alias='_id', default=None)
    count: Optional[int] = None
    title: Optional[str] = None
    order: int = 0
    sort: int = 0
    public: bool = False
    parent: Optional[Parent] = None
    parentId: Optional[int] = None
    items: Optional[list['CollectionItem']] = None


class Collection(RaindropBaseModel):
    item: CollectionItem


class CollectionItems(RaindropBaseModel):
    items: list[CollectionItem] = []


class RaindropBase(BaseModel):
    link: Optional[str] = None
    title: Optional[str] = None
    excerpt: Optional[str] = None
    note: Optional[str] = None
    tags: Optional[list[str]] = None
    important: Optional[bool] = None
    collectionId: Optional[int] = None


class RaindropCreate(RaindropBase):
    pleaseParse: dict
    link: str


class RaindropUpdate(RaindropBase):
    pleaseParse: Optional[dict] = None


class RaindropsUpdate(BaseModel):
    ids: Optional[list[int]] = None
    important: Optional[bool] = None
    tags: Optional[list[str]] = None
    collectionId: Optional[int] = None


class RaindropBaseResponse(RaindropBase):
    id: Optional[int] = Field(alias='_id', default=None)
    collection: Optional[Parent] = None


class RaindropResponse(RaindropBaseModel):
    item: RaindropBaseResponse


class RaindropsResponse(RaindropBaseModel):
    items: list[RaindropBaseResponse] = []
    count: int = 0


class UpdateDeleteRaindropsResponse(BaseModel):
    modified: int


class Tag(BaseModel):
    id: Optional[str] = Field(alias='_id', default=None)
    count: int = 0


class Tags(RaindropBaseModel):
    items: list[Tag] = []
