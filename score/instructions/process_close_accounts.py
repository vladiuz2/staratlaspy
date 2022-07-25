from __future__ import annotations
import typing
from solana.publickey import PublicKey
from solana.transaction import TransactionInstruction, AccountMeta
import borsh_construct as borsh
from ..program_id import PROGRAM_ID


class ProcessCloseAccountsArgs(typing.TypedDict):
    staking_bump: int
    scorevars_bump: int
    ship_bump: int
    fuel_bump: int
    food_bump: int
    arms_bump: int
    escrow_auth_bump: int


layout = borsh.CStruct(
    "staking_bump" / borsh.U8,
    "scorevars_bump" / borsh.U8,
    "ship_bump" / borsh.U8,
    "fuel_bump" / borsh.U8,
    "food_bump" / borsh.U8,
    "arms_bump" / borsh.U8,
    "escrow_auth_bump" / borsh.U8,
)


class ProcessCloseAccountsAccounts(typing.TypedDict):
    player_account: PublicKey
    ship_staking_account: PublicKey
    score_vars_account: PublicKey
    ship_token_account_escrow: PublicKey
    fuel_token_account_escrow: PublicKey
    food_token_account_escrow: PublicKey
    arms_token_account_escrow: PublicKey
    escrow_authority: PublicKey
    token_program: PublicKey
    system_program: PublicKey
    ship_mint: PublicKey
    fuel_mint: PublicKey
    food_mint: PublicKey
    arms_mint: PublicKey
    clock: PublicKey


def process_close_accounts(
    args: ProcessCloseAccountsArgs, accounts: ProcessCloseAccountsAccounts
) -> TransactionInstruction:
    keys: list[AccountMeta] = [
        AccountMeta(
            pubkey=accounts["player_account"], is_signer=True, is_writable=False
        ),
        AccountMeta(
            pubkey=accounts["ship_staking_account"], is_signer=False, is_writable=True
        ),
        AccountMeta(
            pubkey=accounts["score_vars_account"], is_signer=False, is_writable=False
        ),
        AccountMeta(
            pubkey=accounts["ship_token_account_escrow"],
            is_signer=False,
            is_writable=True,
        ),
        AccountMeta(
            pubkey=accounts["fuel_token_account_escrow"],
            is_signer=False,
            is_writable=True,
        ),
        AccountMeta(
            pubkey=accounts["food_token_account_escrow"],
            is_signer=False,
            is_writable=True,
        ),
        AccountMeta(
            pubkey=accounts["arms_token_account_escrow"],
            is_signer=False,
            is_writable=True,
        ),
        AccountMeta(
            pubkey=accounts["escrow_authority"], is_signer=False, is_writable=False
        ),
        AccountMeta(
            pubkey=accounts["token_program"], is_signer=False, is_writable=False
        ),
        AccountMeta(
            pubkey=accounts["system_program"], is_signer=False, is_writable=False
        ),
        AccountMeta(pubkey=accounts["ship_mint"], is_signer=False, is_writable=False),
        AccountMeta(pubkey=accounts["fuel_mint"], is_signer=False, is_writable=False),
        AccountMeta(pubkey=accounts["food_mint"], is_signer=False, is_writable=False),
        AccountMeta(pubkey=accounts["arms_mint"], is_signer=False, is_writable=False),
        AccountMeta(pubkey=accounts["clock"], is_signer=False, is_writable=False),
    ]
    identifier = b"\xac\x02\xc5\xaaq\xe1\xbeZ"
    encoded_args = layout.build(
        {
            "staking_bump": args["staking_bump"],
            "scorevars_bump": args["scorevars_bump"],
            "ship_bump": args["ship_bump"],
            "fuel_bump": args["fuel_bump"],
            "food_bump": args["food_bump"],
            "arms_bump": args["arms_bump"],
            "escrow_auth_bump": args["escrow_auth_bump"],
        }
    )
    data = identifier + encoded_args
    return TransactionInstruction(keys, PROGRAM_ID, data)
