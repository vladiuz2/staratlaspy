import typing

from base64 import b64decode
from solana.publickey import PublicKey
from solana.rpc.async_api import AsyncClient
from solana.rpc.commitment import Commitment

from anchorpy.utils.rpc import get_multiple_accounts

from .marketplace.accounts import MarketVars
from .marketplace.accounts import OpenOrdersCounter
from .marketplace.accounts import OrderAccount
from .marketplace.accounts import RegisteredCurrency
from .score.accounts import ScoreVars
from .score.accounts import ScoreVarsShip
from .score.accounts import ShipStaking
from .faction.accounts import PlayerFactionData
from .faction.program_id import PROGRAM_ID as faction_PROGRAM_ID
from .marketplace.program_id import PROGRAM_ID as marketplace_PROGRAM_ID
from .score.program_id import PROGRAM_ID as score_PROGRAM_ID

account_type_map = {}

for account_type_meta in [
        (marketplace_PROGRAM_ID, MarketVars),
        (marketplace_PROGRAM_ID, OpenOrdersCounter),
        (marketplace_PROGRAM_ID, OrderAccount),
        (marketplace_PROGRAM_ID, RegisteredCurrency),
        (score_PROGRAM_ID, ScoreVars),
        (score_PROGRAM_ID, ScoreVarsShip),
        (score_PROGRAM_ID,ShipStaking),
        (faction_PROGRAM_ID,PlayerFactionData)
    ]:
    program = account_type_map.get(account_type_meta[0], {})
    program[account_type_meta[1].discriminator] = account_type_meta[1]
    account_type_map[account_type_meta[0]] = program

async def fetch_multiple_accounts(
        client:AsyncClient,
        addresses: list[PublicKey],
        commitment: Commitment = Commitment('confirmed')
    ):
    resps = await get_multiple_accounts(client, addresses, commitment=commitment)
    result = []
    for resp in resps:
        if resp is None:
            result.append(None)
            continue
        if resp.account.owner in account_type_map.keys():
            program = account_type_map.get(resp.account.owner)
            if resp.account.data[:8] in program.keys():
                result.append(program.get(resp.account.data[:8]).decode(resp.account.data))
                continue
        result.append(resp)
    return result