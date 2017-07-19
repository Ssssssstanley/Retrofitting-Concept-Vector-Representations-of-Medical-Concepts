#####
from sklearn.metrics.pairwise import cosine_similarity
import gensim
import numpy as np
import scipy.stats
import math
def get_cui_vecs(fname):
    cui_vecs={}
    for line in open(fname,'r'):
        line = line.strip().split()
        val = map(lambda x:float(x),line[1:])
        cui_vecs[line[0]]=val
    return cui_vecs

def cosine(M1,M2):
    nor = sum([a*b for a, b in zip(M1, M2)])
    denor = math.sqrt(sum([math.pow(i,2) for i in M1]))*math.sqrt(sum([math.pow(j,2) for j in M2]))
    return (nor*1.0)/denor


def main():
    '''cui_sem={}
    for line in open('semantic_type.txt','r'):
        line0 = line.strip()[:8]
        line1 = line.strip()[9:]
        
        if line1=='Disease or Syndrome':
            cui_sem[line0.lower()]='disorder'
        elif line1=='Sign or Symptom':
            cui_sem[line0.lower()]='symptom'
        else:
            cui_sem[line0.lower()]='drug'
    '''
                
    #lexs= ['CHD','PAR','SIB','SY','AQ','RB','RL','RN','RO','RQ','RU','QB','XR']
    lexs=['RN+RO']
    for lex in lexs:
        print lex
        fname1='./Re_cui_vecs_PubMedCUI10_'+lex+'.txt'
        fname2='./cui_vecs_PubMedCUI10_'+lex+'.txt'
        re_cui_vecs=get_cui_vecs(fname1)
        cui_vecs=get_cui_vecs(fname2)
        '''vec1 = cui_vecs['c0878544']
        vec2= cui_vecs['c0039070']
        print cosine(vec1, vec2)
        exit()'''

        rates_relatedness=[]
        #rates_relatedness2=[]
        re_relatedness1=[]
        #re_relatedness2=[]
        re_re_w2v=[]
        #re_cui_vecs = cui_vecs
        print ""
        model = gensim.models.Word2Vec.load_word2vec_format('./w2v-model-PubMed-CUIs-10.bin', binary=True)
        #print model.similarity('C0008350','C0006277')
        #print len(model['C0008350'])
        #exit()
        ## Di-Di
        
        with open('./Test_Set/UMNSRSrelatedness_mod.sv','r') as f:
            next(f)
            c1=0
            c2=0
            c3=0
            cs=0
            for line in f:
                c1+=1
                line = line.strip().split()
                line = map(lambda x:x.lower(), line)
                try:
                    if line[0] in re_cui_vecs and line[1] in re_cui_vecs:
                        c2+=1
                        rates_relatedness.append(float(line[2]))
                        re_relatedness1.append(cosine(re_cui_vecs[line[0]], re_cui_vecs[line[1]]))
                        #print cosine(re_cui_vecs[line[0]], re_cui_vecs[line[1]])
                        #print line[2]
                        '''if (cui_sem[line[0]]=='disorder' and cui_sem[line[1]]=='disorder')or(cui_sem[line[1]]=='disorder' and cui_sem[line[0]]=='disorder'):
                            cs +=1
                            rates_relatedness2.append(float(line[2]))
                            re_relatedness2.append(cosine_similarity(np.asarray(re_cui_vecs[line[0]]).reshape(1,-1),np.asarray(re_cui_vecs[line[1]]).reshape(1,-1))[0][0])'''
                        re_re_w2v.append(model.similarity(line[0].upper(),line[1].upper()))
                except:
                    c3 +=1
                    pass
        print c1, c2, c3, cs
        rates_similarity=[]
        #rates_similarity2=[]
        re_similarity1=[]
        #re_similarity2=[]
        re_si_w2v=[]
        #f = open('./test_result_sim.txt','w')
        with open('./Test_Set/UMNSRSsimilarity_mod.sv','r') as f1:
            next(f1)
            c1, c2, c3, cs = 0,0,0,0
            for line in f1:
                line = line.strip().split()
                line = map(lambda x:x.lower(), line)
                c1 +=1
                try:
                    if line[0] in re_cui_vecs and line[1] in re_cui_vecs:
                        c2 +=1
                        rates_similarity.append(float(line[2]))
                        re_similarity1.append(cosine(re_cui_vecs[line[0]], re_cui_vecs[line[1]]))
                        '''if (cui_sem[line[0]]=='disorder' and cui_sem[line[1]]=='disorder')or(cui_sem[line[1]]=='disorder' and cui_sem[line[0]]=='disorder'):
                            cs +=1
                            rates_similarity2.append(float(line[2]))
                            re_similarity2.append(cosine_similarity(np.asarray(re_cui_vecs[line[0]]).reshape(1,-1),np.asarray(re_cui_vecs[line[1]]).reshape(1,-1))[0][0])'''
                        
                        re_si_w2v.append(model.similarity(line[0].upper(),line[1].upper()))
                        #print cosine(re_cui_vecs[line[0]], re_cui_vecs[line[1]]), line[2]
                        #f.writelines(str(cosine(re_cui_vecs[line[0]], re_cui_vecs[line[1]]))+','+str(line[2])+'.\n')
                except:
                    c3 +=1
                    pass

        print c1, c2, c3, cs

        #print re_similarity1

        #print rates_similarity
        ### similarity
        print "Spearman Correlation Coefficient result comparing with reference Set "
        print '*******Similarity*********'
        rates_similarity = np.asarray(rates_similarity)
        re_similarity1 = np.asarray(re_similarity1)
        #re_similarity2 = np.asarray(re_similarity2)
        re_si_w2v= np.asarray(re_si_w2v)
        
        #print scipy.stats.spearmanr(rates_similarity1, re_similarity2)
        print "Without Retrofitting:  " + str(scipy.stats.spearmanr(rates_similarity, re_si_w2v))
        print 
        print "With Retrofitting "+lex+ ":  " +str(scipy.stats.spearmanr(rates_similarity, re_similarity1))

        ### relatedness
        print '*********Relatedness********'
        rates_relatedness = np.asarray(rates_relatedness)
        re_relatedness1 = np.asarray(re_relatedness1)
        #re_relatedness2 = np.asarray(re_relatedness2)
        re_re_w2v=np.asarray(re_re_w2v)
        
        #print scipy.stats.spearmanr(rates_relatedness2, re_relatedness2)
        print "Without Retrofitting:  " +str(scipy.stats.spearmanr(rates_relatedness, re_re_w2v))
        print
        print "With Retrofitting "+lex+ ":  " +str(scipy.stats.spearmanr(rates_relatedness, re_relatedness1))
    
                
main()            
    
    





