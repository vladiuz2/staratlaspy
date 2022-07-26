import typing
from dataclasses import dataclass
from base64 import b64decode
from construct import Construct
from solana.publickey import PublicKey
from solana.rpc.async_api import AsyncClient
from solana.rpc.commitment import Commitment
import borsh_construct as borsh
from anchorpy.coder.accounts import ACCOUNT_DISCRIMINATOR_SIZE
from anchorpy.error import AccountInvalidDiscriminator
from anchorpy.utils.rpc import get_multiple_accounts
from anchorpy.borsh_extension import BorshPubkey
from ..program_id import PROGRAM_ID
from ..types import royalty_tier

class RegisteredCurrencyJSON(typing.TypedDict):
    token_mint: str
    sa_currency_vault: str
    royalty: int
    bump: int
    royalty_tiers: typing.Optional[list[royalty_tier.RoyaltyTierJSON]]


@dataclass
class RegisteredCurrency:
    discriminator: typing.ClassVar = b"<r\xf4\x86\x10\xa63\x95"
    layout: typing.ClassVar = borsh.CStruct(
        "token_mint" / BorshPubkey,
        "sa_currency_vault" / BorshPubkey,
        "royalty" / borsh.U64,
        "bump" / borsh.U8,
        "royalty_tiers"
        / borsh.Option(
            borsh.Vec(typing.cast(Construct, royalty_tier.RoyaltyTier.layout))
        ),
    )
    token_mint: PublicKey
    sa_currency_vault: PublicKey
    royalty: int
    bump: int
    royalty_tiers: typing.Optional[list[royalty_tier.RoyaltyTier]]

    @classmethod
    async def fetch(
        cls,
        conn: AsyncClient,
        address: PublicKey,
        commitment: typing.Optional[Commitment] = None,
    ) -> typing.Optional["RegisteredCurrency"]:
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
    ) -> typing.List[typing.Optional["RegisteredCurrency"]]:
        infos = await get_multiple_accounts(conn, addresses, commitment=commitment)
        res: typing.List[typing.Optional["RegisteredCurrency"]] = []
        for info in infos:
            if info is None:
                res.append(None)
                continue
            if info.account.owner != PROGRAM_ID:
                raise ValueError("Account does not belong to this program")
            res.append(cls.decode(info.account.data))
        return res

    @classmethod
    def decode(cls, data: bytes) -> "RegisteredCurrency":
        if data[:ACCOUNT_DISCRIMINATOR_SIZE] != cls.discriminator:
            raise AccountInvalidDiscriminator(
                "The discriminator for this account is invalid"
            )
        dec = RegisteredCurrency.layout.parse(data[ACCOUNT_DISCRIMINATOR_SIZE:])
        return cls(
            token_mint=dec.token_mint,
            sa_currency_vault=dec.sa_currency_vault,
            royalty=dec.royalty,
            bump=dec.bump,
            royalty_tiers=(
                None
                if dec.royalty_tiers is None
                else list(
                    map(
                        lambda item: royalty_tier.RoyaltyTier.from_decoded(item),
                        dec.royalty_tiers,
                    )
                )
            ),
        )

    def to_json(self) -> RegisteredCurrencyJSON:
        return {
            "token_mint": str(self.token_mint),
            "sa_currency_vault": str(self.sa_currency_vault),
            "royalty": self.royalty,
            "bump": self.bump,
            "royalty_tiers": (
                None
                if self.royalty_tiers is None
                else list(map(lambda item: item.to_json(), self.royalty_tiers))
            ),
        }

    @classmethod
    def from_json(cls, obj: RegisteredCurrencyJSON) -> "RegisteredCurrency":
        return cls(
            token_mint=PublicKey(obj["token_mint"]),
            sa_currency_vault=PublicKey(obj["sa_currency_vault"]),
            royalty=obj["royalty"],
            bump=obj["bump"],
            royalty_tiers=(
                None
                if obj["royalty_tiers"] is None
                else list(
                    map(
                        lambda item: royalty_tier.RoyaltyTier.from_json(item),
                        obj["royalty_tiers"],
                    )
                )
            ),
        )
