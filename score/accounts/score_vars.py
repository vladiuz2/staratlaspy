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


class ScoreVarsJSON(typing.TypedDict):
    update_authority_master: str
    fuel_mint: str
    food_mint: str
    arms_mint: str
    toolkit_mint: str


@dataclass
class ScoreVars:
    discriminator: typing.ClassVar = b"-R\xb6K\xa5Qy<"
    layout: typing.ClassVar = borsh.CStruct(
        "update_authority_master" / BorshPubkey,
        "fuel_mint" / BorshPubkey,
        "food_mint" / BorshPubkey,
        "arms_mint" / BorshPubkey,
        "toolkit_mint" / BorshPubkey,
    )
    update_authority_master: PublicKey
    fuel_mint: PublicKey
    food_mint: PublicKey
    arms_mint: PublicKey
    toolkit_mint: PublicKey

    @classmethod
    async def fetch(
        cls,
        conn: AsyncClient,
        address: PublicKey,
        commitment: typing.Optional[Commitment] = None,
    ) -> typing.Optional["ScoreVars"]:
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
    ) -> typing.List[typing.Optional["ScoreVars"]]:
        infos = await get_multiple_accounts(conn, addresses, commitment=commitment)
        res: typing.List[typing.Optional["ScoreVars"]] = []
        for info in infos:
            if info is None:
                res.append(None)
                continue
            if info.account.owner != PROGRAM_ID:
                raise ValueError("Account does not belong to this program")
            res.append(cls.decode(info.account.data))
        return res

    @classmethod
    def decode(cls, data: bytes) -> "ScoreVars":
        if data[:ACCOUNT_DISCRIMINATOR_SIZE] != cls.discriminator:
            raise AccountInvalidDiscriminator(
                "The discriminator for this account is invalid"
            )
        dec = ScoreVars.layout.parse(data[ACCOUNT_DISCRIMINATOR_SIZE:])
        return cls(
            update_authority_master=dec.update_authority_master,
            fuel_mint=dec.fuel_mint,
            food_mint=dec.food_mint,
            arms_mint=dec.arms_mint,
            toolkit_mint=dec.toolkit_mint,
        )

    def to_json(self) -> ScoreVarsJSON:
        return {
            "update_authority_master": str(self.update_authority_master),
            "fuel_mint": str(self.fuel_mint),
            "food_mint": str(self.food_mint),
            "arms_mint": str(self.arms_mint),
            "toolkit_mint": str(self.toolkit_mint),
        }

    @classmethod
    def from_json(cls, obj: ScoreVarsJSON) -> "ScoreVars":
        return cls(
            update_authority_master=PublicKey(obj["update_authority_master"]),
            fuel_mint=PublicKey(obj["fuel_mint"]),
            food_mint=PublicKey(obj["food_mint"]),
            arms_mint=PublicKey(obj["arms_mint"]),
            toolkit_mint=PublicKey(obj["toolkit_mint"]),
        )
