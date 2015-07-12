
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
# MODULE             VOCALIZATION
##################################################################

import re
import sys

dict_vocalization = {'Perf W': {'0': 'َ', '1': 'ُ', '2':'ِ'},\
                     'Imperf V': {'0': 'َ', '1': 'ُ'}, \
                     'Imperf W': {'0': 'ِ', '1': 'ُ', '2':'َ'}}

# This function generates perfective active
def generate_VPA (perfective, cod_perfect):

    # vowel V default values
    VPA = perfective.replace('V', 'َ')
    # vowel W values in dictionary
    VPA = VPA.replace('W', dict_vocalization['Perf W'][cod_perfect])

    return(VPA)


# This function generates perfective passive
def generate_VPP (perfective):

    # vowel V default values
    VPP = perfective.replace('V', 'ُ')
    # vowel W default values
    VPP = VPP.replace('W', 'ِ')

    return(VPP)


# This function generates imperfective active
def generate_VIA (imperfective, cod_imperfV, cod_imperfW):

    # vowel V values in dictionary
    VIA = imperfective.replace('V', dict_vocalization['Imperf V'][cod_imperfV])
    # vowel W values in dictionary
    VIA = VIA.replace('W', dict_vocalization['Imperf W'][cod_imperfW])

    return(VIA)



# This function generates imperfective passive
def generate_VIP (imperfective):

    # vowel V default values
    VIP = imperfective.replace('V', 'ُ')
    # vowel W default values
    VIP = VIP.replace('W', 'َ')

    return(VIP)


# This function generates imperative active
def generate_VIAMA (imperative, cod_imperfW):

    # vowel W values in dictionary
    VIAMA = imperative.replace('W', dict_vocalization['Imperf W'][cod_imperfW])

    return(VIAMA)



# This function returns a dictionary with different stems. Stems vary in tense/aspect and voice.
# Hence we have active p-stem, passive p-stem, active i-stem, passive i-stem and active m-stem
# i.e. {'VI-P': 'udrhmam', 'VI-A': 'adrhmim', 'VP-A': 'drahmam', 'VP-P': 'druhmim', 'VIAM-A': 'drhmim'}
def generate_Active_and_Pasive (dict_tenses, cod_vocalization):

    dict_voc_tens={}
    dict_voc_tens['VP-A']=generate_VPA(dict_tenses['VP'],\
                                        cod_vocalization['Perf V2'])
    dict_voc_tens['VP-P']=generate_VPP(dict_tenses['VP'])
    dict_voc_tens['VI-A']=generate_VIA(dict_tenses['VI'],\
                                             cod_vocalization['Imperf V1'], \
                                             cod_vocalization['Imperf V2'])
    dict_voc_tens['VI-P']=generate_VIP(dict_tenses['VI'])
    dict_voc_tens['VIAM']=generate_VIAMA(dict_tenses['VIAM'], \
                                                  cod_vocalization['Imperf V2'])
    return(dict_voc_tens)
