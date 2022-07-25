from __future__ import annotations
import typing
from solana.publickey import PublicKey
from solana.transaction import TransactionInstruction, AccountMeta
import borsh_construct as borsh
from ..program_id import PROGRAM_ID


class ProcessRegisterShipArgs(typing.TypedDict):
    scorevars_ship_bump: int
    scorevars_bump: int
    reward_rate_per_second: int
    fuel_max_reserve: int
    food_max_reserve: int
    arms_max_reserve: int
    toolkit_max_reserve: int
    milliseconds_to_burn_one_fuel: int
    milliseconds_to_burn_one_food: int
    milliseconds_to_burn_one_arms: int
    milliseconds_to_burn_one_toolkit: int


layout = borsh.CStruct(
    "scorevars_ship_bump" / borsh.U8,
    "scorevars_bump" / borsh.U8,
    "reward_rate_per_second" / borsh.U64,
    "fuel_max_reserve" / borsh.U32,
    "food_max_reserve" / borsh.U32,
    "arms_max_reserve" / borsh.U32,
    "toolkit_max_reserve" / borsh.U32,
    "milliseconds_to_burn_one_fuel" / borsh.U32,
    "milliseconds_to_burn_one_food" / borsh.U32,
    "milliseconds_to_burn_one_arms" / borsh.U32,
    "milliseconds_to_burn_one_toolkit" / borsh.U32,
)


class ProcessRegisterShipAccounts(typing.TypedDict):
    update_authority_account: PublicKey
    score_vars_account: PublicKey
    score_vars_ship_account: PublicKey
    ship_mint: PublicKey
    system_program: PublicKey


def process_register_ship(
    args: ProcessRegisterShipArgs, accounts: ProcessRegisterShipAccounts
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
        AccountMeta(
            pubkey=accounts["system_program"], is_signer=False, is_writable=False
        ),
    ]
    identifier = b"\xc1\x98%T\x080\x0fZ"
    encoded_args = layout.build(
        {
            "scorevars_ship_bump": args["scorevars_ship_bump"],
            "scorevars_bump": args["scorevars_bump"],
            "reward_rate_per_second": args["reward_rate_per_second"],
            "fuel_max_reserve": args["fuel_max_reserve"],
            "food_max_reserve": args["food_max_reserve"],
            "arms_max_reserve": args["arms_max_reserve"],
            "toolkit_max_reserve": args["toolkit_max_reserve"],
            "milliseconds_to_burn_one_fuel": args["milliseconds_to_burn_one_fuel"],
            "milliseconds_to_burn_one_food": args["milliseconds_to_burn_one_food"],
            "milliseconds_to_burn_one_arms": args["milliseconds_to_burn_one_arms"],
            "milliseconds_to_burn_one_toolkit": args[
                "milliseconds_to_burn_one_toolkit"
            ],
        }
    )
    data = identifier + encoded_args
    return TransactionInstruction(keys, PROGRAM_ID, data)
