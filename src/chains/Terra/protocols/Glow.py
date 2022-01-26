#    This program is free software; you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation; either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program; if not, write to the Free Software
#    Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA

# refs:
# https://github.com/glow-protocol/glow-contracts
# https://finder.terra.money/mainnet/address/terra13zx49nk8wjavedjzu8xkk95r3t0ta43c9ptul7
# https://finder.terra.money/mainnet/address/terra1le3a67j4khkjhyytkllxre60dvywm43ztq2s8t
# https://docs.glowyield.com/glow-yield/smart-contracts/deployed-contracts

# TODO
# Farm/Stake Rewards

# Terra SDK
from ..utils.contact_addresses import contract_addresses

from terra_sdk.core.numeric import Dec

import time

class Glow:
    def __init__(self, client, walletAddress, network='MAINNET'):
        self.wallet = client
        self.account_address = walletAddress

        contact_addresses = contract_addresses.contact_addresses(network)

        self.protocol = 'Glow'

        # Contracts required
        self.Oracle = contact_addresses['TerraSwap_Router']

        # known contracts
        self.GLOW_token = contact_addresses['GLOW']

        self.GLOW_GLOW_UST_Farm = contact_addresses['Glow Staking']
        self.GLOW_GLOW_UST_Pair = contact_addresses['Glow GLOW-UST Pair']
        self.GLOW_GLOW_UST_LP = contact_addresses['Glow GLOW-UST LP']

    def get_token_rate(self, token_address='terra...'):
        query = {
            "simulate_swap_operations" : {
                "offer_amount": "1000000",
                "operations": [{
                    "terra_swap": {
                      "offer_asset_info": {
                        "native_token": {
                          "denom": "uusd"
                        }
                      },
                      "ask_asset_info": {
                        "token": {
                          "contract_addr": token_address
                        }
                      }
                    }
                }]
            }
        }
        query_result = self.wallet.wasm.contract_query(self.Oracle, query)

        return Dec(1000000/int(query_result['amount']))

    def get_pool_info(self, token_UST_pair_address:str):

        query = {
            "pool": {}
        }
        query_result = self.wallet.wasm.contract_query(token_UST_pair_address, query)

        UST_in_pool = sum(Dec(asset['amount']) for asset in query_result['assets'] if asset['info'].get('token') is None)
        token_in_pool = sum(Dec(asset['amount']) for asset in query_result['assets'] if asset['info'].get('token') is not None)
        total_share = Dec(query_result['total_share'])

        return [token_in_pool, UST_in_pool, total_share]

    def get_available_LP_token_for_withdrawal(self, token_farm_address:str, token_address:str):
        LP_token_available = 0

        query = {
            "staker_info": {
                "staker": self.account_address, 
            }
        }
        query_result = self.wallet.wasm.contract_query(token_farm_address, query)
        # {'staker': 'terra***', 'reward_index': '0.010145480163178208', 'bond_amount': '17420000', 'pending_reward': '0'}

        if query_result != []:
            LP_token_available = query_result['bond_amount']

        return Dec(int(LP_token_available)/1000000)

    def get_pool_claimable_GLOW(self, token_farm_address:str):
        LP_token_available = 0

        return Dec(int(LP_token_available)/1000000)

    def get_glow_pool(self):
        all_rates = {}
        GLOW_pool_info = self.get_pool_info(self.GLOW_GLOW_UST_Pair)

        all_rates['GLOW'] = Dec(GLOW_pool_info[1] / GLOW_pool_info[0] * 1000000)

        all_rates['GLOW-TOKEN-PER-SHARE'] = Dec(GLOW_pool_info[0] / GLOW_pool_info[2])
        all_rates['GLOW-UST-PER-SHARE'] = Dec(GLOW_pool_info[1] / GLOW_pool_info[2])

        GLOW_LP_balance = self.get_available_LP_token_for_withdrawal(self.GLOW_GLOW_UST_Farm, self.GLOW_GLOW_UST_LP)
        GLOW_token_rate = self.get_token_rate(self.GLOW_token)

        GLOW_balance = all_rates['GLOW-TOKEN-PER-SHARE'] * GLOW_LP_balance
        UST_balance = all_rates['GLOW-UST-PER-SHARE'] * GLOW_LP_balance
        value_of_GLOW_LP_token = GLOW_balance * GLOW_token_rate + UST_balance

        rewards = self.get_pool_claimable_GLOW(self.GLOW_GLOW_UST_Farm)
        return {
            "Pool": "GLOW+UST",
            "Balances": f'{GLOW_LP_balance} GLOW-UST ({GLOW_balance} GLOW+{UST_balance} UST)',
            "Rewards": rewards,
            "Value": value_of_GLOW_LP_token + rewards * GLOW_token_rate,
            "details": {
                "supply_token_list": [{
                    "name": "GLOW",
                    "symbol": "GLOW",
                    "balance": GLOW_balance,
                    "price": GLOW_token_rate,
                    "decimals": 0
                }, {
                    "name": "UST",
                    "symbol": "UST",
                    "balance": UST_balance,
                    "price": 1.00,
                    "decimals": 0
                }],
                "reward_token_list": [{
                    "name": "GLOW",
                    "symbol": "GLOW",
                    "balance": rewards,
                    "price": GLOW_token_rate,
                    "decimals": 0
                }]
            },
            "name": "Farm"
        }

    def get_cards(self):
        cards = {}

        # panel farm (contiene i titoli delle colonne)
        cards['Farm'] = {
            "rows": {}
        }
        ## row glow+ust
        cards['Farm']['rows']['GLOW+UST'] = self.get_glow_pool()

        # panel govern (contiene i titoli delle colonne)
        ## row glow

        return cards
