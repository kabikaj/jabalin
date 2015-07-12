
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
# MODULE             UTILITIES
###################################################################
import re
import sys

# This function inverts a string
def invertir(var):
    return var[::-1]


# This function returns 'true' if the line passed as a parameter begins with the word 'ENTRY'
# or if it's an empty line, else return 'false'
def delete_line(line):
    if re.match("ENTRY(.+)", line):
        return (True)
    if re.match("^\n", line):
        return(True)
    return(False)


# This function gets a code and returns a dictionary with its decodification
# or empty dictionary if something worked wrong
# i.e. {'Vocalization': {'Perf V2': '0', 'Imperf V2': '0', 'Imperf V1': '0'},
#       'Internal derivation': {'lengthening': '1', 'addition': '0'},
#       'Template': 'H',
#       'External derivation': '0'}
def parse_code_verbs(code):
    if len(code)!=7:
        print("error CODE: " + code)
        return ()

    dict_parse={}
    dict_parse["Internal derivation"]={'lengthening': code[0], 'addition': code[1]}
    dict_parse["Template"]=code[2]
    dict_parse["External derivation"]=code[3]
    dict_parse["Vocalization"]={'Perf V2': code[4], 'Imperf V1': code[5], 'Imperf V2': code[6]}

    return(dict_parse)


        
def printFile_forms(lema, root, code, dict_forms, n_file):
    k_forms = dict_forms.keys()

    for k in k_forms:
        print(dict_forms[k] + '\t'+ k + '\t' + str(lema) + '\t'+\
              str(root)+'\t'+ str(code), file=n_file)


def printFile_forms_from_dictForms(lema, root, code, d_forms, n_file):

    printFile_forms(lema, root, code, d_forms['VP']['Active'], n_file)
    printFile_forms(lema, root, code, d_forms['VP']['Pasive'], n_file)
    printFile_forms(lema, root, code, d_forms['VI']['Active']['Indicative'], n_file)
    printFile_forms(lema, root, code, d_forms['VI']['Active']['Subjunctive'], n_file)
    printFile_forms(lema, root, code, d_forms['VI']['Active']['Yusive'], n_file)
    printFile_forms(lema, root, code, d_forms['VI']['Pasive']['Indicative'], n_file)
    printFile_forms(lema, root, code, d_forms['VI']['Pasive']['Subjunctive'], n_file)
    printFile_forms(lema, root, code, d_forms['VI']['Pasive']['Yusive'], n_file)
    printFile_forms(lema, root, code, d_forms['VIAM'], n_file)

    
