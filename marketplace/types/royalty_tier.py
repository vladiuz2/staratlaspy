from __future__ import annotations
import typing
from dataclasses import dataclass
from construct import Container
import borsh_construct as borsh


class RoyaltyTierJSON(typing.TypedDict):
    stake_amount: int
    discount: int


@dataclass
class RoyaltyTier:
    layout: typing.ClassVar = borsh.CStruct(
        "stake_amount" / borsh.U64, "discount" / borsh.U64
    )
    stake_amount: int
    discount: int

    @classmethod
    def from_decoded(cls, obj: Container) -> "RoyaltyTier":
        return cls(stake_amount=obj.stake_amount, discount=obj.discount)

    def to_encodable(self) -> dict[str, typing.Any]:
        return {"stake_amount": self.stake_amount, "discount": self.discount}

    def to_json(self) -> RoyaltyTierJSON:
        return {"stake_amount": self.stake_amount, "discount": self.discount}

    @classmethod
    def from_json(cls, obj: RoyaltyTierJSON) -> "RoyaltyTier":
        return cls(stake_amount=obj["stake_amount"], discount=obj["discount"])
