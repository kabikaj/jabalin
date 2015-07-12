
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
#                   JABALÍN GENERATION SYSTEM                     #
###################################################################


import sys

import utilities
import ID
import PT
import ED
import vocalization
import stem_adjustment
import Inflec
import phonotactics


def generation_verbs(filename, file_out):
    try:
        with open(filename, encoding='utf8') as file, open(file_out, 'w', encoding='utf8') as generation_file:
            try:
                # FOR EACH LINE IT SAVES LEMMA, ROOT, CODE, INFLECTION AND TAG
                for each_line in file:
                    if not utilities.delete_line(each_line):
                        (lema, root, code)=each_line.strip().split('\t',2)
                        
                        # parseamos el código
                        dict_code=utilities.parse_code_verbs(code)

                        # 1.- INTERNAL DERIVATION
                        deriv_root = ID.Internal_derivation(root, \
                                                            dict_code['Internal derivation'])

                        # 2.- PROSODIC TEMPLATE
                        dict_RootInPT = PT.prosodic_template(deriv_root, \
                                                             dict_code['Template'] )

                        # 3.- EXTERNAL DERIVATION
                        deriv_RootInPT = ED.External_derivation(dict_RootInPT, \
                                                                dict_code['External derivation'])

                        # 4.- VOCALIZATION
                        dict_act_pas_forms = vocalization.generate_Active_and_Pasive(deriv_RootInPT, \
                                                                                 dict_code['Vocalization']) 

                        # 5.- STEM ADJUSTMENTS
                        dict_syl_forms = stem_adjustment.rules_stem_adjustment(dict_act_pas_forms, dict_code, root, lema)
            
                        # 6.- INFLECTED SYSTEM
                        dict_inflec_forms = Inflec.Inflectional_system(dict_syl_forms)


                        # 7.- PHONOTACTIC CONSTRAINTS AND ORTHOGRAPHIC NORMALIZATION
                        final_forms = phonotactics.phonotactic_rules(dict_inflec_forms, lema, root, dict_code)
                        utilities.printFile_forms_from_dictForms(lema, root, code, final_forms, generation_file)

            except ValueError as verror1:
                print('Value error Principal: ' + str(verror1))


    except IOError as ioerr:
        print('File error: ' + str(ioerr))
        return(None)





# call to generation_verbs function
try:
    generation_verbs(sys.argv[1], sys.argv[2])
except:
    print('Program expects input and output lexicons:\n\
          JabalinGenerator.py lexicon_lemas_jabalin.txt name_output_file.txt')


