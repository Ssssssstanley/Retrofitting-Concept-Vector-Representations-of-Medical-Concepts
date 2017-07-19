#### get all unique cuis

import gensim
import csv

def get_all_cuis():
    f = open('./Test_Set/all_cuis_modified.txt','w')
    cuis=[]
    c=0
    with open('./Test_Set/UMNSRSrelatedness_modified.txt','r') as f1:
        next(f1)
        for line in f1:
            c+=1
            line = line.strip().split('\t')
            cuis.append(line[0])
            cuis.append(line[1])
    #print c
    with open('./Test_Set/UMNSRSsimilarity_modified.txt','r')as f2:
        next(f2)
        for line in f2:
            c+=1
            line = line.strip().split('\t')
            cuis.append(line[0])
            cuis.append(line[1])
    #print c
    for cui in set(cuis):
        f.writelines('\''+cui+'\',\n')
    #print len(set(cuis))
    return list(set(cuis))

def transform_csv2txt():
    f1 = open('UMNSRSrelatedness_modified.txt','w')
    f1.writelines('CUI1'+'\t'+'CUI2'+'\t'+'Mean'+'\n')
    f2 = open('UMNSRSsimilarity_modified.txt','w')
    f2.writelines('CUI1'+'\t'+'CUI2'+'\t'+'Mean'+'\n')
    with open('UMNSRS_relatedness_modified_word2vec.csv', 'rU') as csvfile1:
        reader1 = csv.DictReader(csvfile1)
        for row in reader1:
            f1.writelines(row['CUI1']+'\t'+row['CUI2']+'\t'+row['Mean']+'\n')
    with open('UMNSRS_similarity_modified_word2vec.csv', 'rU') as csvfile2:
        reader2 = csv.DictReader(csvfile2)
        for row in reader2:
            f2.writelines(row['CUI1']+'\t'+row['CUI2']+'\t'+row['Mean']+'\n')
    return 

def transform_2txt():
    f1 = open('UMNSRSrelatedness_all.txt','w')
    f1.writelines('CUI1'+'\t'+'CUI2'+'\t'+'Mean'+'\n')
    f2 = open('UMNSRSsimilarity_all.txt','w')
    f2.writelines('CUI1'+'\t'+'CUI2'+'\t'+'Mean'+'\n')
    
    with open('UMNSRSsimilarity_mod.sv','r') as f:
        next(f)
        for line in f:
            line = line.strip().split(',')
            f2.writelines(line[4]+'\t'+line[5]+'\t'+line[0]+'\n')
    with open('UMNSRSrelatedness_mod.sv','r') as f:
        next(f)
        for line in f:
            line = line.strip().split(',')
            f1.writelines(line[4]+'\t'+line[5]+'\t'+line[0]+'\n')
    return 
    
    
    
def prepare_lexicon(lex):
    f = open('./Test_Set/umls_structure_'+lex+'.txt','w')
    cui_lexs={}
    all_cuis=[]
    lexs = lex.split('+')
    with open('./Semantic_Lexicons/all_cuis_one_step_relation.txt','r') as f1:
        next(f1)
        for line in f1:
            line=line.strip().split('\t')
            for l in lexs:
                if line[0]==l:#or line[0]=='RN' or line[0]=='RO' or line[0]=='RQ' or line[0]=='RB' or line[0]=='CHD':
                #if line[0]=='RQ' or line[0]=='RO': #or line[0]=='RN' or line[0]=='RQ' or line[0]=='RO':
                #if line[0]=='RN' or line[0]=='RQ' or line[0]=='RO':
                    all_cuis.append(line[1])
                    all_cuis.append(line[3])
                    if line[1] in cui_lexs:
                        cui_lexs[line[1]].append(line[3])
                    else:
                        cui_lexs[line[1]]=[line[3]]
                    break
    for key in cui_lexs:
        f.writelines(key+' '+' '.join(cui_lexs[key])+'\n')
    print len(cui_lexs)
    
    return list(set(all_cuis))

def preparevec(cuis1, cuis2, lex):
    print len(cuis1)
    print len(cuis2)
    cuis = list(set(cuis1+cuis2))
    cuis_index={}    
    for cui in cuis:
        cuis_index[cui.lower()]=0    
    print len(cuis)
    model = gensim.models.Word2Vec.load_word2vec_format('w2v-model-PubMed-CUIs-10.bin', binary=True)
    #print model['C0015397']
    #exit()
    f1 = open('./cui_vecs_PubMedCUI10_'+lex+'.txt','w')
    c=0
    c1 = 0
    for cui in cuis_index:
        c +=1
        try:    
            data= list(model[cui.upper()])
            data = map(lambda x:str(x), data)
            f1.writelines(cui+' ')
            f1.writelines(' '.join(data)+'\n')
            #print cui
        except:
            c1 +=1
            pass
    print c, c1
    
    #f2 = open('./all_cuis_vectors.txt','w')
    #with open('./embeddingvectors.txt','r') as f:
    '''    next(f)
        for line in f:
            #f2.writelines(line.replace('|',' '))
            line = line.strip().split('|')
            if line[0] in cuis_index:
                if cuis_index[line[0]]==0:
                    cuis_index[line[0]]=1
                    f1.writelines(line[0]+' '+' '.join(line[1:])+'\n')
                    c+=1
                    if c%100==0:
                        print c
    print c
    cc=0
    for item in cuis_index:
        if cuis_index[item]==0:
            cc+=1
    print cc   ''' 
    



#lexs= ['CHD','PAR','SIB','SY','AQ','RB','RL','RN','RO','RQ','RU','QB','XR']
#lexs=['CHD+SY','RQ+RO','RN+RQ','RN+RO','RN+RO+RQ','SY+RN+RO+RQ','CHD+SY+RN+RO+RQ']
lexs=['RN+RO']
for lex in lexs:
    print "Get all CUIs in the refernce set"
    cui1=get_all_cuis()
    #print cui1
    print "Get all CUIs from one step semantic relationship: "+ lex
    cui2=prepare_lexicon(lex)
    #print cui2
    
    print "get all unqiue CUIs vector representation ready for retrofitting"
    preparevec(cui1,cui2,lex)
