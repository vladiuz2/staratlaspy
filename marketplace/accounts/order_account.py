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
from ..types import order_side

class OrderAccountJSON(typing.TypedDict):
    order_initializer_pubkey: str
    currency_mint: str
    asset_mint: str
    initializer_currency_token_account: str
    initializer_asset_token_account: str
    order_side: order_side.OrderSideJSON
    price: int
    order_origination_qty: int
    order_remaining_qty: int
    created_at_timestamp: int


@dataclass
class OrderAccount:
    discriminator: typing.ClassVar = b"OCp\x9b\xd6\x0e 7"
    layout: typing.ClassVar = borsh.CStruct(
        "order_initializer_pubkey" / BorshPubkey,
        "currency_mint" / BorshPubkey,
        "asset_mint" / BorshPubkey,
        "initializer_currency_token_account" / BorshPubkey,
        "initializer_asset_token_account" / BorshPubkey,
        "order_side" / order_side.layout,
        "price" / borsh.U64,
        "order_origination_qty" / borsh.U64,
        "order_remaining_qty" / borsh.U64,
        "created_at_timestamp" / borsh.I64,
    )
    order_initializer_pubkey: PublicKey
    currency_mint: PublicKey
    asset_mint: PublicKey
    initializer_currency_token_account: PublicKey
    initializer_asset_token_account: PublicKey
    order_side: order_side.OrderSideKind
    price: int
    order_origination_qty: int
    order_remaining_qty: int
    created_at_timestamp: int

    @classmethod
    async def fetch(
        cls,
        conn: AsyncClient,
        address: PublicKey,
        commitment: typing.Optional[Commitment] = None,
    ) -> typing.Optional["OrderAccount"]:
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
    ) -> typing.List[typing.Optional["OrderAccount"]]:
        infos = await get_multiple_accounts(conn, addresses, commitment=commitment)
        res: typing.List[typing.Optional["OrderAccount"]] = []
        for info in infos:
            if info is None:
                res.append(None)
                continue
            if info.account.owner != PROGRAM_ID:
                raise ValueError("Account does not belong to this program")
            res.append(cls.decode(info.account.data))
        return res

    @classmethod
    def decode(cls, data: bytes) -> "OrderAccount":
        if data[:ACCOUNT_DISCRIMINATOR_SIZE] != cls.discriminator:
            raise AccountInvalidDiscriminator(
                "The discriminator for this account is invalid"
            )
        dec = OrderAccount.layout.parse(data[ACCOUNT_DISCRIMINATOR_SIZE:])
        return cls(
            order_initializer_pubkey=dec.order_initializer_pubkey,
            currency_mint=dec.currency_mint,
            asset_mint=dec.asset_mint,
            initializer_currency_token_account=dec.initializer_currency_token_account,
            initializer_asset_token_account=dec.initializer_asset_token_account,
            order_side=order_side.from_decoded(dec.order_side),
            price=dec.price,
            order_origination_qty=dec.order_origination_qty,
            order_remaining_qty=dec.order_remaining_qty,
            created_at_timestamp=dec.created_at_timestamp,
        )

    def to_json(self) -> OrderAccountJSON:
        return {
            "order_initializer_pubkey": str(self.order_initializer_pubkey),
            "currency_mint": str(self.currency_mint),
            "asset_mint": str(self.asset_mint),
            "initializer_currency_token_account": str(
                self.initializer_currency_token_account
            ),
            "initializer_asset_token_account": str(
                self.initializer_asset_token_account
            ),
            "order_side": self.order_side.to_json(),
            "price": self.price,
            "order_origination_qty": self.order_origination_qty,
            "order_remaining_qty": self.order_remaining_qty,
            "created_at_timestamp": self.created_at_timestamp,
        }

    @classmethod
    def from_json(cls, obj: OrderAccountJSON) -> "OrderAccount":
        return cls(
            order_initializer_pubkey=PublicKey(obj["order_initializer_pubkey"]),
            currency_mint=PublicKey(obj["currency_mint"]),
            asset_mint=PublicKey(obj["asset_mint"]),
            initializer_currency_token_account=PublicKey(
                obj["initializer_currency_token_account"]
            ),
            initializer_asset_token_account=PublicKey(
                obj["initializer_asset_token_account"]
            ),
            order_side=order_side.from_json(obj["order_side"]),
            price=obj["price"],
            order_origination_qty=obj["order_origination_qty"],
            order_remaining_qty=obj["order_remaining_qty"],
            created_at_timestamp=obj["created_at_timestamp"],
        )
