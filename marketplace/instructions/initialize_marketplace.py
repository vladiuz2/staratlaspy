from __future__ import annotations
import typing
from solana.publickey import PublicKey
from solana.transaction import TransactionInstruction, AccountMeta
from ..program_id import PROGRAM_ID


class InitializeMarketplaceAccounts(typing.TypedDict):
    update_authority_account: PublicKey
    market_vars_account: PublicKey
    system_program: PublicKey


def initialize_marketplace(
    accounts: InitializeMarketplaceAccounts,
) -> TransactionInstruction:
    keys: list[AccountMeta] = [
        AccountMeta(
            pubkey=accounts["update_authority_account"],
            is_signer=True,
            is_writable=True,
        ),
        AccountMeta(
            pubkey=accounts["market_vars_account"], is_signer=False, is_writable=True
        ),
        AccountMeta(
            pubkey=accounts["system_program"], is_signer=False, is_writable=False
        ),
    ]
    identifier = b"/Q@\x00`8i\x07"
    encoded_args = b""
    data = identifier + encoded_args
    return TransactionInstruction(keys, PROGRAM_ID, data)
