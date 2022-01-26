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
# https://terra-money.github.io/terra.py/guides/lcdclient.html#lcdclient-reference
# https://github.com/realkibou/Terra-One-Stop-Bot
# https://github.com/unl1k3ly/AnchorHODL
# https://github.com/AaronCQL/bluna-bot

# Terra SDK
from terra_sdk.client.lcd import LCDClient
from terra_sdk.core.numeric import Dec
from terra_sdk.core.coins import Coin
from terra_sdk.exceptions import LCDResponseError

from .utils.contact_addresses import contract_addresses
from src.chains.Terra.protocols.Nexus import Nexus
from src.chains.Terra.protocols.Glow import Glow
from src.chains.Terra.protocols.Astroport import Astroport
from src.chains.Terra.protocols.Valkyrie import Valkyrie
from src.chains.Terra.protocols.Apollo import Apollo

class Terra:
    def __init__(self, network='MAINNET', walletAddress='', walletMnemonic=''):
        if network == 'MAINNET':
            chain_id = 'columbus-5'
            public_node_url = 'https://lcd.terra.dev'
            # tx_look_up = f'https://finder.terra.money/{chain_id}/tx/'
            contact_addresses = contract_addresses.contact_addresses(network='MAINNET')
            rev_Contract_addresses = contract_addresses.rev_contact_addresses(contact_addresses)

        else:
            chain_id = 'bombay-12'
            public_node_url = 'https://bombay-lcd.terra.dev'
            # tx_look_up = f'https://finder.terra.money/{chain_id}/tx/'
            contact_addresses = contract_addresses.contact_addresses(network='bombay-12')
            rev_Contract_addresses = contract_addresses.rev_contact_addresses(contact_addresses)

        self.chain = 'Terra'

        self.wallet = LCDClient(
            chain_id=chain_id,
            url=public_node_url,
    #        gas_prices=terra_gas_prices['uusd']+"uusd",
            gas_adjustment=2
        )

        self.account_address = walletAddress

        # Contracts required
        self.Oracle = contact_addresses['TerraSwap_Router']

        # known contracts
        self.bLUNA_token = contact_addresses['bLUNA']
        self.aUST_token = contact_addresses['aUST']
        self.MIR_token = contact_addresses['MIR']
        self.SPEC_token = contact_addresses['SPEC']
        self.ANC_token = contact_addresses['ANC']
        self.PSI_token = contact_addresses['PSI']
        self.bPsiDP_token = contact_addresses['Pylon bPsiDP-24m Token']
        self.GLOW_token = contact_addresses['GLOW']
        self.LOOP_token = contact_addresses['LOOP']
        self.LOOPR_token = contact_addresses['LOOPR']
        self.ASTRO_token = contact_addresses['ASTRO']

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

        for symbol in ['bLUNA', 'aUST', 'ANC','MIR', 'SPEC', 'ANC', 'PSI', 'GLOW', 'LOOP', 'LOOPR', 'APOLLO', 'ASTRO']:
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

        wallet_balances['bPsiDP-24m'] = {
            "name": 'bPsiDP-24m',
            "symbol": 'bPsiDP-24m',
            "balance": self.get_non_native_balance(getattr(self, 'bPsiDP_token')), 
            "chain": self.chain,
            "price": self.get_token_token_rate(self.PSI_token, getattr(self, 'bPsiDP_token')) * self.get_token_rate(self.PSI_token),
            "decimals": 0
        }

        return wallet_balances

    def get_wallet_balances(self):
        wallet_balances = self.get_non_native()

        try:
            balance_native = self.wallet.bank.balance(address=self.account_address)
            for i in balance_native.to_data():
                s = i['denom']
                wallet_balances[s[1:]] = {
                    "name": s[1:].upper(),
                    "symbol": s[1:].upper(),
                    "balance": Dec(int(i['amount'])/1000000), 
                    "chain": self.chain,
                    "price": self.get_native_rate(i['denom']),
                    "decimals": 0
                }
        except LCDResponseError:
            print('Error reading native balance')

        return wallet_balances

    def get_protocols(self):
        protocols = {}

        protocols['Nexus Protocol'] = Nexus(client=self.wallet, walletAddress=self.account_address)
        protocols['Glow'] = Glow(client=self.wallet, walletAddress=self.account_address)
        protocols['Astroport'] = Astroport(client=self.wallet, walletAddress=self.account_address)
        protocols['Valkyrie'] = Valkyrie(client=self.wallet, walletAddress=self.account_address)
        protocols['Apollo'] = Apollo(client=self.wallet, walletAddress=self.account_address)

        return protocols
