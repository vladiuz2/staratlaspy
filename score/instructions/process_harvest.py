from __future__ import annotations
import typing
from solana.publickey import PublicKey
from solana.transaction import TransactionInstruction, AccountMeta
import borsh_construct as borsh
from ..program_id import PROGRAM_ID


class ProcessHarvestArgs(typing.TypedDict):
    staking_bump: int
    scorevars_ship_bump: int
    treasury_bump: int
    treasury_auth_bump: int


layout = borsh.CStruct(
    "staking_bump" / borsh.U8,
    "scorevars_ship_bump" / borsh.U8,
    "treasury_bump" / borsh.U8,
    "treasury_auth_bump" / borsh.U8,
)


class ProcessHarvestAccounts(typing.TypedDict):
    player_account: PublicKey
    ship_staking_account: PublicKey
    score_vars_ship_account: PublicKey
    player_atlas_token_account: PublicKey
    treasury_token_account: PublicKey
    treasury_authority_account: PublicKey
    token_program: PublicKey
    clock: PublicKey
    ship_mint: PublicKey


def process_harvest(
    args: ProcessHarvestArgs, accounts: ProcessHarvestAccounts
) -> TransactionInstruction:
    keys: list[AccountMeta] = [
        AccountMeta(
            pubkey=accounts["player_account"], is_signer=True, is_writable=False
        ),
        AccountMeta(
            pubkey=accounts["ship_staking_account"], is_signer=False, is_writable=True
        ),
        AccountMeta(
            pubkey=accounts["score_vars_ship_account"],
            is_signer=False,
            is_writable=False,
        ),
        AccountMeta(
            pubkey=accounts["player_atlas_token_account"],
            is_signer=False,
            is_writable=True,
        ),
        AccountMeta(
            pubkey=accounts["treasury_token_account"], is_signer=False, is_writable=True
        ),
        AccountMeta(
            pubkey=accounts["treasury_authority_account"],
            is_signer=False,
            is_writable=False,
        ),
        AccountMeta(
            pubkey=accounts["token_program"], is_signer=False, is_writable=False
        ),
        AccountMeta(pubkey=accounts["clock"], is_signer=False, is_writable=False),
        AccountMeta(pubkey=accounts["ship_mint"], is_signer=False, is_writable=False),
    ]
    identifier = b"\xbfFf)\xe2$\x7f\xa0"
    encoded_args = layout.build(
        {
            "staking_bump": args["staking_bump"],
            "scorevars_ship_bump": args["scorevars_ship_bump"],
            "treasury_bump": args["treasury_bump"],
            "treasury_auth_bump": args["treasury_auth_bump"],
        }
    )
    data = identifier + encoded_args
    return TransactionInstruction(keys, PROGRAM_ID, data)
