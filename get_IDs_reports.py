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


def send_command(gmp):    
    res = gmp.get_reports()
    #idReport = res.xpath('@id')[0] #Con esto saco el id del reporte para guardarlo despues
    print(res) # Me devuelve eso -> ['<Element get_reports_response at 0x7fb792f53ec0>'], pero no puedo cogerlo con el [0]. Puede ser que tenga que
    #el ID al lanzar la task

def main(gmp: Gmp, args: Namespace) -> None:
    # pylint: disable=undefined-variable

    send_command(gmp)

if __name__ == '__gmp__':
    main(gmp,args)