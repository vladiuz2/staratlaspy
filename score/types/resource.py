from __future__ import annotations
import typing
from dataclasses import dataclass
from anchorpy.borsh_extension import EnumForCodegen
import borsh_construct as borsh


class ArmsJSON(typing.TypedDict):
    kind: typing.Literal["Arms"]


class FuelJSON(typing.TypedDict):
    kind: typing.Literal["Fuel"]


class FoodJSON(typing.TypedDict):
    kind: typing.Literal["Food"]


class ToolkitsJSON(typing.TypedDict):
    kind: typing.Literal["Toolkits"]


@dataclass
class Arms:
    discriminator: typing.ClassVar = 0
    kind: typing.ClassVar = "Arms"

    @classmethod
    def to_json(cls) -> ArmsJSON:
        return ArmsJSON(
            kind="Arms",
        )

    @classmethod
    def to_encodable(cls) -> dict:
        return {
            "Arms": {},
        }


@dataclass
class Fuel:
    discriminator: typing.ClassVar = 1
    kind: typing.ClassVar = "Fuel"

    @classmethod
    def to_json(cls) -> FuelJSON:
        return FuelJSON(
            kind="Fuel",
        )

    @classmethod
    def to_encodable(cls) -> dict:
        return {
            "Fuel": {},
        }


@dataclass
class Food:
    discriminator: typing.ClassVar = 2
    kind: typing.ClassVar = "Food"

    @classmethod
    def to_json(cls) -> FoodJSON:
        return FoodJSON(
            kind="Food",
        )

    @classmethod
    def to_encodable(cls) -> dict:
        return {
            "Food": {},
        }


@dataclass
class Toolkits:
    discriminator: typing.ClassVar = 3
    kind: typing.ClassVar = "Toolkits"

    @classmethod
    def to_json(cls) -> ToolkitsJSON:
        return ToolkitsJSON(
            kind="Toolkits",
        )

    @classmethod
    def to_encodable(cls) -> dict:
        return {
            "Toolkits": {},
        }


ResourceKind = typing.Union[Arms, Fuel, Food, Toolkits]
ResourceJSON = typing.Union[ArmsJSON, FuelJSON, FoodJSON, ToolkitsJSON]


def from_decoded(obj: dict) -> ResourceKind:
    if not isinstance(obj, dict):
        raise ValueError("Invalid enum object")
    if "Arms" in obj:
        return Arms()
    if "Fuel" in obj:
        return Fuel()
    if "Food" in obj:
        return Food()
    if "Toolkits" in obj:
        return Toolkits()
    raise ValueError("Invalid enum object")


def from_json(obj: ResourceJSON) -> ResourceKind:
    if obj["kind"] == "Arms":
        return Arms()
    if obj["kind"] == "Fuel":
        return Fuel()
    if obj["kind"] == "Food":
        return Food()
    if obj["kind"] == "Toolkits":
        return Toolkits()
    kind = obj["kind"]
    raise ValueError(f"Unrecognized enum kind: {kind}")


layout = EnumForCodegen(
    "Arms" / borsh.CStruct(),
    "Fuel" / borsh.CStruct(),
    "Food" / borsh.CStruct(),
    "Toolkits" / borsh.CStruct(),
)
