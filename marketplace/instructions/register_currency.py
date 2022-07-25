from __future__ import annotations
import typing
from solana.publickey import PublicKey
from solana.transaction import TransactionInstruction, AccountMeta
import borsh_construct as borsh
from ..program_id import PROGRAM_ID


class RegisterCurrencyArgs(typing.TypedDict):
    royalty: int


layout = borsh.CStruct("royalty" / borsh.U64)


class RegisterCurrencyAccounts(typing.TypedDict):
    update_authority_account: PublicKey
    market_vars_account: PublicKey
    registered_currency: PublicKey
    currency_mint: PublicKey
    sa_currency_vault: PublicKey
    system_program: PublicKey


def register_currency(
    args: RegisterCurrencyArgs, accounts: RegisterCurrencyAccounts
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
    identifier = b"\xf7\xe5s\xcc-$\xb3h"
    encoded_args = layout.build(
        {
            "royalty": args["royalty"],
        }
    )
    data = identifier + encoded_args
    return TransactionInstruction(keys, PROGRAM_ID, data)
