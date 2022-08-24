# staratlaspy

A library to interact with StarAtlas solana programs.

Based on [Kevin Heavey's AnchorPy](https://kevinheavey.github.io/anchorpy/) that made this
a very easy job.

> This code is not associated with Star Atlas, Automata LLC, or any of their companies.

# Install

```bash
python3 -m pip install staratlaspy
```

# Usage

### Get individual fleet state

```python
from staratlaspy.score.accounts.score_vars_ship import ScoreVarsShip
from staratlaspy.score.accounts.ship_staking import ShipStaking
from staratlaspy.score import getShipStakingAccount, getScoreVarsShipAccount, ScoreStats
from solana.rpc.async_api import AsyncClient
import asyncio, json
from solana.publickey import PublicKey
client = AsyncClient("https://api.mainnet-beta.solana.com")
wallet = PublicKey('8BMwvX4CNk8iEaDrhL51fvwdiPKFkPc5BnnTxbwPYxtf')
mint = PublicKey('AkNbg12E9PatjkiAWJ3tAbM479gtcoA1gi6Joa925WKi')
async def main():
    shipStakingAccount, bump = getShipStakingAccount(wallet, mint)
    varsShipAccount, vbump = getScoreVarsShipAccount(mint)
    stakingData = await ShipStaking.fetch(client, shipStakingAccount)
    varsData = await ScoreVarsShip.fetch(client, varsShipAccount)
    await client.close()
    return ScoreStats(varsData, 
                      stakingData).to_json()
print(json.dumps(asyncio.run(main()),indent=2))
```
returns
```
{
  "arms_daily_burn_units": 17131,
  "arms_full_supply_deficit_units": 185221,
  "arms_optimal_supply_deficit_seconds": 84585.73706315039,
  "arms_optimal_supply_deficit_seconds_human": "23h 29m 45s",
  "arms_optimal_supply_deficit_units": 16770,
  "arms_remaining_percent": 23.045995002917252,
  "arms_remaining_seconds": 279765.4929368496,
  "arms_remaining_seconds_human": "3d 5h 42m 45s",
  "arms_remaining_units": 55469,
  "arms_total_capacity_seconds": 1213944.084,
  "arms_total_capacity_units": 240690,
  "food_daily_burn_units": 17550,
  "food_full_supply_deficit_units": 17182,
  "food_optimal_supply_deficit_seconds": 84585.73706315039,
  "food_optimal_supply_deficit_seconds_human": "23h 29m 45s",
  "food_optimal_supply_deficit_units": 17181,
  "food_remaining_percent": 76.78456113263282,
  "food_remaining_seconds": 279765.4929368496,
  "food_remaining_seconds_human": "3d 5h 42m 45s",
  "food_remaining_units": 56828,
  "food_total_capacity_seconds": 364351.23,
  "food_total_capacity_units": 74010,
  "fuel_daily_burn_units": 15460,
  "fuel_full_supply_deficit_units": 87670,
  "fuel_optimal_supply_deficit_seconds": 84585.73706315039,
  "fuel_optimal_supply_deficit_seconds_human": "23h 29m 45s",
  "fuel_optimal_supply_deficit_units": 15135,
  "fuel_remaining_percent": 36.346497974527956,
  "fuel_remaining_seconds": 279765.4929368496,
  "fuel_remaining_seconds_human": "3d 5h 42m 45s",
  "fuel_remaining_units": 50060,
  "fuel_total_capacity_seconds": 769717.878,
  "fuel_total_capacity_units": 137730,
  "min_capacity_seconds": 364332,
  "min_capacity_seconds_human": "4d 5h 12m 12s",
  "min_total_capacity_seconds": 364351.23,
  "seconds_inactive": 0,
  "seconds_inactive_human": "",
  "seconds_since_last_action": 84568.5070631504,
  "toolkit_daily_burn_units": 19221,
  "toolkit_full_supply_deficit_units": 106249,
  "toolkit_optimal_supply_deficit_seconds": 84587.73706315039,
  "toolkit_optimal_supply_deficit_seconds_human": "23h 29m 47s",
  "toolkit_optimal_supply_deficit_units": 18817,
  "toolkit_remaining_percent": 36.93862968057066,
  "toolkit_remaining_seconds": 279763.4929368496,
  "toolkit_remaining_seconds_human": "3d 5h 42m 43s",
  "toolkit_remaining_units": 62236,
  "toolkit_total_capacity_seconds": 757373.772,
  "toolkit_total_capacity_units": 168485
}
```

### Get all fleets info for a wallet

```python
import asyncio, json, httpx, prettytable
from solana.publickey import PublicKey
from typing import Any, List, Tuple, Union
from staratlas.score import  getShipStakingAccount, getScoreVarsShipAccount, getScoreEscrowAuthAccount
from solana.rpc.async_api import AsyncClient
from staratlas import fetch_multiple_accounts
from staratlas.score import ScoreVars, ShipStaking, ScoreStats

playerKey = PublicKey('8BMwvX4CNk8iEaDrhL51fvwdiPKFkPc5BnnTxbwPYxtf')

async def main():
    connection = AsyncClient("https://api.mainnet-beta.solana.com")
    async with httpx.AsyncClient() as client:
        r = await client.get('https://api.staratlas.club/nfts?category=ship')
        nfts = r.json()
        await client.aclose()
    mints = [PublicKey(nft.get('mint')) for nft in nfts]
    staking = [getShipStakingAccount(playerKey, mint)[0] for mint in mints]
    escrow = [getScoreEscrowAuthAccount(playerKey, mint)[0] for mint in mints]
    vars = [getScoreVarsShipAccount(mint)[0] for mint in mints]
    staking_state = await fetch_multiple_accounts(connection, staking)
    vars_state = await fetch_multiple_accounts(connection, vars)
    await connection.close()
    score_fleet = []
    last_stat = None
    for i in range(len(nfts)):
        if staking_state[i]:
            score_fleet.append({
                "nft": nfts[i],
                "staking": staking_state[i].to_json(),
                "vars": vars_state[i].to_json(),
                "accounts": {
                    "shipStaking": str(staking[i]),
                    "escrowAuth": str(escrow[i]),
                    "varsShip": str(vars[i])
                },
                "stats": ScoreStats(vars_state[i], staking_state[i]).to_json(),
                "resources_to_optimal_supply": ScoreStats(vars_state[i], staking_state[i]).limited_atlas_resupply(atlas = 1000)
            })
    print(json.dumps(score_fleet, indent=2))
asyncio.run(main())
```

This will display up-to-date info on a wallet's fleet.

including this:
```json    
{
    "stats": {
      "arms_daily_burn_units": 572185,
      "arms_full_supply_deficit_units": 11828958,
      "arms_optimal_supply_deficit_seconds": 672604.625,
      "arms_optimal_supply_deficit_seconds_human": "7d 18h 50m 4s",
      "arms_optimal_supply_deficit_units": 4454335,
      "arms_remaining_percent": 0,
      "arms_remaining_seconds": 0,
      "arms_remaining_seconds_human": "",
      "arms_remaining_units": 0,
      "arms_total_capacity_seconds": 1786172.658,
      "arms_total_capacity_units": 11828958,
      "food_daily_burn_units": 377018,
      "food_full_supply_deficit_units": 2934998,
      "food_optimal_supply_deficit_seconds": 672603.625,
      "food_optimal_supply_deficit_seconds_human": "7d 18h 50m 3s",
      "food_optimal_supply_deficit_units": 2934997,
      "food_remaining_percent": 0.00014867575434825475,
      "food_remaining_seconds": 1.0,
      "food_remaining_seconds_human": "1s",
      "food_remaining_units": 4,
      "food_total_capacity_seconds": 672604.625,
      "food_total_capacity_units": 2935002,
      "fuel_daily_burn_units": 381176,
      "fuel_full_supply_deficit_units": 4921316,
      "fuel_optimal_supply_deficit_seconds": 672603.625,
      "fuel_optimal_supply_deficit_seconds_human": "7d 18h 50m 3s",
      "fuel_optimal_supply_deficit_units": 2967368,
      "fuel_remaining_percent": 8.964596299127781e-05,
      "fuel_remaining_seconds": 1.0,
      "fuel_remaining_seconds_human": "1s",
      "fuel_remaining_units": 4,
      "fuel_total_capacity_seconds": 1115499.2,
      "fuel_total_capacity_units": 4921320,
      "min_capacity_seconds": 309949,
      "min_capacity_seconds_human": "3d 14h 5m 49s",
      "min_total_capacity_seconds": 672604.625,
      "seconds_inactive": 208707.7673690319,
      "seconds_inactive_human": "2d 9h 58m 27s",
      "seconds_since_last_action": 518656.7673690319,
      "toolkit_daily_burn_units": 593135,
      "toolkit_full_supply_deficit_units": 9249707,
      "toolkit_optimal_supply_deficit_seconds": 672603.625,
      "toolkit_optimal_supply_deficit_seconds_human": "7d 18h 50m 3s",
      "toolkit_optimal_supply_deficit_units": 4617416,
      "toolkit_remaining_percent": 7.421838727502712e-05,
      "toolkit_remaining_seconds": 1.0,
      "toolkit_remaining_seconds_human": "1s",
      "toolkit_remaining_units": 7,
      "toolkit_total_capacity_seconds": 1347375.006,
      "toolkit_total_capacity_units": 9249714
    },
    "resources_to_optimal_supply": {
      "food": 742948,
      "fuel": 751142,
      "arms": 1127549,
      "toolkit": 1168825
    }
}
```


### Get faction account state

```python
from staratlaspy.faction import getPlayerFactionAccount
from staratlaspy.faction.accounts import PlayerFactionData
from solana.rpc.async_api import AsyncClient
import asyncio, json
from solana.publickey import PublicKey
client = AsyncClient("https://api.mainnet-beta.solana.com")
async def main():
    factionAccount, bump = getPlayerFactionAccount(PublicKey('9p5C9hvZiyypdoLR6PrBzug12sZtmpSXAkfNxa8SEevg'))
    factData = await PlayerFactionData.fetch(client, factionAccount)
    await client.close()
    return factData.to_json()
print(json.dumps(asyncio.run(main()),indent=2))
```

returns

```json
{
  "owner": "9p5C9hvZiyypdoLR6PrBzug12sZtmpSXAkfNxa8SEevg",
  "enlisted_at_timestamp": 1658765500,
  "faction_id": 0,
  "bump": 255,
  "padding": [
    0,
    0,
    0,
    0,
    0
  ]
}
```

### Get multiple accounts of different types

```python
from solana.rpc.async_api import AsyncClient
from staratlas import fetch_multiple_accounts
import asyncio, json

client = AsyncClient("https://api.mainnet-beta.solana.com")
accounts = asyncio.run(fetch_multiple_accounts(client, [
    "CkPEsmgfeCV4RcLHWA6jNaDWaGkVXT5Q2TTsysXyRk2B",
    "Tx4YJpozxG2U6R2PvszvW1872em7J8xMY59CgfhndFf",  
    "ADNPGtWPcsrbYakFPHCKFnEv9yWpuo7zAQaUU9rwtvFA"
]))


print(
    json.dumps([
        account.to_json() 
        for account in accounts], 
    indent=2)
)
```

output:

```json
[
  {
    "owner": "8BMwvX4CNk8iEaDrhL51fvwdiPKFkPc5BnnTxbwPYxtf",
    "faction_id": 0,
    "ship_mint": "8RveLFEyteyL1vbCKPQJxjf3JT1ACyrzs46TXbJStrHG",
    "ship_quantity_in_escrow": 150,
    "fuel_quantity_in_escrow": 25161666,
    "food_quantity_in_escrow": 20395265,
    "arms_quantity_in_escrow": 33968125,
    "fuel_current_capacity": 259085,
    "food_current_capacity": 259085,
    "arms_current_capacity": 259085,
    "health_current_capacity": 259085,
    "staked_at_timestamp": 1642501894,
    "fueled_at_timestamp": 1658658240,
    "fed_at_timestamp": 1658658240,
    "armed_at_timestamp": 1658658240,
    "repaired_at_timestamp": 1658658240,
    "current_capacity_timestamp": 1658658240,
    "total_time_staked": 13676418,
    "staked_time_paid": 13510428,
    "pending_rewards": 0,
    "total_rewards_paid": 90449613374400
  },
  {
    "update_authority_master": "DH3QYef5ATXfjULMMpnTvUmB3ocTm7ewgmwNBeZ26n9K",
    "fuel_mint": "fueL3hBZjLLLJHiFH9cqZoozTG3XQZ53diwFPwbzNim",
    "food_mint": "foodQJAztMzX1DKpLaiounNe2BDMds5RNuPC6jsNrDG",
    "arms_mint": "ammoK8AkX2wnebQb35cDAZtTkvsXQbi82cGeTnUvvfK",
    "toolkit_mint": "tooLsNYLiVqzg8o4m3L2Uetbn62mvMWRqkog6PQeYKL"
  }
]
```

# Author

* vlad@theclubguild.com

* Visit: https://theclubguild.com/

* [Discord](https://discord.gg/the-sa-club) | [Twitter](https://twitter.com/TheClubGuild)
| [Youtube](https://www.youtube.com/channel/UCMTp0p-oOsZB8UETrCr53XA?sub_confirmation=1)

# License

[Creative Commons Attribution-NonCommercial-NoDerivatives 4.0 International Public License](LICENSE.txt)
