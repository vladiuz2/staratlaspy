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


class ShipStakingJSON(typing.TypedDict):
    owner: str
    faction_id: int
    ship_mint: str
    ship_quantity_in_escrow: int
    fuel_quantity_in_escrow: int
    food_quantity_in_escrow: int
    arms_quantity_in_escrow: int
    fuel_current_capacity: int
    food_current_capacity: int
    arms_current_capacity: int
    health_current_capacity: int
    staked_at_timestamp: int
    fueled_at_timestamp: int
    fed_at_timestamp: int
    armed_at_timestamp: int
    repaired_at_timestamp: int
    current_capacity_timestamp: int
    total_time_staked: int
    staked_time_paid: int
    pending_rewards: int
    total_rewards_paid: int


@dataclass
class ShipStaking:
    discriminator: typing.ClassVar = b"C\xe5T(\xbc%\t{"
    layout: typing.ClassVar = borsh.CStruct(
        "owner" / BorshPubkey,
        "faction_id" / borsh.U8,
        "ship_mint" / BorshPubkey,
        "ship_quantity_in_escrow" / borsh.U64,
        "fuel_quantity_in_escrow" / borsh.U64,
        "food_quantity_in_escrow" / borsh.U64,
        "arms_quantity_in_escrow" / borsh.U64,
        "fuel_current_capacity" / borsh.U64,
        "food_current_capacity" / borsh.U64,
        "arms_current_capacity" / borsh.U64,
        "health_current_capacity" / borsh.U64,
        "staked_at_timestamp" / borsh.I64,
        "fueled_at_timestamp" / borsh.I64,
        "fed_at_timestamp" / borsh.I64,
        "armed_at_timestamp" / borsh.I64,
        "repaired_at_timestamp" / borsh.I64,
        "current_capacity_timestamp" / borsh.I64,
        "total_time_staked" / borsh.U64,
        "staked_time_paid" / borsh.U64,
        "pending_rewards" / borsh.U64,
        "total_rewards_paid" / borsh.U64,
    )
    owner: PublicKey
    faction_id: int
    ship_mint: PublicKey
    ship_quantity_in_escrow: int
    fuel_quantity_in_escrow: int
    food_quantity_in_escrow: int
    arms_quantity_in_escrow: int
    fuel_current_capacity: int
    food_current_capacity: int
    arms_current_capacity: int
    health_current_capacity: int
    staked_at_timestamp: int
    fueled_at_timestamp: int
    fed_at_timestamp: int
    armed_at_timestamp: int
    repaired_at_timestamp: int
    current_capacity_timestamp: int
    total_time_staked: int
    staked_time_paid: int
    pending_rewards: int
    total_rewards_paid: int

    @classmethod
    async def fetch(
        cls,
        conn: AsyncClient,
        address: PublicKey,
        commitment: typing.Optional[Commitment] = None,
    ) -> typing.Optional["ShipStaking"]:
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
    ) -> typing.List[typing.Optional["ShipStaking"]]:
        infos = await get_multiple_accounts(conn, addresses, commitment=commitment)
        res: typing.List[typing.Optional["ShipStaking"]] = []
        for info in infos:
            if info is None:
                res.append(None)
                continue
            if info.account.owner != PROGRAM_ID:
                raise ValueError("Account does not belong to this program")
            res.append(cls.decode(info.account.data))
        return res

    @classmethod
    def decode(cls, data: bytes) -> "ShipStaking":
        if data[:ACCOUNT_DISCRIMINATOR_SIZE] != cls.discriminator:
            raise AccountInvalidDiscriminator(
                "The discriminator for this account is invalid"
            )
        dec = ShipStaking.layout.parse(data[ACCOUNT_DISCRIMINATOR_SIZE:])
        return cls(
            owner=dec.owner,
            faction_id=dec.faction_id,
            ship_mint=dec.ship_mint,
            ship_quantity_in_escrow=dec.ship_quantity_in_escrow,
            fuel_quantity_in_escrow=dec.fuel_quantity_in_escrow,
            food_quantity_in_escrow=dec.food_quantity_in_escrow,
            arms_quantity_in_escrow=dec.arms_quantity_in_escrow,
            fuel_current_capacity=dec.fuel_current_capacity,
            food_current_capacity=dec.food_current_capacity,
            arms_current_capacity=dec.arms_current_capacity,
            health_current_capacity=dec.health_current_capacity,
            staked_at_timestamp=dec.staked_at_timestamp,
            fueled_at_timestamp=dec.fueled_at_timestamp,
            fed_at_timestamp=dec.fed_at_timestamp,
            armed_at_timestamp=dec.armed_at_timestamp,
            repaired_at_timestamp=dec.repaired_at_timestamp,
            current_capacity_timestamp=dec.current_capacity_timestamp,
            total_time_staked=dec.total_time_staked,
            staked_time_paid=dec.staked_time_paid,
            pending_rewards=dec.pending_rewards,
            total_rewards_paid=dec.total_rewards_paid,
        )

    def to_json(self) -> ShipStakingJSON:
        return {
            "owner": str(self.owner),
            "faction_id": self.faction_id,
            "ship_mint": str(self.ship_mint),
            "ship_quantity_in_escrow": self.ship_quantity_in_escrow,
            "fuel_quantity_in_escrow": self.fuel_quantity_in_escrow,
            "food_quantity_in_escrow": self.food_quantity_in_escrow,
            "arms_quantity_in_escrow": self.arms_quantity_in_escrow,
            "fuel_current_capacity": self.fuel_current_capacity,
            "food_current_capacity": self.food_current_capacity,
            "arms_current_capacity": self.arms_current_capacity,
            "health_current_capacity": self.health_current_capacity,
            "staked_at_timestamp": self.staked_at_timestamp,
            "fueled_at_timestamp": self.fueled_at_timestamp,
            "fed_at_timestamp": self.fed_at_timestamp,
            "armed_at_timestamp": self.armed_at_timestamp,
            "repaired_at_timestamp": self.repaired_at_timestamp,
            "current_capacity_timestamp": self.current_capacity_timestamp,
            "total_time_staked": self.total_time_staked,
            "staked_time_paid": self.staked_time_paid,
            "pending_rewards": self.pending_rewards,
            "total_rewards_paid": self.total_rewards_paid,
        }

    @classmethod
    def from_json(cls, obj: ShipStakingJSON) -> "ShipStaking":
        return cls(
            owner=PublicKey(obj["owner"]),
            faction_id=obj["faction_id"],
            ship_mint=PublicKey(obj["ship_mint"]),
            ship_quantity_in_escrow=obj["ship_quantity_in_escrow"],
            fuel_quantity_in_escrow=obj["fuel_quantity_in_escrow"],
            food_quantity_in_escrow=obj["food_quantity_in_escrow"],
            arms_quantity_in_escrow=obj["arms_quantity_in_escrow"],
            fuel_current_capacity=obj["fuel_current_capacity"],
            food_current_capacity=obj["food_current_capacity"],
            arms_current_capacity=obj["arms_current_capacity"],
            health_current_capacity=obj["health_current_capacity"],
            staked_at_timestamp=obj["staked_at_timestamp"],
            fueled_at_timestamp=obj["fueled_at_timestamp"],
            fed_at_timestamp=obj["fed_at_timestamp"],
            armed_at_timestamp=obj["armed_at_timestamp"],
            repaired_at_timestamp=obj["repaired_at_timestamp"],
            current_capacity_timestamp=obj["current_capacity_timestamp"],
            total_time_staked=obj["total_time_staked"],
            staked_time_paid=obj["staked_time_paid"],
            pending_rewards=obj["pending_rewards"],
            total_rewards_paid=obj["total_rewards_paid"],
        )
