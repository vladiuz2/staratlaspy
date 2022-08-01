from solana.publickey import PublicKey
from .program_id import PROGRAM_ID
from .accounts import ScoreVars, ShipStaking
from ..utils.semantic_time import time_breakdown_string

import  time, math
# next line to be removed
import prettytable, json

def getScoreVarsShipAccount(shipMint: PublicKey, programId: PublicKey = PROGRAM_ID):
    """
    Returns the public key and bump seed for the SCORE variables ship account associated with the provided ship mint.

    :param shipMint: Mint address for the desired ship
    :param programId: Deployed program ID for the SCORE program
    :return: [Escrow account public key, bump seed]
    """
    return PublicKey.find_program_address(
        [b'SCOREVARS_SHIP', bytes(shipMint)],
        PROGRAM_ID)

def getScoreEscrowAuthAccount(playerPublicKey: PublicKey, shipMint: PublicKey, programId: PublicKey = PROGRAM_ID):
    """
     Returns the SCORE escrow authority account

    :param playerPublicKey: Player's public key
    :param shipMint: Mint address for the desired ship
    :param programId: Deployed program ID for the SCORE program
    :return: [Authority account public key, bump seed]
    """
    return PublicKey.find_program_address(
        [b'SCORE_ESCROW_AUTHORITY', bytes(playerPublicKey), bytes(shipMint)],
        PROGRAM_ID)

def getShipStakingAccount(playerPublicKey:PublicKey, assetMint:PublicKey, programId: PublicKey = PROGRAM_ID):
    """
    Returns a user's ship staking account

    :param playerPublicKey: Player's public key
    :param assetMint: Mint address for the desired resource
    :param programId: Deployed program ID for the SCORE program
    :return: [Staking account public key, bump seed]
    """
    return PublicKey.find_program_address(
        [b'SCORE_INFO', bytes(playerPublicKey), bytes(assetMint)],
        PROGRAM_ID)

class ScoreStats():
    json_attrs = []
    def _set_j_attr_(self, name, val):
        if not name in self.json_attrs:
            self.json_attrs.append(name)
        self.__setattr__(name, val)
    def __init__(self, vars: ScoreVars, staking: ShipStaking):
        self.vars = vars
        self.staking = staking
        self._set_j_attr_('seconds_since_last_action',
                          time.time() - staking.current_capacity_timestamp)
        rm = {
            'food':'food',
            'fuel':'fuel',
            'arms':'arms',
            'toolkit':'health'
        }
        # calc basic metrics
        for r in rm.keys():
            self._set_j_attr_(f'{r}_total_capacity_units',
                             staking.ship_quantity_in_escrow *
                             vars.__getattribute__(f'{r}_max_reserve')
                             )
            self._set_j_attr_(f'{r}_total_capacity_seconds',
                             vars.__getattribute__(f'{r}_max_reserve') *
                              vars.__getattribute__(f'milliseconds_to_burn_one_{r}') / 1000
            )
            self._set_j_attr_(f'{r}_daily_burn_units',
                             round(staking.ship_quantity_in_escrow * 24 * 60 * 60 * 1000 /
                             vars.__getattribute__(f'milliseconds_to_burn_one_{r}'))
                             )
        # calculate minimums
        self._set_j_attr_('min_capacity_seconds', min(*[
            staking.__getattribute__(f'{rm[r]}_current_capacity') for r in rm.keys()
        ]))
        self._set_j_attr_('min_total_capacity_seconds', min(*[
            self.__getattribute__(f'{r}_total_capacity_seconds') for r in rm.keys()
        ]))
        self._set_j_attr_('min_capacity_seconds_human',
                          time_breakdown_string(self.min_capacity_seconds*1000,2)
                          )
        self._set_j_attr_('seconds_inactive',
                          max(0,
                              self.seconds_since_last_action - self.min_capacity_seconds
                              ))
        self._set_j_attr_('seconds_inactive_human',
                          time_breakdown_string(self.seconds_inactive*1000,2)
                          )
        for r in rm.keys():
            self._set_j_attr_(f'{r}_remaining_seconds',
                               max(
                                   0,
                                   staking.__getattribute__(f'{rm[r]}_current_capacity') -
                                   (self.seconds_since_last_action - self.seconds_inactive)
                               ))
            self._set_j_attr_(f'{r}_remaining_seconds_human',
                              time_breakdown_string(self.__getattribute__(f'{r}_remaining_seconds') * 1000, 2)
                              )
            self._set_j_attr_(f'{r}_remaining_percent',
                              max(0, 100 * self.__getattribute__(f'{r}_remaining_seconds') /
                                  self.__getattribute__(f'{r}_total_capacity_seconds')
                                  ))
            self._set_j_attr_(f'{r}_remaining_units',
                              round(self.__getattribute__(f'{r}_remaining_percent') *
                              self.__getattribute__(f'{r}_total_capacity_units') / 100)
                              )
            self._set_j_attr_(f'{r}_full_supply_deficit_units',
                              self.__getattribute__(f'{r}_total_capacity_units') -
                              self.__getattribute__(f'{r}_remaining_units')
            )
            self._set_j_attr_(f'{r}_optimal_supply_deficit_seconds',
                              max(0, self.min_total_capacity_seconds -
                                  self.__getattribute__(f'{r}_remaining_seconds')))
            self._set_j_attr_(f'{r}_optimal_supply_deficit_seconds_human',
                              time_breakdown_string(self.__getattribute__(f'{r}_optimal_supply_deficit_seconds') * 1000, 2)
                              )
            self._set_j_attr_(f'{r}_optimal_supply_deficit_units',
                              math.floor(self.__getattribute__(f'{r}_total_capacity_units') *
                                         self.__getattribute__(f'{r}_optimal_supply_deficit_seconds') /
                                      self.__getattribute__(f'{r}_total_capacity_seconds')))

    def limited_atlas_resupply(self,
                               atlas: float,
                               fuel_price: float = 0.00144336,
                               food_price: float = 0.0006144,
                               arms_price: float = 0.00215039,
                               toolkit_price: float = 0.0017408) -> list:
        prices = {'food': food_price, 'fuel': fuel_price, 'arms': arms_price, 'toolkit': toolkit_price}
        deficits = sorted(list(set([self.__getattribute__(f'{r}_optimal_supply_deficit_seconds')
            for r in prices.keys()])), reverse=True)
        f = lambda x: deficits[x - len(deficits) + 1:] if x < len(deficits) - 1 else []
        queue = [
            {'resources': [k for k in prices.keys()
                           if self.__getattribute__(f'{k}_optimal_supply_deficit_seconds')>=deficits[i]
                           and self.__getattribute__(f'{k}_optimal_supply_deficit_seconds') > 0],
             'consumption_limit_seconds': deficits[i] - max(f(i) + [0]),
             'consumption_limit_human': time_breakdown_string((deficits[i] - max(f(i) + [0]))*1000, 2),
             }
            for i in range(len(deficits)) if deficits[i] > 0
        ]
        for i in range(len(queue)):
            queue[i]['atlas_per_second'] = sum([
                self.staking.__getattribute__(f'ship_quantity_in_escrow') * prices[r] /
                (self.vars.__getattribute__(f'milliseconds_to_burn_one_{r}') / 1000)
                for r in queue[i]['resources']
            ])
            queue[i]['atlas_limit'] = queue[i]['atlas_per_second'] * queue[i]['consumption_limit_seconds']
        atlas_remaining = atlas
        consumed_resources = {}
        for step in queue:
            if not atlas_remaining:
                break
            consumed_atlas = min([step.get('consumption_limit_seconds', 0) * step.get('atlas_per_second'),
                                  atlas_remaining
                                  ])
            if not consumed_atlas:
                break
            consumed_seconds = consumed_atlas / step.get('atlas_per_second')
            atlas_remaining = atlas_remaining - consumed_atlas
            for r in step.get('resources'):
                consumed_resources[r] = consumed_resources.get(r,0) + \
                                        consumed_seconds * \
                                        self.staking.__getattribute__(f'ship_quantity_in_escrow') / \
                                        (self.vars.__getattribute__(f'milliseconds_to_burn_one_{r}') / 1000)
        for r in prices.keys():
            if not consumed_resources.get(r):
                consumed_resources[r] = 0
        return {
            r: math.floor(consumed_resources[r])
            for r in prices.keys()
        }

    def to_json(self):
        return {
            k:self.__getattribute__(k)
            for k in sorted(self.json_attrs)
        }
