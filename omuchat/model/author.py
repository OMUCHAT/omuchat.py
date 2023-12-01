from typing import List, NotRequired, TypedDict

from omu.interface.keyable import Keyable
from omu.interface.model import Model

from .role import Role, RoleJson


class AuthorJson(TypedDict):
    id: str
    name: str
    avatar_url: str
    roles: NotRequired[List[RoleJson]] | None


class Author(Keyable, Model[AuthorJson]):
    def __init__(self, id: str, name: str, avatar_url: str, roles: List[Role]):
        self.id = id
        self.name = name
        self.avatar_url = avatar_url
        self.roles = roles

    def key(self) -> str:
        return self.id

    def json(self) -> AuthorJson:
        return {
            "id": self.id,
            "name": self.name,
            "avatar_url": self.avatar_url,
            "roles": [role.json() for role in self.roles],
        }

    @classmethod
    def from_json(cls, json: AuthorJson) -> "Author":
        return cls(
            id=json["id"],
            name=json["name"],
            avatar_url=json["avatar_url"],
            roles=[Role.from_json(role) for role in json["roles"]]
            if json.get("roles", None) and json["roles"]
            else [],
        )

    def __str__(self) -> str:
        return f"Author(id={self.id}, name={self.name}, avatar_url={self.avatar_url}, roles={self.roles})"
