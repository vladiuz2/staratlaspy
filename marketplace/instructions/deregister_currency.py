from __future__ import annotations
import typing
from solana.publickey import PublicKey
from solana.transaction import TransactionInstruction, AccountMeta
from ..program_id import PROGRAM_ID


class DeregisterCurrencyAccounts(typing.TypedDict):
    update_authority_account: PublicKey
    market_vars_account: PublicKey
    registered_currency: PublicKey
    currency_mint: PublicKey
    system_program: PublicKey


def deregister_currency(accounts: DeregisterCurrencyAccounts) -> TransactionInstruction:
    keys: list[AccountMeta] = [
        AccountMeta(
            pubkey=accounts["update_authority_account"],
            is_signer=True,
            is_writable=True,
        ),
        AccountMeta(
            pubkey=accounts["market_vars_account"], is_signer=False, is_writable=False
        ),
        AccountMeta(
            pubkey=accounts["registered_currency"], is_signer=False, is_writable=True
        ),
        AccountMeta(
            pubkey=accounts["currency_mint"], is_signer=False, is_writable=False
        ),
        AccountMeta(
            pubkey=accounts["system_program"], is_signer=False, is_writable=False
        ),
    ]
    identifier = b"\xbd\xe9!\x197\xd8\x1cZ"
    encoded_args = b""
    data = identifier + encoded_args
    return TransactionInstruction(keys, PROGRAM_ID, data)
