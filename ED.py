
#==============================================================================================
# The Jabalín morphological generator for Arabic verbs
#
# Copyright (c) 2012 Susana López Hervás, Alicia González Martínez, Antonio Moreno Sandoval
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
# along with this program.  If not, see <http://www.gnu.org/licenses/>
#==============================================================================================

##################################################################
# MODULE             EXTERNAL DERIVATION
###################################################################

import re
import sys

# This function gets all the pattern VIII stems, included in dict_T,
# and applies the corresponding rules if the cod_ED is '1'.
# It returns the dict_T dictionary modified.
 
def External_derivation(dict_T, cod_ED):
    cod = int(cod_ED)
    if cod == 1:
        # prefix -تَ (-ta) is added to pattern VIII stems
        dict_T['VP']=re.sub(r"(.+)", r"تَ\1", dict_T['VP'])
        dict_T['VIAM']=re.sub(r"(.+)", r"تَ\1", dict_T['VIAM'])
        dict_T['VI']=re.sub(r"(.)(.+)", r"\1تَ\2", dict_T['VI'])

    return (dict_T)
