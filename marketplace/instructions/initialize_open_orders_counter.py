from __future__ import annotations
import typing
from solana.publickey import PublicKey
from solana.transaction import TransactionInstruction, AccountMeta
from ..program_id import PROGRAM_ID


class InitializeOpenOrdersCounterAccounts(typing.TypedDict):
    user: PublicKey
    open_orders_counter: PublicKey
    deposit_mint: PublicKey
    system_program: PublicKey


def initialize_open_orders_counter(
    accounts: InitializeOpenOrdersCounterAccounts,
) -> TransactionInstruction:
    keys: list[AccountMeta] = [
        AccountMeta(pubkey=accounts["user"], is_signer=True, is_writable=True),
        AccountMeta(
            pubkey=accounts["open_orders_counter"], is_signer=False, is_writable=True
        ),
        AccountMeta(
            pubkey=accounts["deposit_mint"], is_signer=False, is_writable=False
        ),
        AccountMeta(
            pubkey=accounts["system_program"], is_signer=False, is_writable=False
        ),
    ]
    identifier = b"\xdd\x86\x05L\x04\x91\xca\x1d"
    encoded_args = b""
    data = identifier + encoded_args
    return TransactionInstruction(keys, PROGRAM_ID, data)
