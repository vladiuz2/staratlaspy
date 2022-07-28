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
      "seconds_remaining": 413345,
      "seconds_since_last_action": 111432,
      "fuel_daily_burn": 281739,
      "fuel_total_capacity_seconds": 829280,
      "fuel_current_supply_to_total_capacity_percent": 0.4983744935365618,
      "fuel_total_capacity": 2704173,
      "fuel_current_supply": 1347690,
      "fuel_needed_for_full_supply": 1356482,
      "fuel_needed_for_optimal_supply": 363538,
      "arms_daily_burn": 380337,
      "arms_total_capacity_seconds": 1670122,
      "arms_current_supply_to_total_capacity_percent": 0.24746216144688832,
      "arms_total_capacity": 7351967,
      "arms_current_supply": 1819333,
      "arms_needed_for_full_supply": 5532633,
      "arms_needed_for_optimal_supply": 490763,
      "food_daily_burn": 225391,
      "food_total_capacity_seconds": 524777,
      "food_current_supply_to_total_capacity_percent": 0.7875592870876582,
      "food_total_capacity": 1368983,
      "food_current_supply": 1078155,
      "food_needed_for_full_supply": 290827,
      "food_needed_for_optimal_supply": 290828,
      "toolkit_daily_burn": 394370,
      "toolkit_total_capacity_seconds": 1155256,
      "toolkit_current_supply_to_total_capacity_percent": 0.35774927808208745,
      "toolkit_total_capacity": 5273135,
      "toolkit_current_supply": 1886460,
      "toolkit_needed_for_full_supply": 3386674,
      "toolkit_needed_for_optimal_supply": 508870
    },
    "resources_to_optimal_supply": {
      "food": 9164,
      "fuel": 11455,
      "arms": 15464,
      "toolkit": 16035
    },
    ...

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
