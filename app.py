#!/usr/bin/env python

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

# Wallet Tracker

import config as config

from src.chains import Terra
from src.chains import Osmosis
from src.chains import Fantom

from src.view import console

if __name__ == "__main__":
    print('Wallet Tracker')
    print('')

    if config and config.terra:
        t = Terra(network=config.NETWORK, walletAddress=config.terra['walletAddress'])
        console.print_protocol(t)

    if config and config.osmosis:
        o = Osmosis(network=config.NETWORK, walletAddress=config.osmosis['walletAddress'])
        console.print_protocol(o)

    if config and config.fantom:
        f = Fantom(network=config.NETWORK, walletAddress=config.fantom['walletAddress'])
        console.print_protocol(f)
