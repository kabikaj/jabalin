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



#     ________________________________________________________
#    |  ____________________________________________________  |
#    | |                                                    | | 
#    | |  EXTRACTS QUANTITATIVE DATA FROM JABALIN LEXICONS  | | 
#    | |____________________________________________________| | 
#    |________________________________________________________|


#    1   number of roots, verbs and mean pattern per root
#    2   number patterns per root
#    3   freq of patterns
#    4   predicted (expected) freq of pattern co-occurrences
#    5   actual (observed) freq of pattern co-ocurrences
#    6   freq of each radical from a specified list of patterns
#    7   freq of patterns from triliteral roots that meet R2=R3 (biliterals)
#    8   freq each pattern for pat/root=1
#    9   freq of patterns from roots without Form I and QI
#    10  freq of vocalism morphemes
#    11  freq of patterns according to traditional counting of prosody



import util_DataExtractor
import itertools
import re




def quantitativeData():

    print("processing input lexicons.....")
    
    util_DataExtractor.preprocess_lexicons()  ### prepares the lexicons to extract the data

    # dict with each root and its list of codes: {root: [pat, pat, ...]}
    RootsPatsTri=util_DataExtractor.saca_root_patterns(3)   # triliteral
    RootsPatsQua=util_DataExtractor.saca_root_patterns(4)   # quadriliteral

    TotalRootsTri=len(RootsPatsTri)        # number triliteral roots
    TotalRootsQua=len(RootsPatsQua)        # number quadriliteral roots


    #  _______________     _______________  
    # |_______________| 1 |_______________| 


    Lemas_per_rootTri,Lemas_per_rootQua=[],[]   # list with the number of lemmas for each root
    TotalVerbsTri=0; TotalVerbsQua=0            # number of verbs

    for code_lem in RootsPatsTri.values():      # triliteral
        num_verbs_each_root=len(code_lem)
        Lemas_per_rootTri.append(num_verbs_each_root)
        TotalVerbsTri=TotalVerbsTri+num_verbs_each_root

    for code_lem in RootsPatsQua.values():      # quadriliteral
        num_verbs_each_root=len(code_lem)
        Lemas_per_rootQua.append(num_verbs_each_root)
        TotalVerbsQua=TotalVerbsQua+num_verbs_each_root



    #  _______________     _______________  
    # |_______________| 3 |_______________| 


    NumPatTri,NumPatQua={},{}
                    # {root: [pat, pat, ...]}
    for root,codes in RootsPatsTri.items():  # triliteral
        for cod in codes:
            NumPatTri[cod]=NumPatTri.get(cod,0)+1
            ## NumPatTri = {'I':32, 'II':120, ...}

    for root,codes in RootsPatsQua.items():  # quadriliteral
        for cod in codes:
            NumPatQua[cod]=NumPatQua.get(cod,0)+1

    freqPatTri,freqPatQua={},{} # pattern - freq abs - freq per Total roots

    for k,v in util_DataExtractor.freq_dic(NumPatTri,TotalRootsTri).items():
        pat,num,perc=k,v[0],v[1]
        freqPatTri[pat]=(num,perc)

    for k,v in util_DataExtractor.freq_dic(NumPatQua,TotalRootsQua).items():
        pat,num,perc=k,v[0],v[1]
        freqPatQua[pat]=(num,perc)



    #  _______________     _______________
    # |_______________| 4 |_______________| 


    ## EG. FREQ OF COOCURRENCY PATTERNS II AND III
    ##
    ## pattern      abs_freq(no. verbs of this pattern)      rel_freq(over n. total roots)
    ##  II                      1811                                  56.1
    ##  III                     996                                   30.8
    ##
    ## freq relative coocurrence II & III -> (56.1 * 30.8) / 100 = 17.2788
    ## freq absolute coocurrence II & III ->  (17.2788 * 3230{i.e.Total no. Roots}) / 100 = 558


    def PredictCoocur(DicFreq,TotalR):
        
        DicKeys=sorted(list(DicFreq.keys()),key=util_DataExtractor.cmp_to_key(util_DataExtractor.numeric_compare))
        pairs_dic=list(itertools.combinations(sorted(DicKeys,key=util_DataExtractor.cmp_to_key(util_DataExtractor.numeric_compare)),2))
        # in pairs_dic we include a list of all relevant combinations of pattern pairs [('II','III'), ('II','IV'), ...]

        CoocurFreq={}
        for pat in pairs_dic:
            x,y=pat[0],pat[1]

            # we calculate the predicted freq of each pair of patterns
            resul_freq=round((float(DicFreq[x][1])*float(DicFreq[y][1]))/100,2)

            # we calculate how many roots are expected to have those patterns
            resul_abs=int((resul_freq*TotalR)/100)

            value={y:(resul_abs,resul_freq)}
            CoocurFreq.setdefault(x,value).update(value)

        # CoocurFreq -> { X : {'XIII': (1, 0.05), 'XII': (12, 0.39), 'XI': (14, 0.46), 'XV': (0, 0.03)}, ... }
        return CoocurFreq



    #  _______________     _______________  
    # |_______________| 5 |_______________| 


    def ActualCoocur(RootsPats, TotalR):

      # RootsPats = {r: [p,p,p], ...}

        CoocurFreq={}
        for root,patterns in RootsPats.items():
            PairsPats=list(itertools.combinations(sorted(patterns,key=util_DataExtractor.cmp_to_key(util_DataExtractor.numeric_compare)),2))

            # !! PairPats -> there are some cases in which a root has two verbs of the same pattern; one of them is archaic
            for pair in PairsPats:
                x,y=pair[0],pair[1]
                if x in CoocurFreq:
                    if y in CoocurFreq[x]:
                        CoocurFreq[x][y]+=1
                    else:
                        CoocurFreq[x][y]=1
                else: CoocurFreq[x]={y:1}

        for pat1,listafreq in CoocurFreq.items():
            for pat2,fq in listafreq.items():
                CoocurFreq[pat1][pat2]=(fq, round((fq*100)/TotalR,2))

        return CoocurFreq


    ######  future work:
    ######  evaluate statistical significance with chi square-test and G-test
    ######  Chi-test
    ######  G-test



    #  _______________     _______________  
    # |_______________| 6 |_______________| 


    def takes_radical_freqs_from_pats(code,lista_pats):
        'extracts a list of selected roots and gets the frequency data'
        list_target_roots=set()
        with open('lexicon_lemas_procesado.txt', encoding='utf8') as f:
            for line in f:
                try: l,r,c=line.strip().split()
                except: print(line)

                # ========= we define the variables to filter the roots we want to extract the frequencies from =========== #
                       # length of root
                trilit = (code[0]=='1') and (len(r)==3)
                quadrilit = (code[0]=='2') and (len(r)==4)

                       # filter of geminated root                 
                GeminTri = (trilit) and ((code[1]=='2' and r[1]==r[2]) or (code[1]=='1')) #and r[1]!=r[2]))
                GeminQua = (quadrilit) and ((code[1]=='2' and r[0]+r[1]==r[2]+r[3]) or (code[1]=='1' and r[0]+r[1]!=r[2]+r[3]))

                       # filter of patterns
                matching_Pat = (code[2]=='1') or ((code[2]=='2') and (c in lista_pats))
                # ========================================================================================================== #

                if matching_Pat and (GeminTri or GeminQua):
                    list_target_roots.add(r)   # LIST OF TARGET ROOTS

        list_target_roots=list(list_target_roots)  # converts the set into a list
        total_Roots=len(list_target_roots)         # total number of roots
        RadicalsFreq=[]                            # list to insert the frequencies

        if len(list_target_roots[0])==3:
            length_root=3
            Radicals = [{},{},{}]      # triliteral roots
        else:
            length_root=4
            Radicals = [{},{},{},{}]   # quadriliteral roots
        
        for raiz in list_target_roots: # go through the list of roots
            i=0
            for r in raiz:     # takes each of the char from the root
                Radicals[i][r]=Radicals[i].get(r,0)+1
                i+=1
        Aux=[]
        for rad in Radicals:
            Aux.append(util_DataExtractor.freq_dic(rad,total_Roots))
        RadicalsFreq.append(Aux)

        return RadicalsFreq, total_Roots, length_root



    def print_freqs(lista_freqR, total_R, length_root): # tri y qua
        print('\ttotal: %d\n' % (total_R))

        if length_root==3:
            print('Char\tR1abs\tR1%\tR2abs\tR2%\tR3abs\tR3%')
            for item in lista_freqR:
                R1,R2,R3=item[0],item[1],item[2]
                for cons,freq in R1.items():
                    r1abs,r1fq=freq[0],freq[1]

                    if cons in R2: r2abs,r2fq=R2[cons][0],R2[cons][1]
                    else: r2abs,r2fq=0,0

                    if cons in R3: r3abs,r3fq=R3[cons][0],R3[cons][1]
                    else: r3abs,r3fq=0,0
                        
                    print(cons,r1abs,r1fq,r2abs,r2fq,r3abs,r3fq,sep='\t')

        elif length_root==4:
            print('Char\tR1abs\tR1%\tR2abs\tR2%\tR3abs\tR3%\tR4abs\tR4%')
            for item in lista_freqR:
                R1,R2,R3,R4=item[0],item[1],item[2],item[3]
                for cons,freq in R1.items():
                    r1abs,r1fq=freq[0],freq[1]

                    if cons in R2: r2abs,r2fq=R2[cons][0],R2[cons][1]
                    else: r2abs,r2fq=0,0

                    if cons in R3: r3abs,r3fq=R3[cons][0],R3[cons][1]
                    else: r3abs,r3fq=0,0

                    if cons in R4: r4abs,r4fq=R4[cons][0],R4[cons][1]
                    else: r4abs,r4fq=0,0
                    
                    print(cons,r1abs,r1fq,r2abs,r2fq,r3abs,r3fq,r4abs,r4fq,sep='\t')
                    
        return




    #  _______________     _______________  
    # |_______________| 7 |_______________| 



    def calculateBilitFreq(RootsPats, num_radicals):
        BilitFreq={}  # just patterns from biliteral root -> {pat: abs}

        if num_radicals=='3':
            for root,patterns in RootsPats.items():
                if root[1]==root[2]:
                    for pat in patterns:
                        BilitFreq[pat]=BilitFreq.get(pat,0)+1
            return BilitFreq

        elif num_radicals=='4':
            for root,patterns in RootsPats.items():
                if root[0]+root[1]==root[2]+root[3]:
                    for pat in patterns:
                        BilitFreq[pat]=BilitFreq.get(pat,0)+1
            return BilitFreq
        

    #  _______________        _______________  
    # |_______________| 8, 9 |_______________| 


    RootsPatsBoth=RootsPatsTri
    RootsPatsBoth.update(RootsPatsQua)


    def WithoutPatternI_OneRPatPerRoot(RootsPats):
        '''it does two things:
        extracts freq of patterns with one pattern per root
        and extracts freq of patterns without pattern I'''

        freqOnePat_per_root={}        # pattern per root Ratio = 1
        freqMultipleTri,freqTri={},{} # triliteral
        freqMultipleQua,freqQua={},{} # quadriliteral

        for Root,Patterns in RootsPats.items():
            Patterns=sorted(Patterns, key=util_DataExtractor.cmp_to_key(util_DataExtractor.numeric_compare))
            Patterns=list(map((lambda p: re.sub('^I[aiu]{2}','I',p)), Patterns))

            # freq pattern that meet pat/root=1
            if len(Patterns)==1:
                for pat in Patterns:
                    freqOnePat_per_root[pat]=freqOnePat_per_root.get(pat,0)+1

            # freq pattern from triliteral root with no form I
            if 'I' not in Patterns and len(Root)==3:
                # no. patterns from TriRoots without Form I
                for pat in Patterns:
                    freqTri[pat]=freqTri.get(pat,0)+1
                    
                    # freq pattern combinations from TriRoots without
                    # Form I and more than one single pattern
                    if len(Patterns)>1:
                        pat=' - '.join(Patterns)
                        freqMultipleTri[pat]=freqMultipleTri.get(pat,0)+1

            # freq pattern from quadriliteral root with no form QI
            elif 'QI' not in Patterns and len(Root)==4:
                    # no. patterns from QuaRoots without Form QI
                    for pat in Patterns:
                        freqQua[pat]=freqQua.get(pat,0)+1
                    
                    # no. pattern combinations from QuaRoots without Form QI
                    # and more than one single pattern
                    if len(Patterns)>1:
                        pat=' - '.join(Patterns)
                        freqMultipleQua[pat]=freqMultipleQua.get(pat,0)+1

        return freqOnePat_per_root, freqTri, freqMultipleTri, freqQua, freqMultipleQua
        


    #  _______________      _______________  
    # |_______________| 10 |_______________| 



    def freqVocalismOneGroup(RootsPats):

        '''Patterns             Vocalism

         Iau                     aa-au
         Iai,VII-XV,QIII,QIV     aa-ai
         Iuu                     au-au
         Iia                     ai-aa
         II,III,IV,QI            aa-ui
         Iaa,V,VI,QII            aa-aa
         Iii                     ai-ai'''

        FreqVoc={}
        for patterns in RootsPats.values():
            for pat in patterns:
                
                if pat=='Iau':
                    FreqVoc['aa-au']=FreqVoc.get('aa-au',0)+1
            
                elif pat in ['Iai','VII','VIII','IX','X','XI','XII',\
                             'XIII','XIV','XV','QIII','QIV']:
                    FreqVoc['aa-ai']=FreqVoc.get('aa-ai',0)+1
                             
                elif pat=='Iuu':
                    FreqVoc['au-au']=FreqVoc.get('au-au',0)+1
                             
                elif pat=='Iia':
                    FreqVoc['ai-aa']=FreqVoc.get('ai-aa',0)+1
                             
                elif pat in ['II','III','IV','QI']:
                    FreqVoc['aa-ui']=FreqVoc.get('aa-ui',0)+1
                             
                elif pat in ['Iaa','V','VI','QII']:
                    FreqVoc['aa-aa']=FreqVoc.get('aa-aa',0)+1

                elif pat=='Iii':
                    FreqVoc['ai-ai']=FreqVoc.get('ai-ai',0)+1

                else:
                    print('fail in pattern: %s' % pat)
                    
        TotalVoc=0
        for i in FreqVoc.values(): TotalVoc=TotalVoc+i

        return FreqVoc, TotalVoc




    def freqVocalismSeparated(RootsPats):

        ''' Perfective

                Patterns                                                Vocalism
                  Iau,Iai,VII-XV,QIII,QIV,II,III,IV,QI,Iaa,V,VI,QII         aa
                  Iuu                                                       au
                  Iia,Iii                                                   ai  
            
            Imperfective
            
                Patterns             Vocalism
       
                  Iau,Iuu                     au
                  Iai,VII-XV,QIII,QIV,Iii     ai
                  Iia,Iaa,V,VI,QII            aa
                  II,III,IV,QI                ui'''
        

        FreqVocP,FreqVocI={},{}
        for patterns in RootsPatsBoth.values():
            for pat in patterns:

                # perfective vocalism
                if pat in ['Iau','Iai','VII','VIII','IX','X','XI','XII','XIII','XIV',\
                           'XV','QIII','QIV','II','III','IV','QI','Iaa','V','VI','QII']:
                    FreqVocP['aa']=FreqVocP.get('aa',0)+1
                elif pat == 'Iuu':
                    FreqVocP['au']=FreqVocP.get('au',0)+1
                elif pat in  ['Iia','Iii']:
                    FreqVocP['ai']=FreqVocP.get('ai',0)+1
                else:
                    print('fail in pattern (perfective): %s' % pat)

                # imperfective vocalism
                if pat in ['Iau','Iuu']:
                    FreqVocI['au']=FreqVocI.get('au',0)+1
                elif pat in ['Iai','VII','VIII','IX','X','XI','XII','XIII','XIV','XV','QIII','QIV','Iii']:
                    FreqVocI['ai']=FreqVocI.get('ai',0)+1
                elif pat in ['Iia','Iaa','V','VI','QII']:
                    FreqVocI['aa']=FreqVocI.get('aa',0)+1
                elif pat in ['II','III','IV','QI']:
                    FreqVocI['ui']=FreqVocI.get('ui',0)+1
                else:
                    print('fail in pattern (imperfective): %s' % pat)
                    
        TotalVocP,TotalVocI=0,0
        for i in FreqVocP.values(): TotalVocP=TotalVocP+i
        for i in FreqVocI.values(): TotalVocI=TotalVocI+i

        return FreqVocP, TotalVocP, FreqVocI, TotalVocI



    #  _______________      _______________  
    # |_______________| 11 |_______________| 


    def traditional_counting(VarForm):
        
        PerfectiveForms = util_DataExtractor.saca_perfective_forms(VarForm)  # {pat: [form, form, ...], ...}
        FreqProsody={}
        
        for pat,forms in PerfectiveForms.items():
            
            for f in forms:
                input_f = f                  # for checking errors in forms
                
                f=f.replace('آ','أَا')        # madda normalization
                f=re.sub(r'(.)ّ',r'\1ْ\1',f)   # shadda normalization
        
                f = re.sub('.ْ','0',f)        # Convert SAKIN letter into 0
                for s in ['ا','و','ي','ى']:  # Convert MAMDOOD letter into 0
                    f = re.sub(s,'0',f)    
                f = re.sub('.[َُِ]','1',f)      # Convert MUTAHARRIK letter into 1

                if not re.search('[^10]',f):

                    # traditional accumulative counting conversion
                    f = re.sub('10','2',f)
                    f = re.sub('12','3',f)
                    f = re.sub('22','4',f)
                    
                    # calculate total weight
                    n=sum(list(map(int,list(f))))

                    # convert into syllabic weight
                    f = re.sub('4','HH',f)   ## 1010 = 22 = 4 = HH
                    f = re.sub('3','LH',f)   ## 110  = 12 = 3 = LH
                    f = re.sub('2','H',f)    ## 10   = 10 = 2 = H
                    f = re.sub('1','L',f)    ## 1    = 1  = 1 = L

                    f = re.sub('H0','SH',f)  ## [H0 = SH] // SH computa lo mismo que H

                else: print('Error in form: %s\tinput form: %s' % (f, input_f))

                # pattern   total   forma_Prosody   freq_abs
                # {(pat,n,f):freq, ...}
                FreqProsody[(pat,n,f)]=FreqProsody.get((pat,n,f),0)+1
                    
        return FreqProsody




    # ****************************************************************************** 

     
    salir = False
    while salir==False:
        option=input('''
    ________________________________________\n
        WRITE NUMBER OF SELECTED OPTION\n\n
        1\tnumber of roots, verbs and mean pattern per root\n
        2\tnumber patterns per root\n
        3\tfreq of patterns\n
        4\tpredicted (expected) freq of pattern co-occurrences\n
        5\tactual (observed) freq of pattern co-ocurrences\n
        6\tfreq of each radical from a specified list of patterns\n
        7\tfreq of patterns from triliteral roots that meet R2=R3 (biliterals)\n
        8\tfreq of each pattern for pat/root=1\n
        9\tfreq of patterns from roots without Form I\n
        10\tfreq of vocalism morphemes\n
        11\tfreq of patterns according to traditional counting of prosody\n
        0\texit\n
    ________________________________________\n''')


        if option == '0': salir=True

        


        elif option == '1':
            print('\nNUMBER OF ROOTS, VERBS AND MEAN PATTERNS PER ROOT')
            print('\ntriliteral roots: %d' % TotalRootsTri)
            print('triliteral verbs: %d' % TotalVerbsTri)
            print('pattern/triliteral root: %.2f\n' % round(TotalVerbsTri/TotalRootsTri,2))

            print('quadriliteral roots: %d' % TotalRootsQua)
            print('quadriliteral verbs: %d' % TotalVerbsQua)
            print('pattern/quadriliteral root: %.2f\n' % round(TotalVerbsQua/TotalRootsQua,2))




        elif option == '2':
            print('\n2. number patterns per root')
            pats_per_rootTri,pats_per_rootQua={},{}

            for i in Lemas_per_rootTri: pats_per_rootTri[i]=pats_per_rootTri.get(i,0)+1  # triliteral
            print('\nPatterns\tNo. TriRoots\t%\n')
            for k,v in util_DataExtractor.freq_dic(pats_per_rootTri,TotalRootsTri).items():
                print(str(k).ljust(15),str(v[0]).ljust(15),v[1])

            for i in Lemas_per_rootQua: pats_per_rootQua[i]=pats_per_rootQua.get(i,0)+1  # quadriliteral
            print('\n\nPatterns\tNo. QuaRoots\t%\n')
            for k,v in util_DataExtractor.freq_dic(pats_per_rootQua,TotalRootsQua).items():
                print(str(k).ljust(15),str(v[0]).ljust(15),v[1])




        elif option == '3':
            print('\nPat\tFreq\t% TriRoots\n')
            DicKeys=sorted(list(freqPatTri.keys()),key=util_DataExtractor.cmp_to_key(util_DataExtractor.numeric_compare))
            for p in DicKeys:
                print(p.ljust(7),str(freqPatTri[p][0]).ljust(7),str(freqPatTri[p][1]))

            
            print('\n\nPat\tFreq\t% QuaRoots\n')
            DicKeys=sorted(list(freqPatQua.keys()),key=util_DataExtractor.cmp_to_key(util_DataExtractor.numeric_compare))
            for p in DicKeys:
                print(p.ljust(7),str(freqPatQua[p][0]).ljust(7),str(freqPatQua[p][1]))




        elif option == '4':
            print('\npredicted freqs for Triliteral pattern co-occurrences\n')
            PredCoocurFqTri=PredictCoocur(freqPatTri,TotalRootsTri)    # gets predicted freqs
            util_DataExtractor.printDic_ordenado(PredCoocurFqTri)               # prints predicted freqs
            print('\npredicted freqs for Quadriliteral pattern co-occurrences\n')
            PredCoocurFqQua=PredictCoocur(freqPatQua,TotalRootsQua)    # gets predicted freqs
            util_DataExtractor.printDic_ordenado(PredCoocurFqQua)               # prints predicted freqs




        elif option == '5':
            print('\nactual freqs for Triliteral pattern co-occurrences\n')
            ActualCoocurFqTri=ActualCoocur(RootsPatsTri,TotalRootsTri)   # gets predicted freqs
            util_DataExtractor.printDic_ordenado(ActualCoocurFqTri)               # prints predicted freqs
            print('\nactual freqs for Quadriliteral pattern co-occurrences\n')
            ActualCoocurFqQua=ActualCoocur(RootsPatsQua,TotalRootsQua)   # gets predicted freqs
            util_DataExtractor.printDic_ordenado(ActualCoocurFqQua)               # prints predicted freqs


     

        elif option == '6':
                # var_length:  tri=1         /  qua=2
                # var_gemin:   no_especif=1  /  yes=2
                # var_pat:     all=1         /  select=2  ->  var_pat_list: [list of patterns]
                var_length=input('write 1 for triliteral roots or 2 for quadriliteral:\n')
                var_gemin=input('write 1 all times of roots and 2 for geminated roots:\n')
                var_pat=input('write 1 for all patterns or 2 if you want to specify the patterns:\n')
                if var_pat.strip()=='2': var_list_pat=input('write the pattern(s) separated by spaces:\n').strip().split()
                elif var_pat.strip()=='1': var_list_pat=[]
                           # 3-digit code with info: lenghth of root / filter of patterns / filter of consonants
                code_filter=var_length+var_gemin+var_pat
                           # apply function that extracts the root list and its freq
                radic_freqs, radic_total, length_r = takes_radical_freqs_from_pats(code_filter,var_list_pat)
                           # prints the frequency data
                print_freqs(radic_freqs, radic_total, length_r)




        elif option == '7':
            print('\nPattern freq from triliteral roots that meet R2=R3\n')
            BilitFreq=calculateBilitFreq(RootsPatsTri,'3')
            DicKeys=sorted(list(BilitFreq.keys()),key=util_DataExtractor.cmp_to_key(util_DataExtractor.numeric_compare))
            for p in DicKeys:
                print(p,BilitFreq[p],sep='\t')

            print('\nPattern freq from quadriliteral roots that meet R1+R2=R3+R4\n')    
            BilitFreq=calculateBilitFreq(RootsPatsQua,'4')
            DicKeys=sorted(list(BilitFreq.keys()),key=util_DataExtractor.cmp_to_key(util_DataExtractor.numeric_compare))
            for p in DicKeys:
                print(p,BilitFreq[p],sep='\t')


            
        elif option == '8':
            print('\nfreq each pattern for pat/root=1\n')
            freqOnePat_per_root = WithoutPatternI_OneRPatPerRoot(RootsPatsBoth)[0]
            for k,v in util_DataExtractor.freq_dic(freqOnePat_per_root).items(): print(k.ljust(23),v)




        elif option == '9':

            freqOnePat_per_root, freqTri, freqMultipleTri, freqQua, freqMultipleQua = WithoutPatternI_OneRPatPerRoot(RootsPatsBoth)
            
            print('\nfreq pats of roots without Form I\n')
            for k,v in util_dataEctractor.freq_dic(freqTri).items(): print(k.ljust(23),v)

            print('\nfreq multiple patterns of roots without Form I for pat/TriRoot>1\n')
            for k,v in util_DataExtractor.freq_dic(freqMultipleTri).items(): print(k.ljust(34),v)

            print('\nfreq pats of roots without Form QI\n')
            for k,v in util_DataExtractor.freq_dic(freqQua).items(): print(k.ljust(23),v)

            print('\nfreq multiple patterns of roots without Form QI for pat/QuaRoot>1\n')
            for k,v in util_DataExtractor.freq_dic(freqMultipleQua).items(): print(k.ljust(34),v)




        elif option == '10':

            VarVocalism = input('write 1 if you want to calculate the frequencies for perfective and imperfective vocalism together, write 2 if separatedly\n')

            if VarVocalism == '1':
                FreqVoc, TotalVoc = freqVocalismOneGroup(RootsPatsBoth)
                print('vocal\tlemas\tfreq\n')
                for k,v in FreqVoc.items():
                    freq=round(v*100/TotalVoc,1)
                    print(k,v,freq,sep='\t')
                print('\ntotal: %d' % TotalVoc)

            elif VarVocalism == '2':
                FreqVocP, TotalVocP, FreqVocI, TotalVocI = freqVocalismSeparated(RootsPatsBoth)
                print('\nPerfective\nvocal\tlemas\tfreq\n')
                for k,v in FreqVocP.items():
                    freq=round(v*100/TotalVocP,1)
                    print(k,v,freq,sep='\t')
                print('\ntotal: %d' % TotalVocP)

                print('\n\nImperfective\nvocal\tlemas\tfreq\n')
                for k,v in FreqVocI.items():
                    freq=round(v*100/TotalVocI,1)
                    print(k,v,freq,sep='\t')
                print('\ntotal: %d' % TotalVocI)
        



        
        elif option == '11':
            FormToCount=input('Write 1 if you want to apply counting to perfective form, and 2 for imperfective\n')
            FreqProsody = traditional_counting(FormToCount)  # {(pat,n,f):freq, ...}
            print('\n\nPattern'.ljust(11),'TotalWeight'.ljust(12),'SylStructure'.ljust(15),'freq')
            DicKeys=sorted(set([i[0] for i in FreqProsody.keys()]),key=util_DataExtractor.cmp_to_key(util_DataExtractor.numeric_compare))
            orden_previous=''  ## we store the previous pattern to know when the pattern changes, so we can print a new line (for a clearer visualization)
            for orden in DicKeys:
                if orden!=orden_previous: print('') # prints a new line
                orden_previous=orden
                for k,v in FreqProsody.items():
                    pat,total,syl,freq=k[0],k[1],k[2],v
                    if pat==orden:
                        print(pat.ljust(12),str(total).ljust(12),syl.ljust(12),freq)


    return


# ============ funciton call ============ #

quantitativeData()

# ======================================= #
