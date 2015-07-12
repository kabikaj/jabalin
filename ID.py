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
# MODULE             INTERNAL DERIVATION
###################################################################

import re
import sys

# This function applies the rules classified as lengthening operations of Internal
# Derivation. The rules are applied to the root, which is passed as a parameter
def ID_rules_lenghtening(root, cod_lenghtening):
    cod=int(cod_lenghtening)
    # the last character is duplicated
    if cod==1:
        root=re.sub(r"(.*)(.)", r"\1\2\2", root)

    # 'ّ' ('~') is added between the second and the third characters     
    elif cod==2:
        root=re.sub(r"(..)(.*)", r"\1ّ\2", root)
        
    # 'E' (lengthening mark) is added between the first and the second characters.
    elif cod==3:
        root=re.sub(r"(.)(.*)", r"\1E\2", root)

    # 'E' is added at the end
    elif cod==4:
        root=re.sub(r"(.+)", r"\1E", root)

    # the second character is duplicated
    elif cod==5:
        root=re.sub(r"(.)(.)(.*)", r"\1\2\2\3", root)

    return (root)


# This function applies the rules classified as addition operations of Internal
# Derivation. Again, the rules are applied to the root
def ID_rules_addition(root, cod_addition):
    cod=int(cod_addition)
    # 'ن' ('n') is added at the beginning
    if cod==1:
        root=re.sub(r"(.+)", r"ن\1", root)

    # 'ت' ('t') is added between the first and the second characters.
    elif cod==2:
        root=re.sub(r"(.)(.*)", r"\1ت\2", root)

    # 'أ' ('Á') is added at the beginning
    elif cod==3:
        root=re.sub(r"(.+)", r"أ\1", root)
        
    # 'ست' ('st') is added at the beginning
    elif cod==4:
        root=re.sub(r"(.+)", r"ست\1", root)

    # 'E' is added between the second and the third characters.
    elif cod==5:
        root=re.sub(r"(..)(.*)", r"\1E\2", root)

    # 'و' ('w') is added between the second and the third characters.
    elif cod==6:
        root=re.sub(r"(..)(.*)", r"\1و\2", root)

    # 'وو' ('ww') is added between the second and the third characters.
    elif cod==7:
        root=re.sub(r"(..)(.*)", r"\1وو\2", root)

    # 'ن' ('n') is added between the second and the third characters.
    elif cod==8:
        root=re.sub(r"(..)(.*)", r"\1ن\2", root)
       
    return (root)



# This function applies all the rules of the Internal Derivation
# to the root, which is passed as parameter
def Internal_derivation(root, cod_ID):

    root_id = ID_rules_lenghtening(root, cod_ID["lengthening"])
    root_id = ID_rules_addition(root_id, cod_ID["addition"])

    return(root_id)


    
