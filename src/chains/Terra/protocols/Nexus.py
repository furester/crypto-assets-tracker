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
# https://github.com/Nexus-Protocol/basset-vault-contracts/tree/master/contracts
# https://docs.nexusprotocol.app/launch/smart-contracts/deployed-contracts
# https://github.com/Nexus-Protocol/contracts_scripts/blob/master/UPLOADED_CONTRACTS_MAINNET.md

# Terra SDK
from ..utils.contact_addresses import contract_addresses
from terra_sdk.core.numeric import Dec

import time

class Nexus:
    def __init__(self, client, walletAddress, network='MAINNET'):
        self.wallet = client
        self.account_address = walletAddress

        contact_addresses = contract_addresses.contact_addresses(network)

        self.protocol = 'Nexus Protocol'

        # Contracts required
        self.Oracle = contact_addresses['TerraSwap_Router']

        # known contracts
        self.PSI_token = contact_addresses['PSI']
        self.NLUNA_token = contact_addresses['nLUNA']

        self.Nexus_PSI_UST_Pair = contact_addresses['Nexus Psi-UST Pair']
        self.Nexus_PSI_UST_LP = contact_addresses['Nexus Psi-UST LP']
        self.Nexus_PSI_UST_Farm = contact_addresses['Nexus Psi-UST Staking']

        self.Nexus_NLUNA_PSI_Pair = contact_addresses['Nexus nLuna+Psi Pair']
        self.Nexus_NLUNA_PSI_LP = contact_addresses['Nexus nLuna+Psi LP']
        self.Nexus_NLUNA_PSI_Farm = contact_addresses['Nexus nLuna+Psi Staking']
        
        self.Airdrop_ANC = contact_addresses['Nexus Psi for ANC stakers']

        self.NexusnLUNArewards = contact_addresses['NexusnLUNArewards']
        self.NexusnGovernance = contact_addresses['Nexus Governance']

    def get_non_native_balance(self, token_address): 
        query = {
            "balance": {
                "address": self.account_address
            }
        }
        query_result = self.wallet.wasm.contract_query(token_address, query)

        return Dec(int(query_result['balance'])/1000000)

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

    def get_token_token_rate(self, from_token_address='terra...', to_token_address='terra...'):
        query = {
            "simulate_swap_operations" : {
                "offer_amount": "1000000",
                "operations": [{
                    "terra_swap": {
                      "offer_asset_info": {
                        "token": {
                          "contract_addr": from_token_address
                        }
                      },
                      "ask_asset_info": {
                        "token": {
                          "contract_addr": to_token_address
                        }
                      }
                    }
                }]
            }
        }
        query_result = self.wallet.wasm.contract_query(self.Oracle, query)

        return Dec(1000000/int(query_result['amount']))

    def get_pool_info(self, token_UST_pair_address:str):
        """ Retrieve info for a pool <token>/<token>"""
        query = {
            "pool": {}
        }
        query_result = self.wallet.wasm.contract_query(token_UST_pair_address, query)

        UST_in_pool = sum(Dec(asset['amount']) for asset in query_result['assets'] if asset['info'].get('token').get('contract_addr') == self.NLUNA_token)
        token_in_pool = sum(Dec(asset['amount']) for asset in query_result['assets'] if asset['info'].get('token').get('contract_addr') == self.PSI_token)
        total_share = Dec(query_result['total_share'])

        return [token_in_pool, UST_in_pool, total_share]

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

    def get_available_LP_token_for_withdrawal(self, token_farm_address:str, token_address:str):
        LP_token_available = 0

        query = {
            "staker_info": {
                "staker": self.account_address, 
            }
        }
        query_result = self.wallet.wasm.contract_query(token_farm_address, query)
        # {'staker': 'terra***', 'reward_index': '1.67128319565732584', 'bond_amount': '161766585', 'pending_reward': '0'}

        if query_result != []:
            LP_token_available = query_result['bond_amount']

        return Dec(int(LP_token_available)/1000000)

    def get_psi_pool(self):
        all_rates = {}
        PSI_pool_info = self.get_stable_pool_info(self.Nexus_PSI_UST_Pair)

        all_rates['PSI'] = Dec(PSI_pool_info[1] / PSI_pool_info[0] * 1000000)

        all_rates['PSI-TOKEN-PER-SHARE'] = Dec(PSI_pool_info[0] / PSI_pool_info[2])
        all_rates['PSI-UST-PER-SHARE'] = Dec(PSI_pool_info[1] / PSI_pool_info[2])

        Psi_LP_balance = self.get_available_LP_token_for_withdrawal(self.Nexus_PSI_UST_Farm, self.Nexus_PSI_UST_LP)
        Psi_token_rate = self.get_token_rate(self.PSI_token)

        Psi_balance = all_rates['PSI-TOKEN-PER-SHARE'] * Psi_LP_balance
        UST_balance = all_rates['PSI-UST-PER-SHARE'] * Psi_LP_balance
        value_of_Psi_LP_token = Psi_balance * Psi_token_rate + UST_balance

        rewards = self.get_pool_claimable_PSI(self.Nexus_PSI_UST_Farm)
        return {
            "Pool": "Psi+UST",
            "Balances": f'{Psi_LP_balance} PSI-UST ({Psi_balance} Psi+{UST_balance} UST)',
            "Rewards": rewards,
            "Value": value_of_Psi_LP_token + rewards * Psi_token_rate,
            "details": {
                "supply_token_list": [{
                    "name": "Nexus Psi Token",
                    "symbol": "Psi",
                    "balance": Psi_balance,
                    "price": Psi_token_rate,
                    "decimals": 0
                }, {
                    "name": "UST",
                    "symbol": "UST",
                    "balance": UST_balance,
                    "price": 1.00,
                    "decimals": 0
                }],
                "reward_token_list": [{
                    "name": "Nexus Psi Token",
                    "symbol": "Psi",
                    "balance": rewards,
                    "price": Psi_token_rate,
                    "decimals": 0
                }]
            },
            "name": "Farm",
            "stats": {
                "asset_name": "Nexus Psi-UST LP",
                "asset_symbol": "uLP",
                "asset_balance": Psi_LP_balance,
                "decimals": 0,
                "asset_usd_value": value_of_Psi_LP_token
            }
        }

    def get_nluna_pool(self):
        all_rates = {}
        PSI_pool_info = self.get_pool_info(self.Nexus_NLUNA_PSI_Pair)

        all_rates['PSI'] = Dec(PSI_pool_info[1] / PSI_pool_info[0] * 1000000)

        all_rates['PSI-TOKEN-PER-SHARE'] = Dec(PSI_pool_info[0] / PSI_pool_info[2])
        all_rates['PSI-NLUNA-PER-SHARE'] = Dec(PSI_pool_info[1] / PSI_pool_info[2])

        Psi_LP_balance = self.get_available_LP_token_for_withdrawal(self.Nexus_NLUNA_PSI_Farm, self.Nexus_NLUNA_PSI_LP)

        nLuna_token_rate = self.get_token_token_rate(self.PSI_token, self.NLUNA_token)
        Psi_token_rate = self.get_token_rate(self.PSI_token)

        Psi_balance = all_rates['PSI-TOKEN-PER-SHARE'] * Psi_LP_balance
        nLuna_balance = all_rates['PSI-NLUNA-PER-SHARE'] * Psi_LP_balance
        value_of_Psi_LP_token = Psi_balance * Psi_token_rate + (nLuna_balance * nLuna_token_rate) * Psi_token_rate

        rewards = self.get_pool_claimable_PSI(self.Nexus_NLUNA_PSI_Farm)
        return {
            "Pool": "nLuna+Psi",
            "Balances": f'{Psi_LP_balance} NLUNA+PSI ({nLuna_balance} nLuna+{Psi_balance} Psi)',
            "Rewards": rewards,
            "Value": value_of_Psi_LP_token + rewards * Psi_token_rate,
            "details": {
                "supply_token_list": [{
                    "name": "Nexus Psi Token",
                    "symbol": "Psi",
                    "balance": Psi_balance,
                    "price": Psi_token_rate,
                    "decimals": 0
                }, {
                    "name": "Nexus nLuna",
                    "symbol": "nLuna",
                    "balance": nLuna_balance,
                    "price": nLuna_token_rate * Psi_token_rate,
                    "decimals": 0
                }],
                "reward_token_list": [{
                    "name": "Nexus Psi Token",
                    "symbol": "Psi",
                    "balance": rewards,
                    "price": Psi_token_rate,
                    "decimals": 0
                }]
            },
            "name": "Farm",
            "stats": {
                "asset_name": "Nexus nLuna-Psi LP",
                "asset_symbol": "uLP",
                "asset_balance": Psi_LP_balance,
                "decimals": 0,
                "asset_usd_value": value_of_Psi_LP_token
            }            
        }

    def get_nluna_vault(self):
        all_rates = {}
        nLuna_balance = self.get_non_native_balance(self.NLUNA_token)

        nLuna_token_rate = self.get_token_token_rate(self.PSI_token, self.NLUNA_token)
        Psi_token_rate = self.get_token_rate(self.PSI_token)

        rewards = self.get_claimable_PSI(self.NexusnLUNArewards)
        return {
            "Pool": "nLuna",
            "Balances": f'{nLuna_balance} nLuna',
            "Rewards": rewards,
            "Value": (nLuna_balance * nLuna_token_rate) * Psi_token_rate + rewards * Psi_token_rate,
            "details": {
                "supply_token_list": [{
                    "name": "Nexus nLuna",
                    "symbol": "nLuna",
                    "balance": nLuna_balance,
                    "price": nLuna_token_rate * Psi_token_rate,
                    "decimals": 0
                }],
                "reward_token_list": [{
                    "name": "Nexus Psi Token",
                    "symbol": "Psi",
                    "balance": rewards,
                    "price": Psi_token_rate,
                    "decimals": 0
                }]
            },
            "name": "Staked"
        }

    def get_psi_gov(self):
        Psi_balance = self.get_gov_staked_PSI(self.NexusnGovernance)

        Psi_token_rate = self.get_token_rate(self.PSI_token)
        value_of_Psi_LP_token = Psi_balance * Psi_token_rate

        return {
            "Pool": "Psi",
            "Balances": f'{Psi_balance} Psi',
            "Value": value_of_Psi_LP_token,
            "details": {
                "supply_token_list": [{
                    "name": "Nexus Psi Token",
                    "symbol": "Psi",
                    "balance": Psi_balance,
                    "price": Psi_token_rate,
                    "decimals": 0
                }]
            },
            "name": "Govern"
        }

    def get_psi_airdrop_to_anc_staker(self):
        # get stage
        stage = self.get_airdrop_stage(self.Airdrop_ANC)

        # get is_claimed
        is_claimed = self.get_airdrop_isclaimed(self.Airdrop_ANC, stage)

        if is_claimed:
            return {
                "details": {}
            }

        # no smart contract query to get airdrop amount

        return {
            "Pool": "Nexus Psi Airdrop for ANC Gov stakers",
            "details": {}
        }

    def get_airdrop_stage(self, nexus_airdrop_address:str):
        latest_stage = 0

        query = {
          "latest_stage": {}
        }
        query_result = self.wallet.wasm.contract_query(nexus_airdrop_address, query)

        if query_result != []:
            latest_stage = query_result['latest_stage']

        return int(latest_stage)

    def get_airdrop_isclaimed(self, nexus_airdrop_address:str, stage:int):
        is_claimed = False

        query = {
          "is_claimed": {
            "stage": stage,
            "address": self.account_address
          }
        }
        query_result = self.wallet.wasm.contract_query(nexus_airdrop_address, query)

        if query_result != []:
            is_claimed = query_result['is_claimed']

        return bool(is_claimed)

    def get_pool_claimable_PSI(self, token_farm_address:str):
        LP_token_available = 0

        query = {
            "staker_info": {
                "staker": self.account_address,
                "time_seconds":int(time.time())
            }
        }
        query_result = self.wallet.wasm.contract_query(token_farm_address, query)
        # {'staker': 'terra***', 'reward_index': '1.67128319565732584', 'bond_amount': '161766585', 'pending_reward': '0'}

        if query_result != []:
            LP_token_available = query_result['pending_reward']

        return Dec(int(LP_token_available)/1000000)

    def get_claimable_PSI(self, contract_address:str):
        """ https://lcd.terra.dev/wasm/contracts/terra12kzewegufqprmzl20nhsuwjjq6xu8t8ppzt30a/store?query_msg=%7B%22staker_info%22:%7B%22staker%22:%22terra1f9l4xpcek8w649ccjjk97jacc4xwgf8cvdf63l%22,%22time_seconds%22:1642418062%7D%7D """
        claimable = 0

        query = {
            "accrued_rewards":
                {
                    "address": self.account_address
                }
        }

        query_result = self.wallet.wasm.contract_query(contract_address, query)

        # Sum up all claimable rewards for this account_address
        claimable = query_result['rewards']

        return Dec(int(claimable)/1000000)

    def get_gov_staked_PSI(self, token_farm_address:str):
        LP_token_available = 0

        query = {
            "staker": {
                "address": self.account_address
            }
        }
        query_result = self.wallet.wasm.contract_query(token_farm_address, query)
        # {'balance': '1525170283', 'share': '1499855152', 'locked_balance': []}

        if query_result != []:
            LP_token_available = query_result['balance']

        return Dec(int(LP_token_available)/1000000)

    def get_cards(self):
        cards = {}

        # panel farm
        cards['Farm'] = {
            "rows": {}
        }
        ## row psi+ust
        cards['Farm']['rows']['Psi+UST'] = self.get_psi_pool()
        ## row nluna+psi
        cards['Farm']['rows']['nLuna+Psi'] = self.get_nluna_pool()

        # panel vault
        cards['Vault'] = {
            "rows": {}
        }
        ## row nluna
        cards['Vault']['rows']['nLuna'] = self.get_nluna_vault()

        # panel govern
        cards['Govern'] = {
            "rows": {}
        }
        ## row psi
        cards['Govern']['rows']['Psi'] = self.get_psi_gov()

        # panel govern
        cards['Airdrop'] = {
            "rows": {}
        }
        ## row psi
        cards['Airdrop']['rows']['Psi'] = self.get_psi_airdrop_to_anc_staker()

        return cards
