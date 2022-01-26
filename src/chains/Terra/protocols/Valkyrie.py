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

# TODO
# Farm
# Stake

# refs:

# Terra SDK
from ..utils.contact_addresses import contract_addresses

from terra_sdk.core.numeric import Dec

import time

class Valkyrie:
    def __init__(self, client, walletAddress, network='MAINNET'):
        self.wallet = client
        self.account_address = walletAddress

        contact_addresses = contract_addresses.contact_addresses(network)

        self.protocol = 'Valkyrie'

        # Contracts required
        self.Oracle = contact_addresses['TerraSwap_Router']

        # known contracts
        self.VKR_token = contact_addresses['VKR']

        self.ValkyrieGovernance = contact_addresses['Valkyrie Governance']

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

    def get_gov_staked_VKR(self, token_farm_address:str):
        LP_token_available = 0

        query = {
            "staker_state": {
                "address": self.account_address
            }
        }
        query_result = self.wallet.wasm.contract_query(token_farm_address, query)
        # {'balance': '10338425', 'share': '5640288', 'votes': []}

        if query_result != []:
            LP_token_available = query_result['balance']

        return Dec(int(LP_token_available)/1000000)

    def get_vkr_vault(self):
        all_rates = {}
        VKR_balance = self.get_gov_staked_VKR(self.ValkyrieGovernance)

        VKR_token_rate = self.get_token_rate(self.VKR_token)

        rewards = 0 #self.get_claimable_PSI(self.NexusnLUNArewards)
        return {
            "Pool": "VKR",
            "Balances": f'{VKR_balance} VKR',
            "Rewards": rewards,
            "Value": VKR_balance * VKR_token_rate + rewards * VKR_token_rate,
            "details": {
                "supply_token_list": [{
                    "name": "ValkyrieProtocol VKR Token",
                    "symbol": "VKR",
                    "balance": VKR_balance,
                    "price": VKR_token_rate,
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
        cards['Farm']['rows']['VKR'] = self.get_vkr_vault()

        # panel govern (contiene i titoli delle colonne)
        ## row glow

        return cards
