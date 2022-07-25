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
from ..program_id import PROGRAM_ID


class OpenOrdersCounterJSON(typing.TypedDict):
    open_order_count: int
    bump: int


@dataclass
class OpenOrdersCounter:
    discriminator: typing.ClassVar = b"\xf5p1\x81.!\xb7I"
    layout: typing.ClassVar = borsh.CStruct(
        "open_order_count" / borsh.U64, "bump" / borsh.U8
    )
    open_order_count: int
    bump: int

    @classmethod
    async def fetch(
        cls,
        conn: AsyncClient,
        address: PublicKey,
        commitment: typing.Optional[Commitment] = None,
    ) -> typing.Optional["OpenOrdersCounter"]:
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
    ) -> typing.List[typing.Optional["OpenOrdersCounter"]]:
        infos = await get_multiple_accounts(conn, addresses, commitment=commitment)
        res: typing.List[typing.Optional["OpenOrdersCounter"]] = []
        for info in infos:
            if info is None:
                res.append(None)
                continue
            if info.account.owner != PROGRAM_ID:
                raise ValueError("Account does not belong to this program")
            res.append(cls.decode(info.account.data))
        return res

    @classmethod
    def decode(cls, data: bytes) -> "OpenOrdersCounter":
        if data[:ACCOUNT_DISCRIMINATOR_SIZE] != cls.discriminator:
            raise AccountInvalidDiscriminator(
                "The discriminator for this account is invalid"
            )
        dec = OpenOrdersCounter.layout.parse(data[ACCOUNT_DISCRIMINATOR_SIZE:])
        return cls(
            open_order_count=dec.open_order_count,
            bump=dec.bump,
        )

    def to_json(self) -> OpenOrdersCounterJSON:
        return {
            "open_order_count": self.open_order_count,
            "bump": self.bump,
        }

    @classmethod
    def from_json(cls, obj: OpenOrdersCounterJSON) -> "OpenOrdersCounter":
        return cls(
            open_order_count=obj["open_order_count"],
            bump=obj["bump"],
        )
