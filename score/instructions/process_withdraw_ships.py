from __future__ import annotations
import typing
from solana.publickey import PublicKey
from solana.transaction import TransactionInstruction, AccountMeta
import borsh_construct as borsh
from ..program_id import PROGRAM_ID


class ProcessWithdrawShipsArgs(typing.TypedDict):
    staking_bump: int
    scorevars_bump: int
    scorevars_ship_bump: int
    escrow_auth_bump: int
    escrow_bump: int
    treasury_auth_bump: int
    treasury_bump: int


layout = borsh.CStruct(
    "staking_bump" / borsh.U8,
    "scorevars_bump" / borsh.U8,
    "scorevars_ship_bump" / borsh.U8,
    "escrow_auth_bump" / borsh.U8,
    "escrow_bump" / borsh.U8,
    "treasury_auth_bump" / borsh.U8,
    "treasury_bump" / borsh.U8,
)


class ProcessWithdrawShipsAccounts(typing.TypedDict):
    player_account: PublicKey
    ship_staking_account: PublicKey
    score_vars_account: PublicKey
    score_vars_ship_account: PublicKey
    player_atlas_token_account: PublicKey
    ship_token_account_escrow: PublicKey
    ship_token_account_return: PublicKey
    toolkit_token_account_source: PublicKey
    treasury_token_account: PublicKey
    treasury_authority_account: PublicKey
    escrow_authority: PublicKey
    token_program: PublicKey
    system_program: PublicKey
    clock: PublicKey
    ship_mint: PublicKey
    toolkit_mint: PublicKey


def process_withdraw_ships(
    args: ProcessWithdrawShipsArgs, accounts: ProcessWithdrawShipsAccounts
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
            pubkey=accounts["ship_token_account_escrow"],
            is_signer=False,
            is_writable=True,
        ),
        AccountMeta(
            pubkey=accounts["ship_token_account_return"],
            is_signer=False,
            is_writable=True,
        ),
        AccountMeta(
            pubkey=accounts["toolkit_token_account_source"],
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
            pubkey=accounts["escrow_authority"], is_signer=False, is_writable=False
        ),
        AccountMeta(
            pubkey=accounts["token_program"], is_signer=False, is_writable=False
        ),
        AccountMeta(
            pubkey=accounts["system_program"], is_signer=False, is_writable=False
        ),
        AccountMeta(pubkey=accounts["clock"], is_signer=False, is_writable=False),
        AccountMeta(pubkey=accounts["ship_mint"], is_signer=False, is_writable=False),
        AccountMeta(pubkey=accounts["toolkit_mint"], is_signer=False, is_writable=True),
    ]
    identifier = b"K\xc6\x17\xd1\xab\xe4\xcfU"
    encoded_args = layout.build(
        {
            "staking_bump": args["staking_bump"],
            "scorevars_bump": args["scorevars_bump"],
            "scorevars_ship_bump": args["scorevars_ship_bump"],
            "escrow_auth_bump": args["escrow_auth_bump"],
            "escrow_bump": args["escrow_bump"],
            "treasury_auth_bump": args["treasury_auth_bump"],
            "treasury_bump": args["treasury_bump"],
        }
    )
    data = identifier + encoded_args
    return TransactionInstruction(keys, PROGRAM_ID, data)
