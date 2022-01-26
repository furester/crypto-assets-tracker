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
# https://github.com/astroport-fi/astroport-changelog/blob/master/columbus-5/1.0.0/core_columbus-5.json
# https://finder.terra.money/mainnet/address/terra1zgrx9jjqrfye8swykfgmd6hpde60j0nszzupp9
# https://github.com/astroport-fi/astroport-core
# https://docs.astroport.fi/astroport/smart-contracts/astroport-contract-addresses

# TODO
# dinamicizzare pool

# Terra SDK
from ..utils.contact_addresses import contract_addresses

from terra_sdk.core.numeric import Dec
from terra_sdk.core.coins import Coin
from terra_sdk.exceptions import LCDResponseError

class Astroport:
    def __init__(self, client, walletAddress, network='MAINNET'):
        self.wallet = client
        self.account_address = walletAddress

        contact_addresses = contract_addresses.contact_addresses(network)

        self.protocol = 'Astroport'

        # Contracts required
        self.Oracle = contact_addresses['TerraSwap_Router']

        # known contracts
        self.ASTRO_token = contact_addresses['ASTRO']
        self.Psi_token = contact_addresses['PSI']
        self.bLUNA_token = contact_addresses['bLUNA']

        self.ASTRO_Astroport_Generator = contact_addresses['Astroport Generator']
        self.ASTRO_Astroport_Lockdrop = contact_addresses['Astroport Lockdrop']
        self.ASTRO_Astroport_Auction = contact_addresses['Astroport Auction']

        self.ASTRO_ASTRO_UST_Pair = contact_addresses['Astroport ASTRO-UST Pool']
        self.ASTRO_ASTRO_UST_LP = contact_addresses['Astroport ASTRO-UST LP']

        self.ASTRO_Psi_UST_Pair = contact_addresses['Astroport Psi-UST Pool']
        self.ASTRO_Psi_UST_LP = contact_addresses['Astroport Psi-UST LP']
        self.Nexus_Psi_UST_LP = contact_addresses['Nexus Psi-UST LP']

        self.ASTRO_bLUNA_LUNA_Pair = contact_addresses['Astroport bLUNA-LUNA Pool']
        self.ASTRO_bLUNA_LUNA_LP = contact_addresses['Astroport bLUNA-LUNA LP']
        self.TerraSwap_bLUNA_LUNA_LP = contact_addresses['terraswapblunaLunaLPToken']


    def get_native_rate(self, denom:str):
        if denom == 'uusd':
            return 1
        
        coin = self.wallet.market.swap_rate(Coin(denom, 1000000), 'uusd')
        return Dec(int(coin.amount)/1000000)

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
        # {'assets': [{'info': {'token': {'contract_addr': 'terra14tl83xcwqjy0ken9peu4pjjuu755lrry2uy25r'}}, 'amount': '104307'}, {'info': {'native_token': {'denom': 'uluna'}}, 'amount': '38076'}], 'total_share': '56568'}
        #print(query_result)

        UST_in_pool = sum(Dec(asset['amount']) for asset in query_result['assets'] if asset['info'].get('token') is None)
        token_in_pool = sum(Dec(asset['amount']) for asset in query_result['assets'] if asset['info'].get('token') is not None)
        total_share = Dec(query_result['total_share'])

        return [token_in_pool, UST_in_pool, total_share]

    def get_available_LP_token_for_withdrawal(self, token_farm_address:str, token_address:str):
        """ Retrieve LP balance associated with address """
        LP_token_available = 0

        query = {
          "lock_up_info":{
            "user_address":self.account_address,
            "terraswap_lp_token": token_address,
            "duration": 52
          }
        }
        #print(query)
        query_result = self.wallet.wasm.contract_query(token_farm_address, query)
        #print(query_result)
        # {'balance': '0'}

        if query_result != []:
            LP_token_available = query_result['lp_units_locked']

        return Dec(int(LP_token_available)/1000000)

    def get_phase1_available_LP_token_for_withdrawal(self, token_farm_address:str, token_address:str, duration:int):
        """ Retrieve LP balance associated with address """
        LP_token_available = 0

        query = {
          "lock_up_info":{
            "user_address":self.account_address,
            "terraswap_lp_token": token_address,
            "duration": duration
          }
        }
        #print(query)
        query_result = self.wallet.wasm.contract_query(token_farm_address, query)
        #print(query_result)
        # {'terraswap_lp_token': 'terra1q6r8hfdl203htfvpsmyh8x689lp2g0m7856fwd', 'lp_units_locked': '113274913', 'withdrawal_flag': False, 'astro_rewards': '16587477', 'duration': 52, 'generator_astro_debt': '0', 'claimable_generator_astro_debt': '0', 'generator_proxy_debt': '0', 'claimable_generator_proxy_debt': '0', 'unlock_timestamp': 1671519600, 'astroport_lp_units': '124146667', 'astroport_lp_token': 'terra1cspx9menzglmn7xt3tcn8v8lg6gu9r50d7lnve', 'astroport_lp_transferred': None}

        if query_result != []:
            LP_token_available = query_result['astroport_lp_units']

        return Dec(int(LP_token_available)/1000000)

    def get_phase1_claimable_ASTRO(self, token_farm_address:str, token_address:str, duration:int):
        """ Retrieve LP balance associated with address """
        ASTRO_token_available = 0

        query = {
          "lock_up_info":{
            "user_address":self.account_address,
            "terraswap_lp_token": token_address,
            "duration": duration
          }
        }
        #print(query)
        query_result = self.wallet.wasm.contract_query(token_farm_address, query)
        #print(query_result)
        # {'terraswap_lp_token': 'terra1q6r8hfdl203htfvpsmyh8x689lp2g0m7856fwd', 'lp_units_locked': '113274913', 'withdrawal_flag': False, 'astro_rewards': '16587477', 'duration': 52, 'generator_astro_debt': '0', 'claimable_generator_astro_debt': '0', 'generator_proxy_debt': '0', 'claimable_generator_proxy_debt': '0', 'unlock_timestamp': 1671519600, 'astroport_lp_units': '124146667', 'astroport_lp_token': 'terra1cspx9menzglmn7xt3tcn8v8lg6gu9r50d7lnve', 'astroport_lp_transferred': None}

        if query_result != []:
            # https://discord.com/channels/886922190489002004/886922190853918734/933208961874800691
            # 7.    Look for “"claimable_generator_astro_debt". Divide by 1,000,000 and that’s your accumulated $Astro for your Astro-UST LP or your particular migrated and locked terraswap LP.
            ASTRO_token_available = query_result['claimable_generator_astro_debt']

        return Dec(int(ASTRO_token_available)/1000000)

    def get_phase2_available_LP_token_for_withdrawal(self, token_farm_address:str, token_address:str):
        """ Retrieve LP balance associated with address """
        LP_token_available = 0

        query = {
          "user_info":{
            "address":self.account_address,
            "terraswap_lp_token": token_address
          }
        }
        
        query_result = self.wallet.wasm.contract_query(token_farm_address, query)
        # {'astro_delegated': '100000000', 'ust_delegated': '20000000', 'ust_withdrawn': False, 'lp_shares': '88274437', 'claimed_lp_shares': '0', 'withdrawable_lp_shares': '20535317', 'auction_incentive_amount': '16121126', 'astro_incentive_transferred': True, 'claimable_generator_astro': '831346', 'generator_astro_debt': '0', 'user_gen_astro_per_share': '0'}

        if query_result != []:
            LP_token_available = query_result['lp_shares']

        return Dec(int(LP_token_available)/1000000)

    def get_phase2_claimable_ASTRO(self, token_farm_address:str, token_address:str):
        """ Retrieve ASTRO rewards balance associated with address """
        ASTRO_token_available = 0

        query = {
          "user_info":{
            "address":self.account_address,
            "terraswap_lp_token": token_address
          }
        }
        #print(query)
        query_result = self.wallet.wasm.contract_query(token_farm_address, query)
        #print(query_result)
        # {'astro_delegated': '100000000', 'ust_delegated': '20000000', 'ust_withdrawn': False, 'lp_shares': '88274437', 'claimed_lp_shares': '0', 'withdrawable_lp_shares': '20535317', 'auction_incentive_amount': '16121126', 'astro_incentive_transferred': True, 'claimable_generator_astro': '831346', 'generator_astro_debt': '0', 'user_gen_astro_per_share': '0'}

        if query_result != []:
            ASTRO_token_available = query_result['claimable_generator_astro']

        return Dec(int(ASTRO_token_available)/1000000)

    def get_lp_balance(self, reward_generator_address:str, token_address:str):
        """ Retrieve LP balance associated with address """
        LP_token_available = 0

        query = {
          "deposit":{
            "user":self.account_address,
            "lp_token": token_address
          }
        }
        #print(query)
        query_result = self.wallet.wasm.contract_query(reward_generator_address, query)
        print(query_result)
        # {'balance': '0'}

        if query_result != []:
            LP_token_available = query_result['lp_units_locked']

        return Dec(int(LP_token_available)/1000000)


    def get_astroust_pool(self):
        all_rates = {}
        ASTRO_pool_info = self.get_pool_info(self.ASTRO_ASTRO_UST_Pair)

        all_rates['ASTRO'] = Dec(ASTRO_pool_info[1] / ASTRO_pool_info[0] * 1000000)

        all_rates['ASTRO-TOKEN-PER-SHARE'] = Dec(ASTRO_pool_info[0] / ASTRO_pool_info[2])
        all_rates['ASTRO-UST-PER-SHARE'] = Dec(ASTRO_pool_info[1] / ASTRO_pool_info[2])

        ASTRO_LP_balance = self.get_phase2_available_LP_token_for_withdrawal(self.ASTRO_Astroport_Auction, self.ASTRO_ASTRO_UST_LP)
        ASTRO_token_rate = self.get_token_rate(self.ASTRO_token)

        ASTRO_balance = all_rates['ASTRO-TOKEN-PER-SHARE'] * ASTRO_LP_balance
        UST_balance = all_rates['ASTRO-UST-PER-SHARE'] * ASTRO_LP_balance
        value_of_ASTRO_LP_token = ASTRO_balance * ASTRO_token_rate + UST_balance

        rewards = self.get_phase2_claimable_ASTRO(self.ASTRO_Astroport_Auction, self.ASTRO_ASTRO_UST_LP)
        return {
            "Pool": "ASTRO+UST",
            "Balances": f'{ASTRO_LP_balance} ASTRO-UST ({ASTRO_balance} ASTRO+{UST_balance} UST)',
            "Rewards": rewards * ASTRO_token_rate,
            "Value": value_of_ASTRO_LP_token + rewards * ASTRO_token_rate,
            "details": {
                "supply_token_list": [{
                    "name": "ASTRO",
                    "symbol": "ASTRO",
                    "balance": ASTRO_balance,
                    "price": ASTRO_token_rate,
                    "decimals": 0
                }, {
                    "name": "UST",
                    "symbol": "UST",
                    "balance": UST_balance,
                    "price": 1.00,
                    "decimals": 0
                }],
                "reward_token_list": [{
                    "name": "ASTRO",
                    "symbol": "ASTRO",
                    "balance": rewards,
                    "price": ASTRO_token_rate,
                    "decimals": 0
                }]
            },
            "name": "Liquidity Provider"
        }

    def get_psiust_pool(self):
        all_rates = {}
        Psi_pool_info = self.get_pool_info(self.ASTRO_Psi_UST_Pair)

        all_rates['Psi'] = Dec(Psi_pool_info[1] / Psi_pool_info[0] * 1000000)

        all_rates['Psi-TOKEN-PER-SHARE'] = Dec(Psi_pool_info[0] / Psi_pool_info[2])
        all_rates['Psi-UST-PER-SHARE'] = Dec(Psi_pool_info[1] / Psi_pool_info[2])

        Psi_LP_balance = self.get_phase1_available_LP_token_for_withdrawal(self.ASTRO_Astroport_Lockdrop, self.Nexus_Psi_UST_LP, duration=52)
        Psi_token_rate = self.get_token_rate(self.Psi_token)
        ASTRO_token_rate = self.get_token_rate(self.ASTRO_token)

        Psi_balance = all_rates['Psi-TOKEN-PER-SHARE'] * Psi_LP_balance
        UST_balance = all_rates['Psi-UST-PER-SHARE'] * Psi_LP_balance
        value_of_Psi_LP_token = Psi_balance * Psi_token_rate + UST_balance

        rewards = self.get_phase1_claimable_ASTRO(self.ASTRO_Astroport_Lockdrop, self.Nexus_Psi_UST_LP, duration=52)
        return {
            "Pool": "Psi+UST",
            "Balances": f'{Psi_LP_balance} Psi-UST ({Psi_balance} Psi+{UST_balance} UST)',
            "Rewards": rewards * ASTRO_token_rate,
            "Value": value_of_Psi_LP_token + rewards * ASTRO_token_rate,
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
                    "name": "ASTRO",
                    "symbol": "ASTRO",
                    "balance": rewards,
                    "price": ASTRO_token_rate,
                    "decimals": 0
                }]
            },
            "name": "Lockdrop"
        }

    def get_blunaluna_pool(self, duration:int):
        all_rates = {}
        bLUNA_pool_info = self.get_pool_info(self.ASTRO_bLUNA_LUNA_Pair)

        all_rates['bLUNA'] = Dec(bLUNA_pool_info[1] / bLUNA_pool_info[0] * 1000000)

        all_rates['bLUNA-TOKEN-PER-SHARE'] = Dec(bLUNA_pool_info[0] / bLUNA_pool_info[2])
        all_rates['bLUNA-LUNA-PER-SHARE'] = Dec(bLUNA_pool_info[1] / bLUNA_pool_info[2])

        bLUNA_LP_balance = self.get_phase1_available_LP_token_for_withdrawal(self.ASTRO_Astroport_Lockdrop, self.TerraSwap_bLUNA_LUNA_LP, duration)
        
        bLUNA_token_rate = self.get_token_rate(self.bLUNA_token)
        LUNA_token_rate = self.get_native_rate ('uluna')
        ASTRO_token_rate = self.get_token_rate(self.ASTRO_token)

        bLUNA_balance = all_rates['bLUNA-TOKEN-PER-SHARE'] * bLUNA_LP_balance
        LUNA_balance = all_rates['bLUNA-LUNA-PER-SHARE'] * bLUNA_LP_balance
        value_of_bLUNA_LP_token = bLUNA_balance * bLUNA_token_rate + LUNA_balance * LUNA_token_rate

        rewards = self.get_phase1_claimable_ASTRO(self.ASTRO_Astroport_Lockdrop, self.TerraSwap_bLUNA_LUNA_LP, duration)
        return {
            "Pool": f"bLUNA+LUNA {duration}",
            "Balances": f'{bLUNA_LP_balance} bLUNA-LUNA ({bLUNA_balance} bLUNA+{LUNA_balance} LUNA)',
            "Rewards": rewards * ASTRO_token_rate,
            "Value": value_of_bLUNA_LP_token + rewards * ASTRO_token_rate,
            "details": {
                "supply_token_list": [{
                    "name": "bLUNA",
                    "symbol": "bLUNA",
                    "balance": bLUNA_balance,
                    "price": bLUNA_token_rate,
                    "decimals": 0
                }, {
                    "name": "LUNA",
                    "symbol": "LUNA",
                    "balance": LUNA_balance,
                    "price": LUNA_token_rate,
                    "decimals": 0
                }],
                "reward_token_list": [{
                    "name": "ASTRO",
                    "symbol": "ASTRO",
                    "balance": rewards,
                    "price": ASTRO_token_rate,
                    "decimals": 0
                }]
            },
            "name": "Lockdrop"
        }

    def get_cards(self):
        cards = {}

        # panel farm (contiene i titoli delle colonne)
        cards['Farm'] = {
            "rows": {}
        }
        ## row astro+ust
        cards['Farm']['rows']['ASTRO+UST'] = self.get_astroust_pool()
        ## row psi+ust
        try:
            cards['Farm']['rows']['Psi+UST'] = self.get_psiust_pool()
        except LCDResponseError:
            # unused pool for provided wallet
            pass

        for d in [2, 10, 52]:
            try:
                cards['Farm']['rows'][f'bLUNA+LUNA {d}'] = self.get_blunaluna_pool(d)
            except LCDResponseError:
                # unused pool for provided wallet
                pass


        # panel govern (contiene i titoli delle colonne)
        ## row astro

        return cards
