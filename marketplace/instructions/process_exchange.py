from __future__ import annotations
import typing
from solana.publickey import PublicKey
from solana.transaction import TransactionInstruction, AccountMeta
import borsh_construct as borsh
from ..program_id import PROGRAM_ID


class ProcessExchangeArgs(typing.TypedDict):
    purchase_quantity: int


layout = borsh.CStruct("purchase_quantity" / borsh.U64)


class ProcessExchangeAccounts(typing.TypedDict):
    order_taker: PublicKey
    order_taker_deposit_token_account: PublicKey
    order_taker_receive_token_account: PublicKey
    currency_mint: PublicKey
    asset_mint: PublicKey
    order_initializer: PublicKey
    initializer_deposit_token_account: PublicKey
    initializer_receive_token_account: PublicKey
    order_vault_account: PublicKey
    order_vault_authority: PublicKey
    order_account: PublicKey
    sa_vault: PublicKey
    registered_currency: PublicKey
    open_orders_counter: PublicKey
    token_program: PublicKey


def process_exchange(
    args: ProcessExchangeArgs, accounts: ProcessExchangeAccounts
) -> TransactionInstruction:
    keys: list[AccountMeta] = [
        AccountMeta(pubkey=accounts["order_taker"], is_signer=True, is_writable=True),
        AccountMeta(
            pubkey=accounts["order_taker_deposit_token_account"],
            is_signer=False,
            is_writable=True,
        ),
        AccountMeta(
            pubkey=accounts["order_taker_receive_token_account"],
            is_signer=False,
            is_writable=True,
        ),
        AccountMeta(
            pubkey=accounts["currency_mint"], is_signer=False, is_writable=False
        ),
        AccountMeta(pubkey=accounts["asset_mint"], is_signer=False, is_writable=False),
        AccountMeta(
            pubkey=accounts["order_initializer"], is_signer=False, is_writable=True
        ),
        AccountMeta(
            pubkey=accounts["initializer_deposit_token_account"],
            is_signer=False,
            is_writable=True,
        ),
        AccountMeta(
            pubkey=accounts["initializer_receive_token_account"],
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
        AccountMeta(pubkey=accounts["sa_vault"], is_signer=False, is_writable=True),
        AccountMeta(
            pubkey=accounts["registered_currency"], is_signer=False, is_writable=False
        ),
        AccountMeta(
            pubkey=accounts["open_orders_counter"], is_signer=False, is_writable=True
        ),
        AccountMeta(
            pubkey=accounts["token_program"], is_signer=False, is_writable=False
        ),
    ]
    identifier = b"p\xc2?c4\x93U0"
    encoded_args = layout.build(
        {
            "purchase_quantity": args["purchase_quantity"],
        }
    )
    data = identifier + encoded_args
    return TransactionInstruction(keys, PROGRAM_ID, data)
