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
# https://finder.extraterrestrial.money/mainnet/projects/apollo
# https://finder.extraterrestrial.money/mainnet/address/terra15cy5ef4e5mtxtjrjemkhlf2jjal7zmzug45vy8
# https://finder.extraterrestrial.money/mainnet/address/terra1g7jjjkt5uvkjeyhp8ecdz4e4hvtn83sud3tmh2
# https://github.com/ApolloFoundation

# TODO
# dinamicizzare pool

# Terra SDK
from ..utils.contact_addresses import contract_addresses
from terra_sdk.core.numeric import Dec

class Apollo:
    def __init__(self, client, walletAddress, network='MAINNET'):
        self.wallet = client
        self.account_address = walletAddress

        contact_addresses = contract_addresses.contact_addresses(network)

        self.protocol = 'Apollo DAO'

        # Contracts required
        self.Oracle = contact_addresses['TerraSwap_Router']

        # known contracts
        self.APOLLO_token = contact_addresses['APOLLO']
        self.MINE_token = contact_addresses['MINE']

        self.APOLLO_MINEUST_AutoCompounder = contact_addresses['Apollo MINE-UST AutoCompounder']

        self.TerraSwap_MINE_UST_Pair = contact_addresses['Terraswap Pylon MINE-UST Pair']

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

    def get_stable_pool_info(self, token_UST_pair_address:str):
        """ Retrieve info for a pool UST/<token>"""
        query = {
            "pool": {}
        }
        query_result = self.wallet.wasm.contract_query(token_UST_pair_address, query)

        UST_in_pool = sum(Dec(asset['amount']) for asset in query_result['assets'] if asset['info'].get('token') is None)
        token_in_pool = sum(Dec(asset['amount']) for asset in query_result['assets'] if asset['info'].get('token') is not None)
        total_share = Dec(query_result['total_share'])

        return [token_in_pool, UST_in_pool, total_share]

    def get_available_LP_token(self, token_farm_address:str):
        LP_token_available = 0

        query = {
            "user_info": {
                "address": self.account_address, 
            }
        }
        query_result = self.wallet.wasm.contract_query(token_farm_address, query)
        # {"base_token_balance": "37702", "shares": "27849"}

        if query_result != []:
            LP_token_available = query_result['base_token_balance']

        return Dec(int(LP_token_available)/1000000)

    def get_mineust_pool(self):
        all_rates = {}
        MINE_pool_info = self.get_stable_pool_info(self.TerraSwap_MINE_UST_Pair)

        all_rates['MINE'] = Dec(MINE_pool_info[1] / MINE_pool_info[0] * 1000000)

        all_rates['MINE-TOKEN-PER-SHARE'] = Dec(MINE_pool_info[0] / MINE_pool_info[2])
        all_rates['MINE-UST-PER-SHARE'] = Dec(MINE_pool_info[1] / MINE_pool_info[2])

        MINE_LP_balance = self.get_available_LP_token(self.APOLLO_MINEUST_AutoCompounder)
        MINE_token_rate = self.get_token_rate(self.MINE_token)

        MINE_balance = all_rates['MINE-TOKEN-PER-SHARE'] * MINE_LP_balance
        UST_balance = all_rates['MINE-UST-PER-SHARE'] * MINE_LP_balance
        value_of_MINE_LP_token = MINE_balance * MINE_token_rate + UST_balance

        return {
            "Pool": "MINE+UST",
            "Balances": f'{MINE_LP_balance} MINE-UST ({MINE_balance} MINE+{UST_balance} UST)',
            "Value": value_of_MINE_LP_token,
            "details": {
                "supply_token_list": [{
                    "name": "MINE",
                    "symbol": "MINE",
                    "balance": MINE_balance,
                    "price": MINE_token_rate,
                    "decimals": 0
                },{
                    "name": "UST",
                    "symbol": "UST",
                    "balance": UST_balance,
                    "price": 1.0,
                    "decimals": 0
                }]
            },
            "name": "Farm"
        }

    def get_cards(self):
        cards = {}

        # panel farm (contiene i titoli delle colonne)
        cards['Farm'] = {
            "name": "Farm",
            "rows": {}
        }
        ## row mineust
        cards['Farm']['rows']['MINE-UST'] = self.get_mineust_pool()

        # panel rewards (contiene i titoli delle colonne)
        cards['Rewards'] = {
            "name": "Rewards",
            "rows": {}
        }
        ## Community Farming - Phase 1
        ## Community Farming - Phase 2
        ## Vault Farming
        ## Luna Staker Airdrop

        # panel govern (contiene i titoli delle colonne)
        ## row apollo

        return cards
