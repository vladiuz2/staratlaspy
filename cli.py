import asyncio, json, httpx, prettytable
import asyncclick as click
from solana.publickey import PublicKey
from typing import Any, List, Tuple, Union
from .score import  getShipStakingAccount, getScoreVarsShipAccount, getScoreEscrowAuthAccount
from solana.rpc.async_api import AsyncClient
from . import fetch_multiple_accounts
from .score import ScoreVars, ShipStaking, ScoreStats
from .utils.semantic_time import time_breakdown_string

SOLANA_NODE_URL = 'https://api.mainnet-beta.solana.com'
NFTS_URL = 'https://api.staratlas.club/nfts?category=ship'
ASSET_PRICES_URL = 'https://api.staratlas.club/redis/asset-prices?symbols='

@click.group()
async def cli():
    """
    Main cli group
    """

@cli.command()
@click.option("--currency", "-c", show_default=True, default='ATLAS', type=click.Choice(['ATLAS', 'USDC']), help="Currency, either ATLAS or USDC")
@click.argument('wallet', nargs=1)
async def score_fleet(wallet, currency):
    """
    Get score fleet info
    """
    def get_price(data, sym, quote):
        markets = {d.get('quote_symbol'):d for d in data.get(sym,{}).get('data',[])}
        atlas_usdc = data.get(sym,{}).get("ATLAS/USDC",1)
        price =  markets.get(quote, {}).get('market_price',0)
        if not price:
            if quote == 'ATLAS':
                price = markets.get('USDC', {}).get('market_price',0) / atlas_usdc
            elif quote == 'USDC':
                price = markets.get('ATLAS', {}).get('market_price',0) * atlas_usdc
            if not price and sym == 'ATLAS':
                price = atlas_usdc
        return price
    playerKey = PublicKey(wallet)
    connection = AsyncClient(SOLANA_NODE_URL)
    async with httpx.AsyncClient() as client:
        r = await client.get(NFTS_URL)
        nfts = r.json()
        await client.aclose()
    async with httpx.AsyncClient() as client:
        r = await client.get(ASSET_PRICES_URL + 'ATLAS,AMMO,FUEL,FOOD,TOOL,'+\
                             ','.join([nft.get('symbol') for nft in nfts]))
        prices = r.json()
        await client.aclose()
    mints = [PublicKey(nft.get('mint')) for nft in nfts]
    staking = [getShipStakingAccount(playerKey, mint)[0] for mint in mints]
    escrow = [getScoreEscrowAuthAccount(playerKey, mint)[0] for mint in mints]
    vars = [getScoreVarsShipAccount(mint)[0] for mint in mints]
    staking_state = await fetch_multiple_accounts(connection, staking)
    vars_state = await fetch_multiple_accounts(connection, vars)
    await connection.close()
    pt = prettytable.PrettyTable()
    #pt.field_names = ['Ship', 'Qty', 'Value', 'Daily Rewards', 'Daily Burn', 'Net Yield', 'APR']
    pt.field_names = ['Ship', 'Qty', 'Daily Rewards', 'Daily Burn', 'Net Yield']
    pt.align['Ship'] = 'l'
    pt.align['Qty'] = 'r'
    pt.align['Value'] = 'r'
    pt.align['Daily Rewards'] = 'r'
    pt.align['Daily Burn'] = 'r'
    pt.align['Net Yield'] = 'r'
    pt.align['APR'] = 'r'
    tot_burn = 0
    tot_reward = 0
    for i in range(len(nfts)):
        if staking_state[i]:
            qty = staking_state[i].ship_quantity_in_escrow
            value = get_price(prices, nfts[i].get('symbol'), currency) * qty
            reward = (60 * 60 * 24 * vars_state[i].reward_rate_per_second * \
                 staking_state[i].ship_quantity_in_escrow) / 10 ** 8
            if currency == 'USDC':
                reward = reward * get_price(prices, 'ATLAS','USDC')
            stats = ScoreStats(vars_state[i], staking_state[i])
            burn = stats.arms_daily_burn_units * get_price(prices, 'AMMO', currency) + \
                   stats.food_daily_burn_units * get_price(prices, 'FOOD', currency) + \
                   stats.fuel_daily_burn_units * get_price(prices, 'FUEL', currency) + \
                   stats.toolkit_daily_burn_units * get_price(prices, 'TOOL', currency)
            net = reward - burn
            tot_burn += burn
            tot_reward += reward
            if value:
                apr = 100*net * 365 / value
            else:
                apr = 0
            pt.add_row([
                nfts[i].get('name'),
                '{:,.0f}'.format(qty),
                #'{:,.0f}'.format(value),
                '{:,.2f}'.format(reward),
                '{:,.2f}'.format(burn),
                '{:,.2f}'.format(net)
                #'{:,.1f} %'.format(apr)
            ])
    pt.add_row([
        'Total:',
        '',
        '{:,.2f}'.format(tot_reward),
        '{:,.2f}'.format(tot_burn),
        '{:,.2f}'.format(tot_reward-tot_burn)
        # '{:,.1f} %'.format(apr)
    ])
    tlines = str(pt).split('\n')  # convert table view to lines
    print('\n'.join(
        tlines[:(len(tlines) - 2)] + [tlines[len(tlines) - 1]] + tlines[-2:]))  # add a sub line to table and print



@cli.command()
@click.argument('wallet', nargs=1)
async def score_supplies(wallet):
    """
    Get score supplies state
    """
    playerKey = PublicKey(wallet)
    connection = AsyncClient(SOLANA_NODE_URL)
    async with httpx.AsyncClient() as client:
        r = await client.get(NFTS_URL)
        nfts = r.json()
        await client.aclose()
    mints = [PublicKey(nft.get('mint')) for nft in nfts]
    staking = [getShipStakingAccount(playerKey, mint)[0] for mint in mints]
    escrow = [getScoreEscrowAuthAccount(playerKey, mint)[0] for mint in mints]
    vars = [getScoreVarsShipAccount(mint)[0] for mint in mints]
    staking_state = await fetch_multiple_accounts(connection, staking)
    vars_state = await fetch_multiple_accounts(connection, vars)
    await connection.close()
    pt = prettytable.PrettyTable()
    pt.field_names = ['Ship', 'Qty', 'Fuel', 'Food', 'Ammo', 'Tool', 'Resupply in']
    pt.align['Ship'] = 'l'
    pt.align['Qty'] = 'r'
    pt.align['Fuel'] = 'r'
    pt.align['Food'] = 'r'
    pt.align['Ammo'] = 'r'
    pt.align['Tool'] = 'r'
    pt.align['Resupply in'] = 'l'
    for i in range(len(nfts)):
        if staking_state[i]:
            qty = staking_state[i].ship_quantity_in_escrow
            reward = (60 * 60 * 24 * vars_state[i].reward_rate_per_second * \
                 staking_state[i].ship_quantity_in_escrow) / 10 ** 8
            stats = ScoreStats(vars_state[i], staking_state[i])
            pt.add_row([
                nfts[i].get('name'),
                '{:,.0f}'.format(qty),
                '{:,.1f}%'.format(stats.fuel_current_supply_to_total_capacity_percent*100),
                '{:,.1f}%'.format(stats.food_current_supply_to_total_capacity_percent*100),
                '{:,.1f}%'.format(stats.arms_current_supply_to_total_capacity_percent*100),
                '{:,.1f}%'.format(stats.toolkit_current_supply_to_total_capacity_percent*100),
                time_breakdown_string(stats.seconds_remaining * 1000, 1 )
            ])
    print(pt)


if __name__ == '__main__':
    cli(_anyio_backend="asyncio")