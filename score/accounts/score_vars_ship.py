import typing
from dataclasses import dataclass
from base64 import b64decode
from solana.publickey import PublicKey
from solana.rpc.async_api import AsyncClient
from solana.rpc.commitment import Commitment
import borsh_construct as borsh
from anchorpy.coder.accounts import ACCOUNT_DISCRIMINATOR_SIZE
from anchorpy.error import AccountInvalidDiscriminator
from anchorpy.utils.rpc import get_multiple_accounts
from anchorpy.borsh_extension import BorshPubkey
from ..program_id import PROGRAM_ID


class ScoreVarsShipJSON(typing.TypedDict):
    ship_mint: str
    reward_rate_per_second: int
    fuel_max_reserve: int
    food_max_reserve: int
    arms_max_reserve: int
    toolkit_max_reserve: int
    milliseconds_to_burn_one_fuel: int
    milliseconds_to_burn_one_food: int
    milliseconds_to_burn_one_arms: int
    milliseconds_to_burn_one_toolkit: int


@dataclass
class ScoreVarsShip:
    discriminator: typing.ClassVar = b"\x1b\xda\x89\x99j\x86\xda\x8f"
    layout: typing.ClassVar = borsh.CStruct(
        "ship_mint" / BorshPubkey,
        "reward_rate_per_second" / borsh.U64,
        "fuel_max_reserve" / borsh.U32,
        "food_max_reserve" / borsh.U32,
        "arms_max_reserve" / borsh.U32,
        "toolkit_max_reserve" / borsh.U32,
        "milliseconds_to_burn_one_fuel" / borsh.U32,
        "milliseconds_to_burn_one_food" / borsh.U32,
        "milliseconds_to_burn_one_arms" / borsh.U32,
        "milliseconds_to_burn_one_toolkit" / borsh.U32,
    )
    ship_mint: PublicKey
    reward_rate_per_second: int
    fuel_max_reserve: int
    food_max_reserve: int
    arms_max_reserve: int
    toolkit_max_reserve: int
    milliseconds_to_burn_one_fuel: int
    milliseconds_to_burn_one_food: int
    milliseconds_to_burn_one_arms: int
    milliseconds_to_burn_one_toolkit: int

    @classmethod
    async def fetch(
        cls,
        conn: AsyncClient,
        address: PublicKey,
        commitment: typing.Optional[Commitment] = None,
    ) -> typing.Optional["ScoreVarsShip"]:
        resp = await conn.get_account_info(address, commitment=commitment)
        info = resp["result"]["value"]
        if info is None:
            return None
        if info["owner"] != str(PROGRAM_ID):
            raise ValueError("Account does not belong to this program")
        bytes_data = b64decode(info["data"][0])
        return cls.decode(bytes_data)

    @classmethod
    async def fetch_multiple(
        cls,
        conn: AsyncClient,
        addresses: list[PublicKey],
        commitment: typing.Optional[Commitment] = None,
    ) -> typing.List[typing.Optional["ScoreVarsShip"]]:
        infos = await get_multiple_accounts(conn, addresses, commitment=commitment)
        res: typing.List[typing.Optional["ScoreVarsShip"]] = []
        for info in infos:
            if info is None:
                res.append(None)
                continue
            if info.account.owner != PROGRAM_ID:
                raise ValueError("Account does not belong to this program")
            res.append(cls.decode(info.account.data))
        return res

    @classmethod
    def decode(cls, data: bytes) -> "ScoreVarsShip":
        if data[:ACCOUNT_DISCRIMINATOR_SIZE] != cls.discriminator:
            raise AccountInvalidDiscriminator(
                "The discriminator for this account is invalid"
            )
        dec = ScoreVarsShip.layout.parse(data[ACCOUNT_DISCRIMINATOR_SIZE:])
        return cls(
            ship_mint=dec.ship_mint,
            reward_rate_per_second=dec.reward_rate_per_second,
            fuel_max_reserve=dec.fuel_max_reserve,
            food_max_reserve=dec.food_max_reserve,
            arms_max_reserve=dec.arms_max_reserve,
            toolkit_max_reserve=dec.toolkit_max_reserve,
            milliseconds_to_burn_one_fuel=dec.milliseconds_to_burn_one_fuel,
            milliseconds_to_burn_one_food=dec.milliseconds_to_burn_one_food,
            milliseconds_to_burn_one_arms=dec.milliseconds_to_burn_one_arms,
            milliseconds_to_burn_one_toolkit=dec.milliseconds_to_burn_one_toolkit,
        )

    def to_json(self) -> ScoreVarsShipJSON:
        return {
            "ship_mint": str(self.ship_mint),
            "reward_rate_per_second": self.reward_rate_per_second,
            "fuel_max_reserve": self.fuel_max_reserve,
            "food_max_reserve": self.food_max_reserve,
            "arms_max_reserve": self.arms_max_reserve,
            "toolkit_max_reserve": self.toolkit_max_reserve,
            "milliseconds_to_burn_one_fuel": self.milliseconds_to_burn_one_fuel,
            "milliseconds_to_burn_one_food": self.milliseconds_to_burn_one_food,
            "milliseconds_to_burn_one_arms": self.milliseconds_to_burn_one_arms,
            "milliseconds_to_burn_one_toolkit": self.milliseconds_to_burn_one_toolkit,
        }

    @classmethod
    def from_json(cls, obj: ScoreVarsShipJSON) -> "ScoreVarsShip":
        return cls(
            ship_mint=PublicKey(obj["ship_mint"]),
            reward_rate_per_second=obj["reward_rate_per_second"],
            fuel_max_reserve=obj["fuel_max_reserve"],
            food_max_reserve=obj["food_max_reserve"],
            arms_max_reserve=obj["arms_max_reserve"],
            toolkit_max_reserve=obj["toolkit_max_reserve"],
            milliseconds_to_burn_one_fuel=obj["milliseconds_to_burn_one_fuel"],
            milliseconds_to_burn_one_food=obj["milliseconds_to_burn_one_food"],
            milliseconds_to_burn_one_arms=obj["milliseconds_to_burn_one_arms"],
            milliseconds_to_burn_one_toolkit=obj["milliseconds_to_burn_one_toolkit"],
        )
