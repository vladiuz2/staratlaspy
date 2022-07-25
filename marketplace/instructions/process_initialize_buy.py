from __future__ import annotations
import typing
from solana.publickey import PublicKey
from solana.transaction import TransactionInstruction, AccountMeta
import borsh_construct as borsh
from ..program_id import PROGRAM_ID


class ProcessInitializeBuyArgs(typing.TypedDict):
    price: int
    origination_qty: int


layout = borsh.CStruct("price" / borsh.U64, "origination_qty" / borsh.U64)


class ProcessInitializeBuyAccounts(typing.TypedDict):
    order_initializer: PublicKey
    market_vars_account: PublicKey
    deposit_mint: PublicKey
    receive_mint: PublicKey
    order_vault_account: PublicKey
    order_vault_authority: PublicKey
    initializer_deposit_token_account: PublicKey
    initializer_receive_token_account: PublicKey
    order_account: PublicKey
    registered_currency: PublicKey
    open_orders_counter: PublicKey
    system_program: PublicKey
    rent: PublicKey
    token_program: PublicKey


def process_initialize_buy(
    args: ProcessInitializeBuyArgs, accounts: ProcessInitializeBuyAccounts
) -> TransactionInstruction:
    keys: list[AccountMeta] = [
        AccountMeta(
            pubkey=accounts["order_initializer"], is_signer=True, is_writable=True
        ),
        AccountMeta(
            pubkey=accounts["market_vars_account"], is_signer=False, is_writable=False
        ),
        AccountMeta(
            pubkey=accounts["deposit_mint"], is_signer=False, is_writable=False
        ),
        AccountMeta(
            pubkey=accounts["receive_mint"], is_signer=False, is_writable=False
        ),
        AccountMeta(
            pubkey=accounts["order_vault_account"], is_signer=False, is_writable=True
        ),
        AccountMeta(
            pubkey=accounts["order_vault_authority"], is_signer=False, is_writable=False
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
            pubkey=accounts["order_account"], is_signer=False, is_writable=True
        ),
        AccountMeta(
            pubkey=accounts["registered_currency"], is_signer=False, is_writable=False
        ),
        AccountMeta(
            pubkey=accounts["open_orders_counter"], is_signer=False, is_writable=True
        ),
        AccountMeta(
            pubkey=accounts["system_program"], is_signer=False, is_writable=False
        ),
        AccountMeta(pubkey=accounts["rent"], is_signer=False, is_writable=False),
        AccountMeta(
            pubkey=accounts["token_program"], is_signer=False, is_writable=False
        ),
    ]
    identifier = b"\x81\x8ef\xbe\x8ag\x91\x83"
    encoded_args = layout.build(
        {
            "price": args["price"],
            "origination_qty": args["origination_qty"],
        }
    )
    data = identifier + encoded_args
    return TransactionInstruction(keys, PROGRAM_ID, data)
