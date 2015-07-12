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
# MODULE             STEM ADJUSTMENT
###################################################################

import re
import sys

def list_rules_stem_adjustment(f, form, dict_cod, root, lema):

    # if ID addition is '3' the letter in second position is removed
    # from VIA and VIP forms
    forms = ['VI-A', 'VI-P']
    if (f in forms) & (dict_cod['Internal derivation']['addition']=='3'):        
        form = re.sub(r"(.)(.)(.*)", r"\1\3", form)     # A1

    # assimilation of V (u) from the ta- prefix in perfective passive template
    # patterms V, VI triliteral and II quadriliteral, ta -> tu
    # eg.: ta.fuw.çal -> tu.fuw.çil
    if (f=='VP-P')&(dict_cod['External derivation']=='1'):
        form=form.replace(form[1], 'ُ', 1)               # A2
   
    
    # for template L, if a sequence CCC is found from the end to the beginning,
    # it is substituted by CCaC
    if dict_cod['Template']== 'L':
        form=re.sub(r"(.*)(?<=[Eبتثجخحدذرزسشصضطظعغفقكلمنهويأءؤئّ])(.)(?<=[Eبتثجخحدذرزسشصضطظعغفقكلمنهويأءؤئّ])(.)(?<=[Eبتثجخحدذرزسشصضطظعغفقكلمنهويأءؤئّ])",\
                          r"\1\2َ\3" , form)             # A3

    # for template H, if a sequence CCC is found from the end to the beginning,
    # it is substituted by CaCC
    if dict_cod['Template']== 'H':
        form=re.sub(r"(.*)(?<=[Eبتثجخحدذرزسشصضطظعغفقكلمنهويأءؤئّ])(.)(?<=[Eبتثجخحدذرزسشصضطظعغفقكلمنهويأءؤئّ])(.)(?<=[Eبتثجخحدذرزسشصضطظعغفقكلمنهويأءؤئّ])",\
                    r"\1َ\2\3" , form)                   # A4
    

    # ASSIMILATION OF INFIX -T- IN PATTERN VIII   
    if dict_cod['Internal derivation']['addition']=='2':

        form = re.sub(r'^(.?)[وي]ت',r'\1تت', form)       # B1 [wy]t -> t~ / ^.?_     eg وتحد -> تتحد
        form = re.sub(r'^(.?[ثدذطظ])ت', r'\1\1', form)   # B2 t -> ~ / ^[þdðTZ].?_   eg ظتنن -> ظظنن
        form = re.sub(r'^(.?ز)ت', r'\1د', form)          # B3 t -> d / ^.?z_         eg زتوج -> زدوج
        form = re.sub(r'^(.?[صض])ت', r'\1ط', form)       # B4 t -> T / ^.?[DS]_      eg ضترب -> ضطرب    

        if re.search(r'^ء', root):
            if re.search(r'^اتّ', lema):
                form = re.sub(r'^(.?)ءت',r'\1تت', form)  # B5  ct -> t~ / ^.?_       eg ءتخذ -> تّخذ
        

    return(form)



def rules_stem_adjustment(dict_forms, dict_cod, root, lema):
    forms = ['VP-A', 'VP-P', 'VI-A', 'VI-P', 'VIAM']

    for f in forms:
        dict_forms[f] = list_rules_stem_adjustment(f, dict_forms[f], dict_cod, root, lema)

    return (dict_forms)
    
            
