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
# https://docs.anchorprotocol.com/protocol/money-market

# TODO
# Savings
# Borrow
# Bond
# Govern
# bLUNA rewards

# Terra SDK
from ..utils.contact_addresses import contract_addresses
from terra_sdk.core.numeric import Dec

class Anchor:
    def __init__(self, client, walletAddress, network='MAINNET'):
        self.wallet = client
        self.account_address = walletAddress

        contact_addresses = contract_addresses.contact_addresses(network)

        self.protocol = 'Anchor'

        # Contracts required
        self.Oracle = contact_addresses['TerraSwap_Router']

        # known contracts
        self.aUST_token = contact_addresses['aUST']

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

    def get_cards(self):
        cards = {}

        # panel savings (contiene i titoli delle colonne)
        cards['Savings'] = {
            "rows": {}
        }
        ## row aUST
        cards['Savings']['rows']['APOLLO'] = self.get_earn_balance()

        # panel govern (contiene i titoli delle colonne)

        return cards
