# -*- coding: utf-8 -*-
# Copyright (C) 2017-2021 Greenbone Networks GmbH
#
# SPDX-License-Identifier: GPL-3.0-or-later
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import sys
import time
from argparse import Namespace
from gvm.protocols.gmp import Gmp

from gvmtools.helper import error_and_exit


def check_args(args):
    len_args = len(args.script) - 1
    if len_args != 1:
        message = """
        This script pulls hostnames from a text file and creates a target \
for each.
        One parameter after the script name is required.

        1. <hostname>        -- IP of the GVM host 
        2. <hosts_textfile>  -- text file containing hostnames

        Example:
            $ gvm-script --gmp-username name --gmp-password pass \
socket scripts/create_targets_from_host_list.py \
<hostname> <hosts_textfile>
        """
        print(message)
        sys.exit()


def load_host_list(host_file):
    try:
        with open(host_file, encoding='utf-8') as f:
            content = f.readlines()
        host_list = [x.strip() for x in content]
        host_list = list(filter(None, host_list))
    except IOError as e:
        error_and_exit(f"Failed to read host_file: {str(e)} (exit)")

    if len(host_list) == 0:
        error_and_exit("Host file is empty (exit)")

    return host_list


def send_command(gmp, host_list):

    name = f"Automatic_target_list_{time.strftime('%Y/%m/%d-%H:%M')}"
    comment = f"Created: {time.strftime('%Y/%m/%d-%H:%M')}"
    
    res = gmp.create_target(name=name, comment=comment, hosts=host_list, port_list_id="33d0cd82-57c6-11e1-8ed1-406186ea4fc5") #El port_list_id es obligatorio y es el de la IANA
    target_id = res.xpath('@id')[0] #Con esto saco el id del target para guardarlo despues
    print(target_id)

def main(gmp: Gmp, args: Namespace) -> None:
    # pylint: disable=undefined-variable

    check_args(args)

    hostfile = args.script[1]

    hostlist = load_host_list(hostfile)
    send_command(gmp, hostlist)

if __name__ == '__gmp__':
    main(gmp, args)