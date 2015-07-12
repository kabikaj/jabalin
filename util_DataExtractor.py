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



def preprocess_lexicons():

    eq_codes={
    '00L0001':'Iau',
    '00L0000':'Iai',
    '00L0002':'Iaa',
    '00L0101':'Iuu',
    '00L0202':'Iia',
    '00L0200':'Iii',
    '20H0010':'II',
    '30H0010':'III',
    '03H0010':'IV',
    '20H1002':'V',
    '30H1002':'VI',
    '01L0000':'VII',
    '02L0000':'VIII',
    '10L0000':'IX',
    '04H0000':'X',
    '15H0000':'XI',
    '56H0000':'XII',
    '07H0000':'XIII',
    '18H0000':'XIV',
    '48H0000':'XV',
    '00H0010':'QI',
    '00H1002':'QII',
    '08H0000':'QIII',
    '10H0000':'QIV',
    }

    ## lexicon lemmas
    with open('lexicon_lemas_jabalin.txt',encoding='utf8') as file,\
         open('lexicon_lemas_procesado.txt','w',encoding='utf8') as outfile:
        for line in file:
            try: l,r,c=line.strip().split()
            except: print(line)
            c=eq_codes[c]
            print(l,r,c, sep='\t' ,file=outfile)


    ## lexicon verbs
    with open('lexiconVerbs_jabalin.txt',encoding='utf8') as file,\
         open('lexiconVerbsPerf_procesado.txt','w',encoding='utf8') as outfileP,\
         open('lexiconVerbsImperf_procesado.txt','w',encoding='utf8') as outfileI:
        for line in file:
            try: f,t,l,r,c=line.strip().split()
            except: print(line)
            c=eq_codes[c]
            if t=='VPAN3SM':
                 print(f,l,r,c, sep='\t' ,file=outfileP)
            if t=='VIAN3SM':
                print(f,l,r,c, sep='\t' ,file=outfileI)

    return()





def saca_root_patterns(length_root):
    'creates a dic with the data in lexicon of lemmas'
    ROOTS={} # dic ROOTS -> v=root; k=[code, code, ...]
    with open('lexicon_lemas_procesado.txt',encoding='utf8') as f:
        for line in f:
            try: l,r,p=line.strip().split()
            except: print(line)
            if length_root==len(r):
                if r in ROOTS: ROOTS[r].append(p)
                else: ROOTS[r]=[p]
    return ROOTS



def freq_dic(dic,total='None'):
    '''takes a dic containing {item : abs_freq}
    creates a dic -> {item : (abs_freq, %_freq)}'''
    FREQ={}
    for k,v in sorted(dic.items(), key=lambda x:x[1], reverse=True):
        if total=='None': FREQ[k]=v
        else: FREQ[k]=(v,float('%.1f' % round(v*100/total,1)))
    return FREQ



def cmp_to_key(mycmp):
    'Convert a cmp= function into a key= function'
    class K(object):
        def __init__(self, obj, *args):
            self.obj = obj
        def __lt__(self, other):
            return mycmp(self.obj, other.obj) < 0
        def __gt__(self, other):
            return mycmp(self.obj, other.obj) > 0
        def __eq__(self, other):
            return mycmp(self.obj, other.obj) == 0
        def __le__(self, other):
            return mycmp(self.obj, other.obj) <= 0
        def __ge__(self, other):
            return mycmp(self.obj, other.obj) >= 0
        def __ne__(self, other):
            return mycmp(self.obj, other.obj) != 0
    return K


def numeric_compare(x, y):
    'sort list by the order defined in the list below'
    orden=['Iau','Iai','Iaa','Iuu','Iia','Iii','II','III','IV','V','VI','VII',
       'VIII','IX','X','XI','XII','XIII','XIV','XV','QI','QII','QIII','QIV']
    return orden.index(x) - orden.index(y)



def printDic_ordenado(Dic):
    '''prints ditionary sorted by pattern order'''
    ##  {IX : {'XIII': (abs, 0.0), ....}, ...}
    orden_patterns_x=sorted(Dic, key=cmp_to_key(numeric_compare))
    for pat_x in orden_patterns_x:
        dict_valores=Dic[pat_x]
        orden_patterns_y=sorted(Dic[pat_x], key=cmp_to_key(numeric_compare))
        for pat_y in orden_patterns_y:
            value_abs=dict_valores[pat_y][0]
            value_frq=dict_valores[pat_y][1]
            print(pat_x, pat_y, value_abs, value_frq, sep='\t')
    return



def saca_perfective_forms(VarForm):
    '''extracts perfective of imperfective forms
    from Jabalín lexicon of inflected verbal forms'''
    VERBS={} # {pat: [form, form, ...], ...}
    if VarForm=='1': input_file='lexiconVerbsPerf_procesado.txt'
    elif VarForm=='2': input_file='lexiconVerbsImperf_procesado.txt'
    with open(input_file,encoding='utf8') as file:
        for line in file:
            try: f,l,r,p=line.strip().split()
            except: print(line)
            VERBS.setdefault(p,[f]).append(f)
    return VERBS






