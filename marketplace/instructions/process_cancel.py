from __future__ import annotations
import typing
from solana.publickey import PublicKey
from solana.transaction import TransactionInstruction, AccountMeta
from ..program_id import PROGRAM_ID


class ProcessCancelAccounts(typing.TypedDict):
    order_initializer: PublicKey
    deposit_mint: PublicKey
    initializer_deposit_token_account: PublicKey
    order_vault_account: PublicKey
    order_vault_authority: PublicKey
    order_account: PublicKey
    open_orders_counter: PublicKey
    token_program: PublicKey


def process_cancel(accounts: ProcessCancelAccounts) -> TransactionInstruction:
    keys: list[AccountMeta] = [
        AccountMeta(
            pubkey=accounts["order_initializer"], is_signer=True, is_writable=True
        ),
        AccountMeta(
            pubkey=accounts["deposit_mint"], is_signer=False, is_writable=False
        ),
        AccountMeta(
            pubkey=accounts["initializer_deposit_token_account"],
            is_signer=False,
            is_writable=True,
        ),
        AccountMeta(
            pubkey=accounts["order_vault_account"], is_signer=False, is_writable=True
        ),
        AccountMeta(
            pubkey=accounts["order_vault_authority"], is_signer=False, is_writable=False
        ),
        AccountMeta(
            pubkey=accounts["order_account"], is_signer=False, is_writable=True
        ),
        AccountMeta(
            pubkey=accounts["open_orders_counter"], is_signer=False, is_writable=True
        ),
        AccountMeta(
            pubkey=accounts["token_program"], is_signer=False, is_writable=False
        ),
    ]
    identifier = b"UT\xd6\xf0\x8c)\xe6\x95"
    encoded_args = b""
    data = identifier + encoded_args
    return TransactionInstruction(keys, PROGRAM_ID, data)
