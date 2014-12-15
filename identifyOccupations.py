#!/usr/bin/python
# -*- coding:utf-8 -*-
'''
This module identifies data-related occupations based on the analysis of 
data-related WAs as provided by O.Net.

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
import loadONET as onet

wa_dr = onet.load_wa_dr()
# ... to set w_mean threshold 
_high_threshold = 90
_middle_threshold = 79
_low_threshold = 66
#===============================================================================
# Select data-related occupations based on different criteria
#===============================================================================

# Select by occupation according to OECD definition of data specialists
def get_oecd_selector():
    selected_occ = ['15-2011.00', # Actuaries
                    '15-2021.00', # Mathematicians
                    '15-2031.00', # Operations research analysts
                    '15-2041.00', # Statisticians
                    '19-3022.00', # Survey researchers
                    '15-1141.00', # Database administrators
                    '15-1142.00', # Network and Computer Systems
                    '15-1143.00', # Computer Network Architects
                    '15-1199.00'] # Computer Occupations All Other
    return selected_occ

# Check occupations which do not use data-related tools or technologies ...
def get_nott_selector(wa_dr=wa_dr):
    selector = ((wa_dr.data_analytics == False) & 
                (wa_dr.db_admin == False) & 
                (wa_dr.advanced_data_analysis == False))
    return wa_dr[selector].index

# Occupations which use data analytics or data management tools
def get_tt_selector(wa_dr=wa_dr):
    selector = ((wa_dr.data_analytics == True) | (wa_dr.db_admin == True))
    return wa_dr[selector].index

def get_manager_selector(wa_dr=wa_dr):
    wa_dr['onetsoc_code'] = wa_dr.index #So we can do string operations
    return wa_dr.onetsoc_code.str.startswith('11-')

def get_data_occ(wa_dr=wa_dr, tt=False,  exclude_managers=True):
    selector = (# A minimum degree of using computers
                (wa_dr['Interacting With Computers'] >= _low_threshold) &
                (# Doing data analysis to a high degree
                 (wa_dr['Analyzing Data or Information'] >= _high_threshold)))
    if tt:
        selector = (selector | 
                    ((wa_dr['Interacting With Computers'] >= _low_threshold) &
                     # Or using data tools to a significant degree
                     ((wa_dr['Analyzing Data or Information'] >= _middle_threshold) &
                      (wa_dr.data_analytics == True) | (wa_dr.db_admin == True) | #&
                      (wa_dr.advanced_data_analysis == True))))
    if exclude_managers:
        selector = (selector & ~get_manager_selector(wa_dr))
    return wa_dr[selector]

def get_pot_data_occ(wa_dr=wa_dr, tt=False, exclude_managers=True):
    #===========================================================================
    # Identify occupations where data analytics have great potentials.
    # These are occupations where data-related WAs incl.
    # 1.) '4.A.2.a.2' # Processing Information
    # 2.) '4.A.2.a.4' # Analyzing Data or Information
    # 3.) '4.A.1.a.1' # Getting Information            
    # are high, but '4.A.3.b.1' # Interacting With Computers is very low.
    # These occupations uses analysis software incl. excel but not more.
    #===========================================================================
    selector = (# Below minimum degree of using computers
                (wa_dr['Interacting With Computers'] < _low_threshold) &
                # Doing data tasks to a significant degree
                ((wa_dr['Getting Information'] >= _middle_threshold) |
                 (wa_dr['Processing Information'] >= _middle_threshold) |
                 (wa_dr['Analyzing Data or Information'] >= _middle_threshold)
                 ))
    if tt:
        selector = (selector & # using analysis tools
                    (wa_dr.analysis == True))
    if exclude_managers:
        selector = (selector & ~get_manager_selector(wa_dr))
    return wa_dr[selector]
