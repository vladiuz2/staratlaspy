from staratlaspy.marketplace import MarketVars
from staratlaspy.marketplace import OpenOrdersCounter
from staratlaspy.marketplace import OrderAccount
from staratlaspy.marketplace import RegisteredCurrency
from staratlaspy.score.accounts import ScoreVars
from staratlaspy.score.accounts import ScoreVarsShip
from staratlaspy.score.accounts import ShipStaking
from staratlaspy.faction.accounts import PlayerFactionData
from staratlaspy.faction.program_id import PROGRAM_ID as faction_PROGRAM_ID
from staratlaspy.marketplace.program_id import PROGRAM_ID as marketplace_PROGRAM_ID
from staratlaspy.score.program_id import PROGRAM_ID as score_PROGRAM_ID

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

