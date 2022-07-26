# staratlaspy

A library to interact with StarAtlas solana programs.

Based on [Kevin Heavey's AnchorPy](https://kevinheavey.github.io/anchorpy/) that made this
a very easy job.

> This code is not associated with Star Atlas, Automata LLC, or any of their companies.


# Usage


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

```
from solana.rpc.async_api import AsyncClient
from staratlas import fetch_multiple_accounts
import asyncio, json

client = AsyncClient("https://api.mainnet-beta.solana.com")
accounts = asyncio.run(fetch_multiple_accounts(client, [
    "CkPEsmgfeCV4RcLHWA6jNaDWaGkVXT5Q2TTsysXyRk2B",
    "Tx4YJpozxG2U6R2PvszvW1872em7J8xMY59CgfhndFf"
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
