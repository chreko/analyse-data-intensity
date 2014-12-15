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

import data.O_NET.onet as onet
import numpy as np

def load_wa_dr():
    onet_data = onet.load_onet_data()
    wa = onet_data['Work Activities']
    #cmr = onet_data['Content Model Reference']
    #dwa = onet_data['DWA Reference']
    #iwa = onet_data['IWA Reference']
    #tasks = onet_data['Task Statements']
    #task_dwa = onet_data['Tasks to DWAs']
    #task_ratings = onet_data['Task Ratings']
    #occup = onet_data['Occupation Data']
    #pd.merge(cmr, dwa, on='Element ID')
    
    #-------------------------------------------------- Selection of data-related WA
    _selected_wa = ['4.A.2.a.2' # Processing Information
                   ,'4.A.2.a.4' # Analyzing Data or Information
                   ,'4.A.3.b.1' # Interacting With Computers
                   # Deselected initially since it includes a lot of misleading tasks (see analyse_iwa)
                   ,'4.A.1.a.1' # Getting Information
                   # only interested in DWAs 'Maintain operational records'.
                   #,'4.A.3.b.6' # Documenting/Recording Information 
                   # only interested in DWAs 'Monitor financial data or activities'
                   #,'4.A.1.a.2' # Monitor Processes, Materials, or Surroundings
                   # only interested in DWAs 'Determine operational methods or procedures'
                   #,'4.A.2.b.1' # Making Decisions and Solving Problems 
                   #,'4.A.2.b.2' # Thinking Creatively # only interested in 3 IWAs
                   # only interested in DWAs 'Collect environmental or biological samples.'
                   #,'4.A.3.a.2' # Handling and Moving Objectives
                   ]
    
    # Only select data-related WAs that are relevant and not recommended for suppress
    wa_dr = wa[wa['Element ID'].isin(_selected_wa) & (wa['Recommend Suppress'] != 'Y') 
               & (wa['Not Relevant'] != 'Y')]
    
    # Create wide format of data frames with IM and LV (using reindexing rather than pivoting)
    wa_dr = wa_dr.set_index(['O*NET-SOC Code', 'Element Name', 'Scale ID'])
    wa_dr = wa_dr.unstack('Scale ID')['Data Value']
    
    # Normalise IM and LV to be between 0 and 100 
    wa_dr.IM = wa_dr.IM.astype(float) / 5 * 100
    wa_dr.LV = wa_dr.LV.astype(float) / 7 * 100
    
    # Compute index which combines IM and LV according to geometric mean
    # Alternatively one could use cobb-douglas function as follow:
    # wa_dr['INDX'] = wa_dr.LV**(1/3.) * wa_dr.IM**(2/3.)
    wa_dr['INDX'] = np.sqrt(wa_dr.LV * wa_dr.IM)
    
    # Now we can focus on the index and have the wa as columns
    wa_dr = wa_dr.unstack().INDX
    
    # We could sort
    #wa_dr.sort('Analyzing Data or Information', ascending=False)
    
    #===============================================================================
    # Analysing data-related tools and technologies used by occupations
    #===============================================================================
    # Extract information on tools and technology used by occupations
    tt = onet_data['Tools and Technology']
    tt = tt.set_index('O*NET-SOC Code')#['Commodity Code']
    #wa_tt_dr = pd.merge(wa_dr, t_t, left_index=True, right_index=True)
    
    #------------------------------ Selection of data-related tools and technologies
    _tech_analysis = ['43232605' # Analytical or scientific software
                      # Other analytic tools which however are too specific
                      ,'43232303' # Customer relationship management CRM software
                      ,'43231604' # Financial analysis software
                      ,'43231511' # Expert system software
                      ,'43232110' # Spreadsheet software
                      ]
    _tech_db_ui = ['43232306' # Data base user interface and query software
                  ,'43232305' # Data base reporting software
                  ]
    _tech_db_admin =['43232304' # Data base management system software
                    ,'43232310' # Metadata management software
                    ,'43232311' # Object oriented data base management software
                    ]
    _tech_dev = ['43232402' # Development environment software
                ,'43232405' # Object or component oriented development software
                ]
    _tech_data_analytics = ['43232307' # Data mining software
                           ,'43232314' # Business intelligence and data analysis software
                           ]
    
    # Select onetsoc_code of occupations using analysis tools #352
    analysts = tt[tt['Commodity Code'].isin(_tech_analysis)]
    analysts = set(analysts.index.values)
    # Using db ui tools #565
    db_users = tt[tt['Commodity Code'].isin(_tech_db_ui)]
    db_users = set(db_users.index.values)
    # Using db management tools #30
    db_admins = tt[tt['Commodity Code'].isin(_tech_db_admin)]
    db_admins = set(db_admins.index.values)
    # ... doing software development #143
    developers = tt[tt['Commodity Code'].isin(_tech_dev)]
    developers = set(developers.index.values)
    # ... doing data analytics #32
    data_analysts = tt[tt['Commodity Code'].isin(_tech_data_analytics)]
    data_analysts = set(data_analysts.index.values)
    
    #----------------- Now we check occupations which use several of these tools
    # Here are some references:
    # Actuaries use: _tech_analysis, _tech_db_ui, _tech_db_admin
    # Astronomers use: _tech_dev, _tech_analysis, _tech_db_ui
    # Economists use: _tech_analysis, _tech_dev, _tech_db_ui
    # Financial analysts use: _tech_analysis, _tech_db_ui, 
    # Information Security Analysts use: _tech_dev, 
    
    # Using analytic tools together with development and db ui tools
    analysts_data_ui_dev = analysts.intersection(db_users).intersection(developers) #97
    # Using analytic tools together with db ui and db admin tools
    analysts_data_ui_db = analysts.intersection(db_users).intersection(db_admins) #26 subset of db_admins
    
    # Finally we define data-related occupations as the union of occupations using
    # data analytics OR db management tools OR the combination of 
    # analytic tools together with development and db ui tools
    data_occupations = db_admins.union(data_analysts).union(analysts_data_ui_dev)
    # And we define "data scientists"  as the intersection of these occupations
    data_scientists = analysts_data_ui_dev.intersection(db_admins).intersection(data_analysts)
    
    # Using data analytics and db management tools together developing tools
    data_scientists_dbu = data_analysts.intersection(db_users)   #31
    data_scientists_dev = data_analysts.intersection(developers) #18
    data_scientists_dbu_dev = data_scientists_dbu.intersection(developers) #17
    data_scientists_dba = data_analysts.intersection(db_admins)  #8 
    data_scientists_dba_dev = data_scientists_dba.intersection(developers) #6
    
    #--------------------------------- Now we combine the this data with that on WAs
    wa_dr['data_analytics'] = False
    wa_dr.data_analytics[wa_dr.index.isin(data_analysts)]=True
    wa_dr['db_admin'] = False
    wa_dr.db_admin[wa_dr.index.isin(db_admins)]=True
    wa_dr['advanced_data_analysis'] = False
    wa_dr.advanced_data_analysis[wa_dr.index.isin(analysts_data_ui_dev)]=True
    wa_dr['analysis'] = False
    wa_dr.analysis[wa_dr.index.isin(analysts)]=True
    
    return wa_dr

