analyse-data-intensity
======================
This project analyses the data intensity in OECD economies.
 
The final objective is to compute an indicator for the data-intensity of the 
economy (incl. by sector). Data intensity is defined as a share of either:
    1.) number of jobs in DrO vs. total number of jobs
    2.) weighted average wages of DrO vs. overall weighted average wages
    3.) the degree of importance, frequency, or relevance of data-related 
    working activities of all occupations.
    
Approach 2.) is the preferred one since it takes into account the fact that wages 
reflects demand for skills. For 1.) and 2.) we need to identify data-related
occupations (DrO), which are occupations where the collection, storage, 
processing, or analysis of data is at the core of the occupation's working 
activities.

How do we operationalise "is at the core of the occupation's working activities"? 
Or what are the requirements for occupations to be data-related? 

Here is the approach that is followed in this project:
I) Identify DrO, which are 
	1.) occupations for which data-related tasks are highly relevant, important,
	   and/or frequent.
	   i) The HumRRO report suggests that tasks are to be classified as "core" 
	   	  if (a) relevance > 67% and (b) a mean importance (IM) > 3.0 (60%);
	   ii) Alternatively, we can select those occupations for which IM and level 
	       (LV) is above the 67%-quantile. This reflects the notion of three 
	       level separation (Hi/Mi/Lo).
	   iii) This approach requires identifying data-related tasks and working
	   		activities.
	2.) occupations that use tools and technologies for data collection, 
	    storage, processing, or analysis;
	    i) This approach requires identifying data-related tools and technologies.
	3.) occupations which are among the ICT specialists or ICT advance users;
		i) This approach requires the list of ICT specialists and advance users
	4.) occupations which require certain types of skills and competences
		i) This approach requires the list of significant skills

II) Computer value-added (growth) by country (and industry) and regress on
	the measure of DrO.

III) Compute output (growth) by country (and industry) and regress on the 
	 measure of DrO. 
	 
The modules are free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

The modules are distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/gpl.txt>.

Copyright (C) 2014 Christian Reimsbach Kounatze
