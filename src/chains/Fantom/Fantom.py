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

from web3 import Web3

#from src.utils.contact_addresses import contract_addresses

class Fantom:
    def __init__(self, network='MAINNET', walletAddress='', walletMnemonic=''):
        if network == 'MAINNET':
            public_node_url = 'https://rpc.ftm.tools'
            # tx_look_up = f'https://finder.terra.money/{chain_id}/tx/'
 #           contact_addresses = contract_addresses.contact_addresses(network='MAINNET')
 #           rev_Contract_addresses = contract_addresses.rev_contact_addresses(contact_addresses)

        else:
            public_node_url = 'https://rpcapi.fantom.network'
            # tx_look_up = f'https://finder.terra.money/{chain_id}/tx/'
 #           contact_addresses = contract_addresses.contact_addresses(network='bombay-12')
 #           rev_Contract_addresses = contract_addresses.rev_contact_addresses(contact_addresses)

        self.chain = 'Fantom'

        #Web3.isAddress('walletAddress')
        self.wallet = Web3(Web3.HTTPProvider('https://rpc.ftm.tools'))
        #print(w3.isConnected())
        #print(w3.eth.get_block('latest'))

        self.account_address = walletAddress

        # Contracts required
        #self.Oracle = contact_addresses['TerraSwap_Router']

        # known contracts

    def get_native_balance(self, denom:str):
        balance_native = self.wallet.bank.balance(address=self.account_address).to_data()
        return sum(Dec(int(item['amount'])) for item in balance_native if item['denom'] == denom)

    def get_non_native_balance(self, token_address): 
        query = {
            "balance": {
                "address": self.account_address
            }
        }
        query_result = self.wallet.wasm.contract_query(token_address, query)

        return Dec(int(query_result['balance'])/1000000)

    def get_native_rate(self, denom:str):
        if denom == 'FTM':
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

        # if not found we have to use a router
        # i.e. https://github.com/astroport-fi/astroport-core/tree/master/contracts/router

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

    def get_non_native(self):
        wallet_balances = {}

        for symbol in ['CMDX']:
            if hasattr(self, f'{symbol}_token') == False:
                continue

            wallet_balances[symbol] = {
                "name": symbol,
                "symbol": symbol,
                "balance": self.get_non_native_balance(getattr(self, f'{symbol}_token')), 
                "chain": self.chain,
                "price": self.get_token_rate(getattr(self, f'{symbol}_token')),
                "decimals": 0
            }

#        wallet_balances['bPsiDP-24m'] = {
#            "name": 'bPsiDP-24m',
#            "symbol": 'bPsiDP-24m',
#            "balance": self.get_non_native_balance(getattr(self, 'bPsiDP_token')), 
#            "chain": self.chain,
#            "price": self.get_token_token_rate(self.PSI_token, getattr(self, 'bPsiDP_token')) * self.get_token_rate(self.PSI_token),
#            "decimals": 0
#        }

        print(wallet_balances)
        return wallet_balances

    def get_wallet_balances(self):
        wallet_balances = {}
        #self.get_non_native()

        balance_native = self.wallet.eth.get_balance(account=self.account_address)
        if balance_native > 0:
            wallet_balances["FTM"] = {
                "name": "FTM",
                "symbol": "FTM",
                "balance": int(balance_native), 
                "chain": self.chain,
                "price": self.get_native_rate("FTM"),
                "decimals": 18
            }

        return wallet_balances

    def get_protocols(self):
        protocols = {}

        return protocols
