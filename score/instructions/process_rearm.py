from __future__ import annotations
import typing
from solana.publickey import PublicKey
from solana.transaction import TransactionInstruction, AccountMeta
import borsh_construct as borsh
from ..program_id import PROGRAM_ID


class ProcessRearmArgs(typing.TypedDict):
    staking_bump: int
    scorevars_bump: int
    scorevars_ship_bump: int
    escrow_auth_bump: int
    escrow_bump: int
    arms_quantity: int


layout = borsh.CStruct(
    "staking_bump" / borsh.U8,
    "scorevars_bump" / borsh.U8,
    "scorevars_ship_bump" / borsh.U8,
    "escrow_auth_bump" / borsh.U8,
    "escrow_bump" / borsh.U8,
    "arms_quantity" / borsh.U64,
)


class ProcessRearmAccounts(typing.TypedDict):
    token_owner_account: PublicKey
    player_account: PublicKey
    ship_staking_account: PublicKey
    score_vars_account: PublicKey
    score_vars_ship_account: PublicKey
    escrow_authority: PublicKey
    system_program: PublicKey
    token_program: PublicKey
    clock: PublicKey
    rent: PublicKey
    ship_mint: PublicKey
    arms_mint: PublicKey
    arms_token_account_source: PublicKey
    arms_token_account_escrow: PublicKey


def process_rearm(
    args: ProcessRearmArgs, accounts: ProcessRearmAccounts
) -> TransactionInstruction:
    keys: list[AccountMeta] = [
        AccountMeta(
            pubkey=accounts["token_owner_account"], is_signer=True, is_writable=False
        ),
        AccountMeta(
            pubkey=accounts["player_account"], is_signer=False, is_writable=False
        ),
        AccountMeta(
            pubkey=accounts["ship_staking_account"], is_signer=False, is_writable=True
        ),
        AccountMeta(
            pubkey=accounts["score_vars_account"], is_signer=False, is_writable=False
        ),
        AccountMeta(
            pubkey=accounts["score_vars_ship_account"],
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
        AccountMeta(pubkey=accounts["arms_mint"], is_signer=False, is_writable=False),
        AccountMeta(
            pubkey=accounts["arms_token_account_source"],
            is_signer=False,
            is_writable=True,
        ),
        AccountMeta(
            pubkey=accounts["arms_token_account_escrow"],
            is_signer=False,
            is_writable=True,
        ),
    ]
    identifier = b"B\x87\x1e\xc2\x9d\xdb!\xdb"
    encoded_args = layout.build(
        {
            "staking_bump": args["staking_bump"],
            "scorevars_bump": args["scorevars_bump"],
            "scorevars_ship_bump": args["scorevars_ship_bump"],
            "escrow_auth_bump": args["escrow_auth_bump"],
            "escrow_bump": args["escrow_bump"],
            "arms_quantity": args["arms_quantity"],
        }
    )
    data = identifier + encoded_args
    return TransactionInstruction(keys, PROGRAM_ID, data)
