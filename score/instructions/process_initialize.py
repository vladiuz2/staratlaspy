from __future__ import annotations
import typing
from solana.publickey import PublicKey
from solana.transaction import TransactionInstruction, AccountMeta
import borsh_construct as borsh
from ..program_id import PROGRAM_ID


class ProcessInitializeArgs(typing.TypedDict):
    bump: int
    treasury_bump: int
    treasury_auth_bump: int


layout = borsh.CStruct(
    "bump" / borsh.U8, "treasury_bump" / borsh.U8, "treasury_auth_bump" / borsh.U8
)


class ProcessInitializeAccounts(typing.TypedDict):
    update_authority_account: PublicKey
    score_vars_account: PublicKey
    token_program: PublicKey
    system_program: PublicKey
    rent: PublicKey
    treasury_token_account: PublicKey
    treasury_authority_account: PublicKey
    atlas_mint: PublicKey
    fuel_mint: PublicKey
    food_mint: PublicKey
    arms_mint: PublicKey
    toolkit_mint: PublicKey


def process_initialize(
    args: ProcessInitializeArgs, accounts: ProcessInitializeAccounts
) -> TransactionInstruction:
    keys: list[AccountMeta] = [
        AccountMeta(
            pubkey=accounts["update_authority_account"],
            is_signer=True,
            is_writable=False,
        ),
        AccountMeta(
            pubkey=accounts["score_vars_account"], is_signer=False, is_writable=True
        ),
        AccountMeta(
            pubkey=accounts["token_program"], is_signer=False, is_writable=False
        ),
        AccountMeta(
            pubkey=accounts["system_program"], is_signer=False, is_writable=False
        ),
        AccountMeta(pubkey=accounts["rent"], is_signer=False, is_writable=False),
        AccountMeta(
            pubkey=accounts["treasury_token_account"], is_signer=False, is_writable=True
        ),
        AccountMeta(
            pubkey=accounts["treasury_authority_account"],
            is_signer=False,
            is_writable=False,
        ),
        AccountMeta(pubkey=accounts["atlas_mint"], is_signer=False, is_writable=False),
        AccountMeta(pubkey=accounts["fuel_mint"], is_signer=False, is_writable=False),
        AccountMeta(pubkey=accounts["food_mint"], is_signer=False, is_writable=False),
        AccountMeta(pubkey=accounts["arms_mint"], is_signer=False, is_writable=False),
        AccountMeta(
            pubkey=accounts["toolkit_mint"], is_signer=False, is_writable=False
        ),
    ]
    identifier = b"\xb8X\x14\xad\x113Q\x85"
    encoded_args = layout.build(
        {
            "bump": args["bump"],
            "treasury_bump": args["treasury_bump"],
            "treasury_auth_bump": args["treasury_auth_bump"],
        }
    )
    data = identifier + encoded_args
    return TransactionInstruction(keys, PROGRAM_ID, data)
