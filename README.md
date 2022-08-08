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


### Get fleet info for a wallet

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
      "arms_daily_burn_units": 52,
      "arms_full_supply_deficit_units": 101,
      "arms_optimal_supply_deficit_seconds": 0,
      "arms_optimal_supply_deficit_seconds_human": "",
      "arms_optimal_supply_deficit_units": 0,
      "arms_remaining_percent": 39.945449521933014,
      "arms_remaining_seconds": 111503.08227705956,
      "arms_remaining_seconds_human": "1d 6h 58m 23s",
      "arms_remaining_units": 67,
      "arms_total_capacity_seconds": 279138.384,
      "arms_total_capacity_units": 168,
      "food_daily_burn_units": 46,
      "food_full_supply_deficit_units": 36,
      "food_optimal_supply_deficit_seconds": 68089.85872294045,
      "food_optimal_supply_deficit_seconds_human": "18h 54m 49s",
      "food_optimal_supply_deficit_units": 36,
      "food_remaining_percent": 13.686780270842995,
      "food_remaining_seconds": 10797.082277059555,
      "food_remaining_seconds_human": "2h 59m 57s",
      "food_remaining_units": 6,
      "food_total_capacity_seconds": 78886.941,
      "food_total_capacity_units": 42,
      "fuel_daily_burn_units": 74,
      "fuel_full_supply_deficit_units": 120,
      "fuel_optimal_supply_deficit_seconds": 55042.85872294045,
      "fuel_optimal_supply_deficit_seconds_human": "15h 17m 22s",
      "fuel_optimal_supply_deficit_units": 47,
      "fuel_remaining_percent": 14.587154353608527,
      "fuel_remaining_seconds": 23844.082277059555,
      "fuel_remaining_seconds_human": "6h 37m 24s",
      "fuel_remaining_units": 20,
      "fuel_total_capacity_seconds": 163459.45,
      "fuel_total_capacity_units": 140,
      "min_capacity_seconds": 33808,
      "min_capacity_seconds_human": "9h 23m 28s",
      "min_total_capacity_seconds": 78886.941,
      "seconds_inactive": 0,
      "seconds_inactive_human": "",
      "seconds_since_last_action": 23010.917722940445,
      "toolkit_daily_burn_units": 72,
      "toolkit_full_supply_deficit_units": 107,
      "toolkit_optimal_supply_deficit_seconds": 43721.85872294045,
      "toolkit_optimal_supply_deficit_seconds_human": "12h 8m 41s",
      "toolkit_optimal_supply_deficit_units": 36,
      "toolkit_remaining_percent": 21.547231787413942,
      "toolkit_remaining_seconds": 35165.082277059555,
      "toolkit_remaining_seconds_human": "9h 46m 5s",
      "toolkit_remaining_units": 29,
      "toolkit_total_capacity_seconds": 163200.0,
      "toolkit_total_capacity_units": 136
    },
    "resources_to_optimal_supply": {
      "food": 36,
      "fuel": 47,
      "arms": 0,
      "toolkit": 36
    },
}
```


### Get faction account state

```python
from solana.rpc.async_api import AsyncClient
from staratlas.faction.accounts import PlayerFactionData
import asyncio, json

client = AsyncClient("https://api.mainnet-beta.solana.com")
async def main():
    factData = await PlayerFactionData.fetch(client, "31JkGcco7wi7x8Nyt48movzDiWqpr1dXeDSbKc6EpCga")
    return factData.to_json()

print(json.dumps(asyncio.run(main()), indent=2))
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
