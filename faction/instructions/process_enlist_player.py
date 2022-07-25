from __future__ import annotations
import typing
from solana.publickey import PublicKey
from solana.transaction import TransactionInstruction, AccountMeta
import borsh_construct as borsh
from ..program_id import PROGRAM_ID


class ProcessEnlistPlayerArgs(typing.TypedDict):
    bump: int
    faction_id: int


layout = borsh.CStruct("bump" / borsh.U8, "faction_id" / borsh.U8)


class ProcessEnlistPlayerAccounts(typing.TypedDict):
    player_faction_account: PublicKey
    player_account: PublicKey
    system_program: PublicKey
    clock: PublicKey


def process_enlist_player(
    args: ProcessEnlistPlayerArgs, accounts: ProcessEnlistPlayerAccounts
) -> TransactionInstruction:
    keys: list[AccountMeta] = [
        AccountMeta(
            pubkey=accounts["player_faction_account"], is_signer=False, is_writable=True
        ),
        AccountMeta(
            pubkey=accounts["player_account"], is_signer=True, is_writable=False
        ),
        AccountMeta(
            pubkey=accounts["system_program"], is_signer=False, is_writable=False
        ),
        AccountMeta(pubkey=accounts["clock"], is_signer=False, is_writable=False),
    ]
    identifier = b"\xc6j>\xa7w.\xcfQ"
    encoded_args = layout.build(
        {
            "bump": args["bump"],
            "faction_id": args["faction_id"],
        }
    )
    data = identifier + encoded_args
    return TransactionInstruction(keys, PROGRAM_ID, data)
