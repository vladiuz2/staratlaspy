from __future__ import annotations
import typing
from solana.publickey import PublicKey
from solana.transaction import TransactionInstruction, AccountMeta
import borsh_construct as borsh
from ..program_id import PROGRAM_ID


class ProcessDeregisterShipArgs(typing.TypedDict):
    scorevars_bump: int
    scorevars_ship_bump: int


layout = borsh.CStruct("scorevars_bump" / borsh.U8, "scorevars_ship_bump" / borsh.U8)


class ProcessDeregisterShipAccounts(typing.TypedDict):
    update_authority_account: PublicKey
    score_vars_account: PublicKey
    score_vars_ship_account: PublicKey
    ship_mint: PublicKey


def process_deregister_ship(
    args: ProcessDeregisterShipArgs, accounts: ProcessDeregisterShipAccounts
) -> TransactionInstruction:
    keys: list[AccountMeta] = [
        AccountMeta(
            pubkey=accounts["update_authority_account"],
            is_signer=True,
            is_writable=False,
        ),
        AccountMeta(
            pubkey=accounts["score_vars_account"], is_signer=False, is_writable=False
        ),
        AccountMeta(
            pubkey=accounts["score_vars_ship_account"],
            is_signer=False,
            is_writable=True,
        ),
        AccountMeta(pubkey=accounts["ship_mint"], is_signer=False, is_writable=False),
    ]
    identifier = b"\r>\xb6\xdb\xb4\x00\xc3M"
    encoded_args = layout.build(
        {
            "scorevars_bump": args["scorevars_bump"],
            "scorevars_ship_bump": args["scorevars_ship_bump"],
        }
    )
    data = identifier + encoded_args
    return TransactionInstruction(keys, PROGRAM_ID, data)
