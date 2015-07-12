
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
# MODULE             INFLECTIONAL SYSTEM
###################################################################

import re
import sys


# This function gets a list containing elements which are tuples, and returns a dictionary
def pass_list_to_dictionary (list_tuples):

    dict={}
    for l in list_tuples:
        dict[l[1]]=l[0]
    return dict


# This function gets a form, a list of the inflectional suffixes, a table with
# the partial tags of each suffix, and f, which indicates if the form is perfective,
# imperfective or imperative. Returns a list of tuples: inflected form with its tag
def STEM_plus_suf(form, list_cod, table_tag, f):
    list_inf_tag = [[form+table_tag[l], f+l] for l in list_cod]

    return (list_inf_tag)


# This function gets a form, a list of the prefixes, a table with the partial tags
# of each suffix, and f, which indicates if the form is perfective, imperfective
# or imperative. Returns a list of tuples: inflected form with its tag
def pre_plus_STEM(form, list_cod, table_tag, f):
    list_inf_tag = [[table_tag[l]+form, f+l] for l in list_cod]
    return (list_inf_tag)


# This function gets a form, a list of prefixes and suffixes, a table with the partial
# tags of each suffixes, and f which, indicates if the form is perfective, imperfective
# or imperative. Returns a list of tuples: inflected form with its tag
def pre_plus_STEM_plus_suf(form, list_cod, table_tag, f):
    list_inf_tag=[]
    for l in list_cod:
        (pre, suf)=table_tag[l].split('_')
        list_inf_tag.append([pre+form+suf, f+l])

    return (list_inf_tag)


# This function gets the dict with the forms and returns a dictionary with the inflected forms
# for passive and active perfective as a list with pairs of inflected form and its tag                   
def inflected_perfective_forms(dict_forms):
    table_perfective = {'N1SN': 'تُ',
                        'N1PN': 'نَE',
                        'N2SM': 'تَ',
                        'N2SF':'تِ',
                        'N2DN': 'تُمَE',
                        'N2PM':'تُم',
                        'N2PF': 'تُنَّ',
                        'N3SM': 'َ',
                        'N3SF': 'َت',
                        'N3DM': 'َE',
                        'N3DF': 'َتَE',
                        'N3PM': 'ُEا',
                        'N3PF': 'نَ'}
    cod = table_perfective.keys()

    list_act = STEM_plus_suf(dict_forms['VP-A'], cod, table_perfective,'VPA')
    list_pas = STEM_plus_suf(dict_forms['VP-P'], cod, table_perfective,'VPP')


    return({'Active': pass_list_to_dictionary(list_act),
            'Pasive': pass_list_to_dictionary(list_pas)})

   
                 
# This function gets the form VIAM (imperatives) and returns a list
# with pairs of inflected form and its tag
def inflected_imperative_forms(form_VIAM):
    table_imperat = {'2SM': '',
                     '2SF': 'ِE',
                     '2DN': 'َE',
                     '2PM': 'ُEا',
                     '2PF': 'نَ'}

    cod = table_imperat.keys()

    infYtag_VIAM= STEM_plus_suf(form_VIAM, cod, table_imperat, 'VIAM')
         
    return (pass_list_to_dictionary(infYtag_VIAM))




# This function adds imperfective inflection to i-stems active and passive,
# without the suffixes for mood
def processing_imperfective(dict_forms):
    table_imperf_pre = {'1SN': 'أ',
                        '1PN': 'ن',
                        '2SM': 'ت',
                        '3SM': 'ي',
                        '3SF': 'ت'}
    cod_prefs = table_imperf_pre.keys()
    
    table_imperf_pre_suf = {'2SF': 'ت_ِE',
                            '2DN': 'ت_َE',
                            '2PM': 'ت_ُE',
                            '2PF': 'ت_نَ',
                            '3DM': 'ي_َE',
                            '3DF': 'ت_َE',
                            '3PM': 'ي_ُE',
                            '3PF': 'ي_نَ'}
    cod_pref_sufs = table_imperf_pre_suf.keys()


    pre_Active = pre_plus_STEM(dict_forms['VI-A'], cod_prefs, table_imperf_pre,'')+ \
                 pre_plus_STEM_plus_suf(dict_forms['VI-A'], cod_pref_sufs, table_imperf_pre_suf,'')
    
    pre_Pasive = pre_plus_STEM(dict_forms['VI-P'], cod_prefs, table_imperf_pre,'')+ \
                 pre_plus_STEM_plus_suf(dict_forms['VI-P'], cod_pref_sufs, table_imperf_pre_suf,'')
 

    return({'Active': pass_list_to_dictionary(pre_Active),
            'Pasive': pass_list_to_dictionary(pre_Pasive)})
    

# This function produced a dictionary with the imperfective forms for passive or active i-stems
# The function gets as parameters a dictionary of imperfective forms, a table with the rules to be applied,
# a flag f indicating if it is active or passive, and a flag t (N:Indicative, S:Subjunctive, Y:Jussive)
def processing_Indic_Subj_Juss_AorP(forms_preprocess, table, f, t):
    keys=forms_preprocess.keys()

    ImperfParadigm={}
    
    for k in keys:
        if k in table:
            ImperfParadigm.setdefault('VI'+f+t+k, forms_preprocess[k]+table[k])
        else:
            ImperfParadigm.setdefault('VI'+f+t+k, forms_preprocess[k])
          
    return (ImperfParadigm)



# This function adds indicative inflection to active and passive i-stems
# and includes them in a dictionary
def processing_Indicative(d_pre_proces):
    table_indicat = {'1SN': 'ُ',
                     '1PN': 'ُ',
                     '2SM': 'ُ',
                     '2SF': 'نَ',
                     '2DN': 'نِ',
                     '2PM': 'نَ',
                     '3SM': 'ُ',
                     '3SF': 'ُ',
                     '3DM': 'نِ',
                     '3DF': 'نِ',
                     '3PM': 'نَ'}
    d_Indicative={}
    d_Indicative['Active']= processing_Indic_Subj_Juss_AorP(d_pre_proces['Active'], table_indicat, 'A', 'N')
    d_Indicative['Pasive']= processing_Indic_Subj_Juss_AorP(d_pre_proces['Pasive'], table_indicat, 'P', 'N')
    return (d_Indicative)

# This function adds subjunctive inflection to active and passive i-stems
# and includes them in a dictionary
def processing_Subjunctive(d_pre_proces):
    table_subjunctive = {'1SN': 'َ',
                         '1PN': 'َ',
                         '2SM': 'َ',
                         '2PM': 'ا',
                         '3SM': 'َ',
                         '3SF': 'َ',
                         '3PM': 'ا'}
    
    d_Subjunctive={}
    d_Subjunctive['Active']= processing_Indic_Subj_Juss_AorP(d_pre_proces['Active'], table_subjunctive, 'A', 'S')
    d_Subjunctive['Pasive']= processing_Indic_Subj_Juss_AorP(d_pre_proces['Pasive'], table_subjunctive, 'P', 'S')
    return (d_Subjunctive)


# This function adds jussive inflection to active and passive i-stems
# and includes them in a dictionary
def processing_Jussive(d_pre_proces):
    table_yusive = {'2PM': 'ا',
                    '3PM': 'ا'}
    
    d_Yusive={}
    d_Yusive['Active']= processing_Indic_Subj_Juss_AorP(d_pre_proces['Active'], table_yusive, 'A', 'Y')
    d_Yusive['Pasive']= processing_Indic_Subj_Juss_AorP(d_pre_proces['Pasive'], table_yusive, 'P', 'Y')
    return (d_Yusive)



# This function applies all the inflection to imperfctive forms
def inflected_imperfective_forms(dict_forms):
    d_imperf = processing_imperfective(dict_forms)
    d_Indicative = processing_Indicative(d_imperf)
    d_Subjunctive = processing_Subjunctive(d_imperf)
    d_Jussive = processing_Jussive(d_imperf)

    
    return({'Active': {'Indicative': d_Indicative['Active'],
                       'Subjunctive': d_Subjunctive['Active'],
                       'Yusive': d_Jussive['Active']},
            'Pasive': {'Indicative': d_Indicative['Pasive'],
                       'Subjunctive': d_Subjunctive['Pasive'],
                       'Yusive': d_Jussive['Pasive']},})




# this function passes each form to the full inflectional paradigm
# and creates a dict of forms
def Inflectional_system (dict_forms):
    dict_Inf_forms={}

    dict_Inf_forms['VP'] = inflected_perfective_forms(dict_forms)
    dict_Inf_forms['VI'] = inflected_imperfective_forms(dict_forms)
    dict_Inf_forms['VIAM'] = inflected_imperative_forms(dict_forms['VIAM'])
    

    return (dict_Inf_forms)


