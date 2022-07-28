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
    ...
    "stats": {
      "seconds_remaining": 49045,
      "seconds_since_last_action": 29841,
      "fuel_daily_burn": 11285,
      "fuel_total_capacity_seconds": 163459,
      "fuel_current_supply_to_total_capacity_percent": 0.8174404590753644,
      "fuel_total_capacity": 21349,
      "fuel_current_supply": 17451,
      "fuel_needed_for_full_supply": 3897,
      "fuel_needed_for_optimal_supply": 0,
      "arms_daily_burn": 7930,
      "arms_total_capacity_seconds": 279138,
      "arms_current_supply_to_total_capacity_percent": 0.8930958880553704,
      "arms_total_capacity": 25619,
      "arms_current_supply": 22880,
      "arms_needed_for_full_supply": 2738,
      "arms_needed_for_optimal_supply": 0,
      "food_daily_burn": 7015,
      "food_total_capacity_seconds": 78886,
      "food_current_supply_to_total_capacity_percent": 0.6217199503080395,
      "food_total_capacity": 6404,
      "food_current_supply": 3981,
      "food_needed_for_full_supply": 2422,
      "food_needed_for_optimal_supply": 2423,
      "toolkit_daily_burn": 10980,
      "toolkit_total_capacity_seconds": 163200,
      "toolkit_current_supply_to_total_capacity_percent": 0.8171507352941176,
      "toolkit_total_capacity": 20740,
      "toolkit_current_supply": 16947,
      "toolkit_needed_for_full_supply": 3792,
      "toolkit_needed_for_optimal_supply": 0
    },
    "resources_to_optimal_supply": {
      "food": 9164,
      "fuel": 11455,
      "arms": 15464,
      "toolkit": 16035
    }
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
