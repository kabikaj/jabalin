
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


###################################################################
# MODULE             PROSODIC TEMPLATE
###################################################################

import re
import sys
import utilities


# This function gets a codec specifing the Prosodic Template which has to be applied, L or H,
# and returns a dictionary containing the templates for Perfective,Imperfective and Imperative.
def select_prosodic_template(cod_template):
    dict_PT = {}
    if cod_template == 'L':
        dict_PT={'VP': 'FFVFWF', 'VI':'VFFFWF', 'VIAM':'FFFWF'}
    elif cod_template == 'H':
        dict_PT={'VP': 'FFVFFWF', 'VI':'VFFFFWF', 'VIAM':'FFFFWF'}
    return (dict_PT)




# This function gets as parameters the root+affixation and the prosodic template
# It inserts the root+affixation in the template and returns the resulting string, the stem
def apply_prosodic_template(der_root, template):
    # the order is inverted to apply the substitutions in the opposite direction
    rev_temp=utilities.invertir(template)
    rev_root=utilities.invertir(der_root)

    # each character of the root+affixation is substituted by the Fs of the template
    rev_temp_root=rev_temp
    for char in rev_root:
        rev_temp_root=rev_temp_root.replace('F', char, 1)

    # is there are remaiming Fs, they are removed from the stem
    rev_temp_root=rev_temp_root.replace('F', '')

    # again, we invert the form, so that the characters of the stem are in the correct direction
    temp_root = utilities.invertir(rev_temp_root)

    return(temp_root)


# This function insterts the root+affixation characters in the templates, and
# returns the dictionary with i-stem (VP), p-stem (VI), and m-stem (VIAM)
def apply_prosodic_all_templates(der_root, dict_PT):
    # p-stem
    dict_PT['VP'] = apply_prosodic_template(der_root, dict_PT['VP'])
    # i-stem
    dict_PT['VI'] = apply_prosodic_template(der_root, dict_PT['VI'])
    # m-stem
    dict_PT['VIAM'] = apply_prosodic_template(der_root, dict_PT['VIAM'])

    return(dict_PT)


# This function gets as parameters the root+affixation and the code, so that the prosodic template
# function can be applied. It returns a dictionary of templates with the root+affixation replacements
def prosodic_template(der_root, cod_template):
    dict_PT = select_prosodic_template(cod_template)
    dict_PT_root = apply_prosodic_all_templates(der_root, dict_PT)

    return (dict_PT_root)





