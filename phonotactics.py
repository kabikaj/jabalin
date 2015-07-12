
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
# MODULE   PHONOTACTIC CONSTRAINTS AND ORTHOGRAPHIC NORMALIZATION #
###################################################################

import re
import sys



# This function sukunizes the form and applies long vowels normalization. 
def Sukun_and_Long_vowels_normalization(form):
    
    # sukunizer
    form=re.sub(r"([ءأئؤبتثجحخدذرزسشصضطظعغفقكلمنوهي])((?![ًٌٍَُِّْ])|(?=$))", r"\1ْ", form)
                                                                          # C1   sukunizer
    # long vowels normalization
    form = form.replace('َE', 'َا')                                         # C2   aE -> aE
    form = form.replace('ُE', 'ُو')                                         # C3   uE -> uw
    form = form.replace('ِE', 'ِي')                                         # C4   iE -> iy

    return(form)





# initial consonant cluster constrints rules - preprocessing initial alif
def  preprocessing_Initial_Alif(form):
    
    C = r'[بتثجخحدذرزسشصضطظعغفقكلمنهويأءؤئ]'
    form=re.sub(r'^({0}ْ{1}ّ?ُ)'.format(C,C), r'اُ\1',form)                  # D1   ∅ -> Au / ^_C·C~?u  
    form=re.sub(r'^({0}ْ{1}ّ?[^ُ])'.format(C,C), r'اِ\1',form)               # D2   ∅ -> Ai / ^_C·C~?[^u]

    return form

    



def Apply_WeakLettersRules(form, al_code, lema, root, d_code):
    
    # Apocopated imperative (rare real irreg):
    # if simple verb, imperative form, first radical waw; and if (thematic vowel of imperfective kasra) or 
    # ((second or third radical is a guttural خ غ ح ع ء ه or semiguttural ر) and (thematic verb is fatha)):
    # then the fist radical is removed from the form (plus prosthetic alif)
    Gutturals = ['خ','غ','ح','ع','ء','ه','ر']
    if d_code['Internal derivation']['lengthening']=='0' and d_code['Internal derivation']['addition']=='0'\
       and d_code['Template']=='L' and al_code[:4]=='VIAM' and root[0]=='و'\
       and ((d_code['Vocalization']['Imperf V2']=='0') or ((d_code['Vocalization']['Imperf V2']=='2')\
                                                           and (root[1] in Gutturals or root[2] in Gutturals))):
            form=form[4:]                                                # E1

    form=re.sub('^اِوْ','اِيْ',form)                                         # E2    y -> w / ^Ai_·    (iw constraint for imperatives)
    
    if (d_code['Internal derivation']['addition']!='3')and (re.search('^[وي]',root))and(len(root)!= 4):
        form=re.sub('^([ء-ي]َ)وْ([ء-ي]ِ)',r'\1\2',form)                     # E3    w· -> ∅ / ^Ca_Ci
        
    form=re.sub('(.[ء-ي]ّ?ِ)[وي]ْ(?!$)',r'\1ي',form)                        # E4    [wy]· -> y / [^^]C~?i_[^$] 
    
    form=re.sub('([ء-ي]ّ?[َ-ِ])[وي]ْ$',r'\1',form)                           # E5    [wy]· -> ∅ / C~?v_$
    
    if d_code['Internal derivation']['lengthening']!='1' and not re.match('[12]',d_code['Internal derivation']['addition'])\
       and len(root)!=4 and re.search('[^وي][^وي].$', lema):
        
        form=re.sub('([ء-ي])ْ[وي]([َ-ِ])(?=[ء-ي]ْ)',r'\1\2',form)            # E6    ·[wy] -> ∅ / C_vC·
        
        form=re.sub('([ء-ي])ْ[وي]َ(?!ي)(.[َ-ِ])',r'\1َا\2',form)              # E7    ·[wy] -> A / C_a[^y]
    
        form=re.sub('(?<=[ء-ي])ْ[وي]ِ([^ي][َ-ِ])',r'ِي\1',form)               # E8    ·[wy]i -> iy / C_[^y]v
        
        form=re.sub('([ء-ي])ْ[وي](ُ)([^ي][َ-ِ])',r'\1\2و\3',form)            # E9    ·[wy]u -> uw / C_[^y]v
    
        form=re.sub('^([ء-ي]َ)[وي][َ-ِ]([^ي][َ-ِ])',r'\1ا\2',form)            # E10   [wy]v -> A / ^Ca_[^y]v
        
        form=re.sub('(.[ء-ي]ّ?َ)[وي]َ([ء-ي]َ)',r'\1\2',form)                 # E11   [wy]a -> ∅ / .C~?a_Ca
    
    form=re.sub('ُ[وي]ِ(.[َ-ِ])',r'ِي\1',form)                                # E12   u[wy]i -> iy / _Cv  
    
    if re.match('[124]',d_code['Internal derivation']['addition']) and re.search('[^وي].$',lema) and re.search('[^وي]$',root):
        form=re.sub('([ء-ي]َ)[وي][َ-ِ]([^ي][َ-ِ])',r'\1ا\2',form)             # E13   [wy]v -> A / Ca_[^y]v  (adaptada para VII-VIII-X)
    
    if (d_code['Vocalization']['Imperf V2']=='1')and(re.search('[وي](?!و)(?!ي).$',root)):
        form=re.sub('([ء-ي])َوَ([ء-ي]ْ)',r'\1ُ\2',form)                      # E14   awa -> u / C_C·

    if (d_code['Vocalization']['Imperf V2']!='1') and len(root)==3 and not\
       re.match('[12]',d_code['Internal derivation']['addition']):              
        form=re.sub('([ء-ي])َ[وي][َِ]([^ي]ْ.)',r'\1ِ\2',form)                 # E15   a[wy][ai] -> i / C_[^y]·.

    if (re.search('^.[^وي][وي]$', root) or re.search('^.[وي][^وي]$', root)): 
        form=re.sub('(َ)[وي][َِ]([ء-ي]ْ)',r'\1\2',form)                      # E16   [wy][ai] -> ∅ / a_C·
    
    form=re.sub('[ُِ][وي](ُو)',r'\1',form)                                  # E17   [ui][wy] -> ∅ / _uW

    if d_code['Vocalization']['Perf V2']!='2' or (root[1]!='و' and root[1:]!='يي'):
        form=re.sub('ُ[وي](ِ.ْ)',r'\1',form)                                # E18   u[wy] -> ∅ / C_iC· 
    
    if (((d_code['Vocalization']['Perf V2']!='1')|(d_code['Vocalization']['Imperf V2']!='1')) and (al_code[2]!='P')): 
        form=re.sub('([ء-ي]ّ?)[ُِ][وي](ِي)',r'\1\2',form)                    # E19   [ui][wy] -> ∅ / C~?_iy

    form=re.sub('(َ)[وي]ُو',r'\1وْ',form)                                   # E20   [wy]uw -> w· / a_
    
    if (d_code['Vocalization']['Imperf V2']!='1') or al_code[2]=='P':            
        form=re.sub('([^ي]َ)[وي][َُ]$',r'\1ى',form)                         # E21   [wy][au]  -> Y / [^y]a_$    (pasiva & imperf en u sí cambia a alif maqsura)
        
    if (d_code['Vocalization']['Imperf V2']=='1'):
        form=re.sub('(َ)وَ$',r'\1ا',form)                                  # E22   wa -> A / a_$

    form=re.sub('(يَ)يَ$',r'\1ا',form)                                     # E23   ya -> A / ya_$

    form=re.sub('(ُو)ُ$',r'\1',form)                                       # E24   u -> ∅ / uw_$

    form=re.sub('ِوَ',r'ِيَ',form)                                           # E25   w -> y / i_a

    if re.match('VPAN3[SD]F',al_code):
        form=re.sub('([ء-ي]َ)[وي]َ([ء-ي][َْ]ا?)$',r'\1\2',form)              # E26   [wy]a -> ∅ / Ca_C[·a]A?$

    form=re.sub('(ُو|ِي)ْ',r'\1',form)                                      # E27   · -> ∅ / (uw|iy)_
    
    form=re.sub('(ِ)[وي]ُ$',r'\1ي',form)                                   # E28   [wy]u -> y / i_$

    if re.search('^..و$',root) and\
       ((d_code['Internal derivation']['lengthening']!='0' or d_code['Internal derivation']['addition']!='0')\
       and not re.match('V[IP][AP][NSY]3PM',al_code) and not re.match('VI[AP][NSYM]2PM',al_code))\
        or ((d_code['Internal derivation']['lengthening']=='0' and d_code['Internal derivation']['addition']=='0')\
        and (d_code['Vocalization']['Perf V2']=='0' and d_code['Vocalization']['Imperf V2']=='1')\
        and (re.match('VIP[NSY][23]D[FMN]',al_code) or re.match('VIP[NSY][23]PF',al_code) or re.match('VIPN2SF',al_code))):

        form=re.sub('([ء-ي]ّ?َ)و',r'\1ي',form)                             # E29   w -> y / C~?a_
    
    form=re.sub('َيِي','َيْ',form)                                           # E30   yiy -> y· / a_ 
    
    return(form)




    
def Apply_ShaddaRules(form, al_code, lema, root, d_code):

    # this rule suggest the need of a syllabic frontier mark
    if (d_code['Internal derivation']['lengthening']=='1')\
        or (\
              len(root)==3 and (not re.match(r'^.([يو])\1$',root))\
              and ((not 'ت' in root)\
                   or (re.search('.ت[َ-ِ]ت[َ-ِ]ت[َ-ِ]',form))\
                   or (root[0]=='ت' and (d_code['External derivation']!='1')\
                       and not (d_code['Internal derivation']['addition']=='4'\
                       and root[:2]=='تو'))\
                   or (re.match('^.تت$',root) and not re.match('VP[AP]N3DF',al_code) and d_code['Internal derivation']['addition']!='2')\
                   )\
            ):

            form=re.sub(r'([^ْ])([ء-ي])[َ-ِ]\2([َ-ِ])',r'\1\2ّ\3',form)        # F1   C¹v¹C¹ -> C¹~ / [^·]_v² (and not beginning)        
            form=re.sub(r'([ء-ي])ْ([ء-ي])([َ-ِ])\2([َ-ِ])',r'\1\3\2ّ\4',form)  # F2  ·C²v¹C² -> v¹C²~ / C¹_v²	



    if root[1]==root[2] and not re.match('[YM]',al_code[3]):
        form=re.sub(r'ْ([ء-ي])([َ-ِ])\1ْ$',r'\2\1َّ',form)                     # F3   ·C¹v¹C¹· -> v¹C¹~a / _$

    # ORTHOGRAPHIC
    form=re.sub(r'([ء-ي])ْ\1([َ-ِ])',r'\1ّ\2',form)                          # F4   ·C¹ -> ~ / C¹_v¹     (C¹·C¹v¹ -> C¹~v¹)

    return(form)





# initial consonant cluster constrints rule - posprocessing initial
def  posprocessing_Initial_Alif(form):

    C = r'[بتثجخحدذرزسشصضطظعغفقكلمنهويأءؤئ]'
    form=re.sub(r'^ا[َُِ]({0}[َُِ])'.format(C), r'\1',form)                    # D3   Av -> ∅ / ^_Cv
    
    return form





def Apply_HamzaRules(form):

    try:
        
        form_trasl=form
        
        form_trasl=re.sub('^[ءؤئأ]ِ','إِ',form_trasl)                      # G1 [cúýÁ] -> À / ^_i  eg إِبدَاء

        form_trasl=re.sub('^[ءؤئإ](?=[َُ])','أ',form_trasl)                # G2 [cúýÀ] -> Á / ^_[au]  eg أُسرَةُ

        form_trasl=re.sub('(^|[^اُِي])[ءأإؤئ]َا',r'\1آ',form_trasl)        # G3 [cÁÀúý]aA -> Ã / (^|[^Auiy])_  eg آسِف / قُرآن
        
        form_trasl=re.sub('[ءأإؤئ]َ[ءأإؤئ]ْ','آ',form_trasl)               # G4 [cÁÀúý]a[cÁÀúý]· -> Ã  eg آتَكِلُ

        form_trasl=re.sub('ْ[ءإؤئ]َ','ْأَ',form_trasl)                       # G5 [cÀúý] -> Á / ·_a  eg أَبأَرُ

        form_trasl=re.sub('ْ[ءأإئ]ُ','ْؤُ',form_trasl)                       # G6 [cÁÀý] -> ú / ·_u  eg اُبؤُس

        form_trasl=re.sub('ي[أإؤئ]([ًٌٍَُِ]ا?)$',r'يء\1',form_trasl)           # G8 [ÁÀúý] -> c / y_[aiuâîû]A?$  eg جُزَيءٌ

        form_trasl=re.sub('ي[ءأإؤ](?!ًا)(?=..)','يئ',form_trasl)          # G9 [cÁÀú] -> ý / y_(?!âA)(?=..)  eg بَدِيئَة 

        form_trasl=re.sub('ا[أإؤئ]َ','اءَ',form_trasl)                     # G10 [ÁÀúý] -> c / A_a  eg بَدَاءَة

        form_trasl=re.sub('ُ[ءأإئ](?=[َُْ])','ُؤ',form_trasl)                 # G11 [cÁÀý] -> ú / u_[a·u]  eg بَطُؤتُ

        form_trasl=re.sub('و[ءأإئ](?=[َُ].)(?!ًا)','وؤ',form_trasl)         # G12 [cÁÀý] -> ú / w_(?=[au].)(?!âA)  eg مَوبُوؤَينِ

        form_trasl=re.sub('و[أإؤئ]([ًٌَُ]ا?)$',r'وء\1',form_trasl)           # G13 [ÁÀúý] -> c / w_[auâû]A?$  eg بُرُوءٌ

        form_trasl=re.sub('َ[ءإؤئ](?=ّ?[َْ])','َأ',form_trasl)                # G14 [cÀúý] -> Á / a_~?[a·]  eg وَثَأتُ

        form_trasl=re.sub('(?<=[َا])[ءأإئ]ُ(?=.)','ؤُ',form_trasl)          # G15 [cÁÀý] -> ú / [aA]_u. eg يُوثَؤُوا

        form_trasl=re.sub('َ[ءإؤئ]([ٌُ])$',r'َأ\1',form_trasl)               # G16 [cÀúý] -> Á / a_[uû]$  eg وَثَأُ

        form_trasl=re.sub('ا[أإؤئ]([ٌُ])$',r'اء\1',form_trasl)             # G17 [ÁÀúý] -> c / A_[uû]$  eg وَثَاءٌ

        form_trasl=re.sub('([^َْ])[ءأإؤ](ّ?ِ)$',r'\1ئ\2',form_trasl)         # G18a [cÁÀú] -> ý / [^·a]_~?i$
        
        form_trasl=re.sub('َ[ءأإؤ]ِ$',r'َئِ',form_trasl)                     # G18b [cÁÀú] -> ý / a_i$
        
        form_trasl=re.sub('َ[ءئإؤ]ِّ$',r'َئِّ',form_trasl)                     # G18b [cýÀú] -> Á / a_~i$  
    
        form_trasl=re.sub('(?<=.)[ءأإؤ](?=ّ?ِ.)','ئ',form_trasl)           # G19 [cÁÀú] -> ý / ._~?i[^$]  eg تُنئِيَا

        form_trasl=re.sub('ْ[ءأؤئ]ِ$','ْإِ',form_trasl)                      # G20 [cÁúý] -> À / ·_i$  eg أَصءِ

        form_trasl=re.sub('ِ[ءأإؤ]','ِئ',form_trasl)                       # G7 [cÁÀú] -> ý / i_ eg جَآجِئُ
        
        return(form_trasl)

    except ValueError as verror:
        print('Value error in function Apply_RulesPostTrasl_form(): ' + str(verror))






# This function receives as paremeters a list with a dictionary containing the verbal forms and CODE, lema, root, d_code
# and applyies the phonotactic and orthographic rules returning a list with the surface forms and their CODE.
def Irreg_rules_list(d_form, lema, root, d_code):
    keys=d_form.keys()
    d_norm_f={}
    for k in keys:
        # Sukun and long vowel rules
        form = Sukun_and_Long_vowels_normalization(d_form[k])
        # initial consonant clusters preprocessing
        form = preprocessing_Initial_Alif(form)
        # Weak letters
        form = Apply_WeakLettersRules(form, k, lema, root, d_code)
        # Shadda rules
        form = Apply_ShaddaRules(form, k, lema, root, d_code)
        # initial consonant clusters posprocessing
        form = posprocessing_Initial_Alif(form)
        # Hamza rules
        form = Apply_HamzaRules(form)
        d_norm_f.setdefault(k, form)

    return d_norm_f





# This function receives as paremeters a dictionary with the verbal form, lema, root, d_code
# and applies the phonotactic and orthographic rules returning a dictionary with the surface forms
def phonotactic_rules(dict_form, lema, root, d_code):

    dict_form['VP']= {'Active': Irreg_rules_list(dict_form['VP']['Active'], lema, root, d_code),
                      'Pasive': Irreg_rules_list(dict_form['VP']['Pasive'], lema, root, d_code)}                    
    dict_form['VI']['Active']= {'Indicative': Irreg_rules_list(dict_form['VI']['Active']['Indicative'], lema, root, d_code),
                                'Subjunctive': Irreg_rules_list(dict_form['VI']['Active']['Subjunctive'], lema, root, d_code),
                                'Yusive': Irreg_rules_list(dict_form['VI']['Active']['Yusive'], lema, root, d_code)}
    dict_form['VI']['Pasive']= {'Indicative': Irreg_rules_list(dict_form['VI']['Pasive']['Indicative'], lema, root, d_code),
                                'Subjunctive': Irreg_rules_list(dict_form['VI']['Pasive']['Subjunctive'], lema, root, d_code),
                                'Yusive': Irreg_rules_list(dict_form['VI']['Pasive']['Yusive'], lema, root, d_code)}
    dict_form['VIAM'] = Irreg_rules_list(dict_form['VIAM'], lema, root, d_code)
    
    return(dict_form)
    
   
