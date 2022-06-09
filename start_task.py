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
        Launching the task according to the ID passed as a parameter \

        One parameter after the script name is required.

        1. <task_id>        -- ID of the task (String)

        Example: gvm-script --gmp-username <user> --gmp-password <pass> socket /home/kali/Desktop/start_task.py <task_id>

        """
        print(message)
        sys.exit()

def send_command(gmp, idTask):    
    res = gmp.start_task(idTask)
    idReport = res[0].text
    print(idReport)

def main(gmp: Gmp, args: Namespace) -> None:
    # pylint: disable=undefined-variable

    check_args(args)

    idTask = args.script[1]

    send_command(gmp, idTask)

if __name__ == '__gmp__':
    main(gmp, args)