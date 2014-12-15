#!/usr/bin/python
# -*- coding:utf-8 -*-
'''
This module loads the most recent ONET data as Pandas data frame into the 
memory.

This module is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/gpl.txt>.

Created on 14 May 2014
@author: Christian Reimsbach-Kounatze
@contact: chreko@gmx.net
@copyright: Copyright (C) 2014 Christian Reimsbach Kounatze
@license: GPLv3
'''
import pandas as pd
import os

def load_onet_data():
    db_folder = os.path.dirname(os.path.realpath(__file__))
    onet_data = {}
    for root, subdirs, files in os.walk(db_folder):
        for f in files:
            if f.find('.txt') != -1:
                n = f.replace('.txt', '')
                path = os.path.join(root, f)
                df = pd.io.parsers.read_table(path, dtype=unicode)
                onet_data.update({n: df})
    return onet_data
