from datetime import datetime
from typing import List, NotRequired, TypedDict

from omu.interface import Keyable, Model

from .author import Author, AuthorJson
from .content import Content, ContentComponent, ContentJson, TextContent
from .gift import Gift, GiftJson
from .paid import Paid, PaidJson


class MessageJson(TypedDict):
    room_id: str
    id: str
    content: NotRequired[ContentJson] | None
    author: NotRequired[AuthorJson] | None
    paid: NotRequired[PaidJson] | None
    gift: NotRequired[GiftJson] | None
    created_at: NotRequired[int] | None


class Message(Keyable, Model[MessageJson]):
    def __init__(
        self,
        room_id: str,
        id: str,
        content: Content | None = None,
        author: Author | None = None,
        paid: Paid | None = None,
        gift: Gift | None = None,
        created_at: datetime | None = None,
    ) -> None:
        self.room_id = room_id
        self.id = id
        self.content = content
        self.author = author
        self.paid = paid
        self.gift = gift
        self.created_at = created_at

    @classmethod
    def from_json(cls, json: MessageJson) -> "Message":
        content = None
        if json.get("content", None) and json["content"]:
            content = ContentComponent.from_json(json["content"])
        author = None
        if json.get("author", None) and json["author"]:
            author = Author.from_json(json["author"])
        paid = None
        if json.get("paid", None) and json["paid"]:
            paid = Paid.from_json(json["paid"])
        gift = None
        if json.get("gift", None) and json["gift"]:
            gift = Gift.from_json(json["gift"])
        created_at = None
        if json.get("created_at", None) and json["created_at"]:
            created_at = datetime.fromtimestamp(json["created_at"] / 1000)

        return cls(
            room_id=json["room_id"],
            id=json["id"],
            content=content,
            author=author,
            paid=paid,
            gift=gift,
            created_at=created_at,
        )

    @property
    def text(self) -> str:
        if not self.content:
            return ""
        parts = []
        components: List[Content] = [self.content]
        while components:
            component = components.pop(0)
            if isinstance(component, TextContent):
                parts.append(component.text)
            if component.siblings:
                components.extend(component.siblings)
        return "".join(parts)

    def key(self) -> str:
        return self.id

    def json(self) -> MessageJson:
        return MessageJson(
            room_id=self.room_id,
            id=self.id,
            content=self.content.json() if self.content else None,
            author=self.author.json() if self.author else None,
            paid=self.paid.json() if self.paid else None,
            gift=self.gift.json() if self.gift else None,
            created_at=int(self.created_at.timestamp() * 1000)
            if self.created_at
            else None,
        )

    def __str__(self) -> str:
        return f"{self.author}: {self.content}"
