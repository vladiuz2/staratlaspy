from __future__ import annotations
import typing
from solana.publickey import PublicKey
from solana.transaction import TransactionInstruction, AccountMeta
import borsh_construct as borsh
from ..program_id import PROGRAM_ID


class ProcessInitialDepositArgs(typing.TypedDict):
    staking_bump: int
    scorevars_ship_bump: int
    escrow_auth_bump: int
    escrow_bump: int
    ship_quantity: int


layout = borsh.CStruct(
    "staking_bump" / borsh.U8,
    "scorevars_ship_bump" / borsh.U8,
    "escrow_auth_bump" / borsh.U8,
    "escrow_bump" / borsh.U8,
    "ship_quantity" / borsh.U64,
)


class ProcessInitialDepositAccounts(typing.TypedDict):
    player_account: PublicKey
    ship_staking_account: PublicKey
    score_vars_ship_account: PublicKey
    player_faction_account: PublicKey
    escrow_authority: PublicKey
    system_program: PublicKey
    token_program: PublicKey
    clock: PublicKey
    rent: PublicKey
    ship_mint: PublicKey
    ship_token_account_source: PublicKey
    ship_token_account_escrow: PublicKey


def process_initial_deposit(
    args: ProcessInitialDepositArgs, accounts: ProcessInitialDepositAccounts
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
            pubkey=accounts["player_faction_account"],
            is_signer=False,
            is_writable=False,
        ),
        AccountMeta(
            pubkey=accounts["escrow_authority"], is_signer=False, is_writable=False
        ),
        AccountMeta(
            pubkey=accounts["system_program"], is_signer=False, is_writable=False
        ),
        AccountMeta(
            pubkey=accounts["token_program"], is_signer=False, is_writable=False
        ),
        AccountMeta(pubkey=accounts["clock"], is_signer=False, is_writable=False),
        AccountMeta(pubkey=accounts["rent"], is_signer=False, is_writable=False),
        AccountMeta(pubkey=accounts["ship_mint"], is_signer=False, is_writable=False),
        AccountMeta(
            pubkey=accounts["ship_token_account_source"],
            is_signer=False,
            is_writable=True,
        ),
        AccountMeta(
            pubkey=accounts["ship_token_account_escrow"],
            is_signer=False,
            is_writable=True,
        ),
    ]
    identifier = b"\xfb\x16,\xe7\xc9\x89\xda\xa2"
    encoded_args = layout.build(
        {
            "staking_bump": args["staking_bump"],
            "scorevars_ship_bump": args["scorevars_ship_bump"],
            "escrow_auth_bump": args["escrow_auth_bump"],
            "escrow_bump": args["escrow_bump"],
            "ship_quantity": args["ship_quantity"],
        }
    )
    data = identifier + encoded_args
    return TransactionInstruction(keys, PROGRAM_ID, data)
