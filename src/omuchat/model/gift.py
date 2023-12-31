from typing import NotRequired, TypedDict

from omu.interface import Model


class GiftJson(TypedDict):
    id: str
    name: str
    amount: int
    is_paid: bool
    image_url: NotRequired[str] | None


class Gift(Model[GiftJson]):
    def __init__(
        self,
        id: str,
        name: str,
        amount: int,
        is_paid: bool,
        image_url: str | None = None,
    ) -> None:
        self.id = id
        self.name = name
        self.amount = amount
        self.is_paid = is_paid
        self.image_url = image_url

    @classmethod
    def from_json(cls, json: GiftJson) -> "Gift":
        return cls(
            id=json["id"],
            name=json["name"],
            amount=json["amount"],
            is_paid=json["is_paid"],
            image_url=json.get("image_url", None) and json["image_url"],
        )

    def to_json(self) -> GiftJson:
        return {
            "id": self.id,
            "name": self.name,
            "amount": self.amount,
            "is_paid": self.is_paid,
            "image_url": self.image_url,
        }

    def __str__(self) -> str:
        return self.name
