from __future__ import annotations
import typing
from solana.publickey import PublicKey
from solana.transaction import TransactionInstruction, AccountMeta
from ..program_id import PROGRAM_ID


class UpdateCurrencyVaultAccounts(typing.TypedDict):
    update_authority_account: PublicKey
    market_vars_account: PublicKey
    registered_currency: PublicKey
    currency_mint: PublicKey
    sa_currency_vault: PublicKey
    system_program: PublicKey


def update_currency_vault(
    accounts: UpdateCurrencyVaultAccounts,
) -> TransactionInstruction:
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
            pubkey=accounts["sa_currency_vault"], is_signer=False, is_writable=False
        ),
        AccountMeta(
            pubkey=accounts["system_program"], is_signer=False, is_writable=False
        ),
    ]
    identifier = b"\x12\x88H\x1fL\xf2\nR"
    encoded_args = b""
    data = identifier + encoded_args
    return TransactionInstruction(keys, PROGRAM_ID, data)
