from solana.publickey import PublicKey
from .program_id import PROGRAM_ID
from .accounts import ScoreVars, ShipStaking
from ..utils.semantic_time import time_breakdown_string

import  time, math

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
            self._set_j_attr_(f'{r}_optimal_supply_deficit_units',
                              max(0, math.floor(self.__getattribute__(f'{r}_total_capacity_units') * (
                                  self.min_total_capacity_seconds -
                                  self.__getattribute__(f'{r}_remaining_seconds')) /
                                      self.min_total_capacity_seconds)))
        """
        self.fuel_current_supply_to_total_capacity_percent = max(0, (staking.fuel_current_capacity -
                                                              self.seconds_since_last_action) / \
                                                             self.fuel_total_capacity_seconds)
        self.fuel_needed_for_full_supply = staking.ship_quantity_in_escrow * \
                                           max(0, (1 - self.fuel_current_supply_to_total_capacity_percent) *
                                               self.fuel_total_capacity_seconds) / \
                                           (vars.milliseconds_to_burn_one_fuel/1000)
        self.fuel_current_supply = self.fuel_total_capacity - self.fuel_needed_for_full_supply
        self.fuel_needed_for_optimal_supply = max(0, round(staking.ship_quantity_in_escrow * min_total_capacity_seconds / \
                                                  (vars.milliseconds_to_burn_one_fuel / 1000) -
                                                  self.fuel_current_supply))
        # arms
        self.arms_daily_burn = round(staking.ship_quantity_in_escrow * 24 * 60 * 60 * 1000 /
                                   vars.milliseconds_to_burn_one_arms)
        self.arms_total_capacity = round(staking.ship_quantity_in_escrow * self.arms_total_capacity_seconds /
                                       (vars.milliseconds_to_burn_one_arms / 1000))
        #self.arms_current_supply_to_total_capacity_percent = max(0, (staking.arms_current_capacity -
        #                                                      self.seconds_since_last_action) / \
        #                                                     self.arms_total_capacity_seconds)
        self.arms_current_supply_to_total_capacity_percent = max(0, (staking.arms_current_capacity -
                                                              self.seconds_since_last_action) / \
                                                             self.arms_total_capacity_seconds)
        self.arms_needed_for_full_supply = staking.ship_quantity_in_escrow * \
                                           max(0, (1 - self.arms_current_supply_to_total_capacity_percent) *
                                               self.arms_total_capacity_seconds) / \
                                           (vars.milliseconds_to_burn_one_arms / 1000)
        self.arms_current_supply = self.arms_total_capacity - self.arms_needed_for_full_supply
        self.arms_needed_for_optimal_supply = max(0, round(staking.ship_quantity_in_escrow * min_total_capacity_seconds / \
                                                         (vars.milliseconds_to_burn_one_arms / 1000) -
                                                         self.arms_current_supply))
        # food
        self.food_daily_burn = round(staking.ship_quantity_in_escrow * 24 * 60 * 60 * 1000 /
                                   vars.milliseconds_to_burn_one_food)
        self.food_current_supply_to_total_capacity_percent = max(0, (staking.food_current_capacity -
                                                              self.seconds_since_last_action) / \
                                                             self.food_total_capacity_seconds)
        self.food_needed_for_full_supply = staking.ship_quantity_in_escrow * \
                                           max(0, (1 - self.food_current_supply_to_total_capacity_percent) *
                                               self.food_total_capacity_seconds) / \
                                           (vars.milliseconds_to_burn_one_food / 1000)
        self.food_current_supply = self.food_total_capacity - self.food_needed_for_full_supply
        self.food_needed_for_optimal_supply = max(0, round(staking.ship_quantity_in_escrow * min_total_capacity_seconds / \
                                                         (vars.milliseconds_to_burn_one_food / 1000) -
                                                         self.food_current_supply))
        # toolkit
        self.toolkit_daily_burn = round(staking.ship_quantity_in_escrow * 24 * 60 * 60 * 1000 /
                                      vars.milliseconds_to_burn_one_toolkit)
        self.toolkit_current_supply_to_total_capacity_percent = max(0, (staking.health_current_capacity -
                                                                 self.seconds_since_last_action) / \
                                                                self.toolkit_total_capacity_seconds)
        self.toolkit_needed_for_full_supply = staking.ship_quantity_in_escrow * \
                                              max(0, (1 - self.toolkit_current_supply_to_total_capacity_percent) *
                                                  self.toolkit_total_capacity_seconds) / \
                                              (vars.milliseconds_to_burn_one_toolkit / 1000)
        self.toolkit_current_supply = self.toolkit_total_capacity - self.toolkit_needed_for_full_supply
        self.toolkit_needed_for_optimal_supply = max(0,
                                                     round(staking.ship_quantity_in_escrow * min_total_capacity_seconds / \
                                                         (vars.milliseconds_to_burn_one_toolkit / 1000) -
                                                         self.toolkit_current_supply))
        """
    def limited_atlas_resupply(self,
                               atlas: float,
                               fuel_price: float = 0.00144336,
                               food_price: float = 0.0006144,
                               arms_price: float = 0.00215039,
                               toolkit_price: int = 0.0017408) -> list[4]:
        resources = {
            "food": {
                "seconds_to_optimal_supply": self.food_needed_for_optimal_supply * (
                        self.vars.milliseconds_to_burn_one_food / 1000) / self.staking.ship_quantity_in_escrow,
                "atlas_per_second": self.staking.ship_quantity_in_escrow * food_price / (
                        self.vars.milliseconds_to_burn_one_food / 1000),
                "milliseconds_to_burn_one":self.vars.milliseconds_to_burn_one_food
            },
            "fuel": {
                "seconds_to_optimal_supply": self.fuel_needed_for_optimal_supply * (
                        self.vars.milliseconds_to_burn_one_fuel / 1000) / self.staking.ship_quantity_in_escrow,
                "atlas_per_second": self.staking.ship_quantity_in_escrow * fuel_price / (
                        self.vars.milliseconds_to_burn_one_fuel / 1000),
                "milliseconds_to_burn_one":self.vars.milliseconds_to_burn_one_fuel
            },
            "arms": {
                "seconds_to_optimal_supply": self.arms_needed_for_optimal_supply * (
                        self.vars.milliseconds_to_burn_one_arms / 1000) / self.staking.ship_quantity_in_escrow,
                "atlas_per_second": self.staking.ship_quantity_in_escrow * arms_price / (
                        self.vars.milliseconds_to_burn_one_arms / 1000),
                "milliseconds_to_burn_one":self.vars.milliseconds_to_burn_one_arms
            },
            "toolkit": {
                "seconds_to_optimal_supply": self.toolkit_needed_for_optimal_supply * (
                        self.vars.milliseconds_to_burn_one_toolkit / 1000) / self.staking.ship_quantity_in_escrow,
                "atlas_per_second": self.staking.ship_quantity_in_escrow * toolkit_price / (
                        self.vars.milliseconds_to_burn_one_toolkit / 1000),
                "milliseconds_to_burn_one":self.vars.milliseconds_to_burn_one_toolkit
            }
        }

        def get_depleted_resources():
            return [k for k in resources.keys() if not resources[k].get('seconds_to_optimal_supply', 0) > 0]

        def get_atlas_per_second():
            return sum(
                [resources[k]['atlas_per_second'] for k in resources.keys() if k not in get_depleted_resources()])

        def update_consumed_seconds(secs=0):
            for k in resources.keys():
                if k not in get_depleted_resources():
                    resources[k]["seconds_to_optimal_supply"] -= secs
                    resources[k]["seconds_consumed"] = resources[k].get('seconds_consumed', 0) + secs

        atlas_remaining = atlas
        atlas_consumed = None
        for m in sorted([{**{"key": k}, **resources[k]} for k in resources.keys() if k not in get_depleted_resources()],
                        key=lambda x: x.get('seconds_to_optimal_supply')):
            if not get_atlas_per_second() > 0 or atlas_consumed == 0:
                break
            seconds_consumed = max(0, min(atlas_remaining / get_atlas_per_second(),
                                          resources[m.get('key')]['seconds_to_optimal_supply']))
            if not seconds_consumed > 0:
                break
            atlas_consumed = seconds_consumed * get_atlas_per_second()
            atlas_remaining = atlas_remaining - atlas_consumed
            update_consumed_seconds(seconds_consumed)
        return{ k:math.floor(resources[k].get('seconds_consumed',0)/\
                  (resources[k].get('milliseconds_to_burn_one')/1000)) for k in resources}

    def to_json(self):
        return {
            k:self.__getattribute__(k)
            for k in sorted(self.json_attrs)
        }
