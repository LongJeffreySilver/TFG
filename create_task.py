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
    if len_args != 2:
        message = """
        This script takes the id of a target and creates a task with it to be launched \

        One parameter after the script name is required.

        1. <target_id>        -- ID of the target (String)

        Example: gvm-script --gmp-username <user> --gmp-password <pass> socket /home/kali/Desktop/create_task.py <target_id>

        """
        print(message)
        sys.exit()

def send_command(gmp, idTargets,name):
    #name = f"Automatic task {time.strftime('%Y/%m/%d-%H:%M:%S')}"
    
    res = gmp.create_task(name=name,config_id="daba56c8-73ec-11df-a475-002264764cea" ,scanner_id="08b69003-5fc2-4037-a479-93b440211c73", target_id=idTargets)
    idTask = res.xpath('@id')[0] #Con esto saco el id de las task para guardarlo despues
    print(idTask)

def main(gmp: Gmp, args: Namespace) -> None:
    # pylint: disable=undefined-variable

    check_args(args)

    idTargets = args.script[1]
    name = args.script[2]
    send_command(gmp, idTargets,name)




if __name__ == '__gmp__':
    main(gmp, args)