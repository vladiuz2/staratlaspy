# staratlaspy

A library to interact with StarAtlas solana programs.

Based on [Kevin Heavey's AnchorPy](https://kevinheavey.github.io/anchorpy/) that made this
a very easy job.

> This code is not associated with Star Atlas, Automata LLC, or any of their companies.


# Usage


### Faction Accounts
Get a faction data account

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

# Author

* vlad@theclubguild.com

* Visit: https://theclubguild.com/

* [Discord](https://discord.gg/the-sa-club) | [Twitter](https://twitter.com/TheClubGuild)
| [Youtube](https://www.youtube.com/channel/UCMTp0p-oOsZB8UETrCr53XA?sub_confirmation=1)

# License

[Creative Commons Attribution-NonCommercial-NoDerivatives 4.0 International Public License](LICENSE.txt)
