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

from jinja2 import Template

def getTitleTemplate():
    dataCard = '''{{ "POOL" }}
{%- for space in range(18 - "POOL"|length) -%}
{{ " " }}
{%- endfor -%}
{{ "BALANCES" }}
{%- for space in range(35 - "BALANCES"|length) -%}
{{ " " }}
{%- endfor -%}
{{ "REWARDS" }}
{%- for space in range(18 - "REWARDS"|length) -%}
{{ " " }}
{%- endfor -%}
{{ "$VALUE"}}
{%- for space in range(8 - "$VALUE"|length) -%}
{{ " " }}
{%- endfor -%}
'''

    return Template(dataCard)

def get_card_template():
    dataCard = '''
{%- set ns = namespace(pool='', balances='',rewards='',value=0) -%}
{%- for token in card['details']['supply_token_list']  -%}
{% set ns.pool = ns.pool + token.symbol|e %}
{%- if not loop.last -%}{% set ns.pool = ns.pool + '+' %}{%- endif -%}
{%- endfor -%}
{{ ns.pool }}
{%- for space in range(18 - ns.pool|length) -%}
{{ " " }}
{%- endfor -%}
{%- for token in card['details']['supply_token_list']  -%}
{%- set ns.balances = ns.balances + '%0.3f' % token.balance | float + ' ' + token.symbol -%} 
{%- if not loop.last -%}{% set ns.balances = ns.balances + ' ' %}{%- endif -%}
{%- endfor -%}
{{ ns.balances}}
{%- for space in range(35 - ns.balances|length) -%}
{{ " " }}
{%- endfor -%}
{%- for token in card['details']['reward_token_list']  -%}
{%- set ns.rewards = ns.rewards + '%0.3f' % token.balance | float + ' ' + token.symbol -%}
{%- if not loop.last -%}{% set ns.rewards = ns.rewards + ' ' %}{%- endif -%}
{%- endfor -%}
{{ ns.rewards }}
{%- for space in range(18 - ns.rewards|length) -%}
{{ " " }}
{%- endfor -%}
{%- for token in card['details']['supply_token_list'] -%}
{%- set ns.value = ns.value + token.balance*token.price -%}
{%- endfor -%}
{%- for token in card['details']['reward_token_list'] -%}
{%- set ns.value = ns.value + token.balance*token.price -%}
{%- endfor -%}
${{ '%0.3f' % ns.value | float }}'''

    return Template(dataCard)

def print_protocol(protocol):
    print(f'=== {protocol.chain} ===')

    print(f'=== Wallet ===')
    print(f'%10s %8s %25s %15s %25s' % ('ASSETS', '', 'BALANCES', 'PRICE', 'VALUE'))
    for key, coin in protocol.get_wallet_balances().items():
        value = coin["balance"].__float__() * coin["price"].__float__()
        if value < 0.001:
            # hide small balances (dust)
            continue

        print(f'%10s %8s %25.9f %15.3f %25.3f' % (
            coin["name"], 
            '........', 
            coin["balance"].__float__()/10**coin['decimals'], 
            coin["price"].__float__(),
            value/10**coin['decimals']
        ))
    print('')

    tt = getTitleTemplate()
    tm = get_card_template()
    for p_key, protocol in protocol.get_protocols().items():
        print(f'=== {p_key} ===')

        cards = protocol.get_cards()
        for c_key, card in cards.items():
            print(f'=== {c_key} ===')
            msg = tt.render(card=card)
            print(msg)

            for c_key, row in card['rows'].items():
                if not row['details']:
                    continue

                msg = tm.render(card=row)
                print(msg)
            print('')
