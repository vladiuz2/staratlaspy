from __future__ import annotations
import typing
from dataclasses import dataclass
from anchorpy.borsh_extension import EnumForCodegen
import borsh_construct as borsh


class AssetJSON(typing.TypedDict):
    kind: typing.Literal["Asset"]


class CurrencyJSON(typing.TypedDict):
    kind: typing.Literal["Currency"]


@dataclass
class Asset:
    discriminator: typing.ClassVar = 0
    kind: typing.ClassVar = "Asset"

    @classmethod
    def to_json(cls) -> AssetJSON:
        return AssetJSON(
            kind="Asset",
        )

    @classmethod
    def to_encodable(cls) -> dict:
        return {
            "Asset": {},
        }


@dataclass
class Currency:
    discriminator: typing.ClassVar = 1
    kind: typing.ClassVar = "Currency"

    @classmethod
    def to_json(cls) -> CurrencyJSON:
        return CurrencyJSON(
            kind="Currency",
        )

    @classmethod
    def to_encodable(cls) -> dict:
        return {
            "Currency": {},
        }


TokenTypeKind = typing.Union[Asset, Currency]
TokenTypeJSON = typing.Union[AssetJSON, CurrencyJSON]


def from_decoded(obj: dict) -> TokenTypeKind:
    if not isinstance(obj, dict):
        raise ValueError("Invalid enum object")
    if "Asset" in obj:
        return Asset()
    if "Currency" in obj:
        return Currency()
    raise ValueError("Invalid enum object")


def from_json(obj: TokenTypeJSON) -> TokenTypeKind:
    if obj["kind"] == "Asset":
        return Asset()
    if obj["kind"] == "Currency":
        return Currency()
    kind = obj["kind"]
    raise ValueError(f"Unrecognized enum kind: {kind}")


layout = EnumForCodegen("Asset" / borsh.CStruct(), "Currency" / borsh.CStruct())
