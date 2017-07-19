# Retrofitting-Concept-Vector-Representations-of-Medical-Concepts (Published in MedInfo 2017)
Zhiguo Yu, Todd Johnson, Trevor Cohen

The University of Texas School of Biomedical Informatics at Houston, Houston, Texas, USA,

Byron C. Wallace

College of Computer and Information Science, Northeastern University, Boston, Massachusetts, USA,

Estimation of semantic similarity and relatedness between biomedical concepts has utility for many informatics applications. Automated methods fall into two categories: methods based on distributional statistics drawn from text corpora, and methods using the structure of existing knowledge resources. Methods in the former disregard taxonomic structure, while those in the latter fail to consider semantically relevant empirical information. In this work, we present a method that retrofits distributional context vector representations of biomedical concepts using structural information from the UMLS Metathesaurus, such that the similarity between vector representations of linked concepts is augmented. 

We evaluated this approach on the UMNSRS benchmark. Our results demonstrate that retrofitting of concept vector representations leads to better correlation with human raters for both similarity and relatedness, surpassing the best results reported to date. We also demonstrated a clear improvement on the correlation with standards from retrofitted vector representation compared to the vector representation without retrofitting.

Below is an example of this approach.

Pre_requirment: 
1, Python 2.7 working environment (if you are using pyhton 3.0, please change codes accordingly), 2, Concept based word2vector model based on whole PubMed citations (download here: https://www.dropbox.com/s/qdnbs4742x3vsss/w2v-model-PubMed-CUIs-10.bin?dl=0)

Step 1: Download or clone this repository to local computer

Step 2: download CUI based w2v model and save it the current folder

Step 3: Let's set PubMed semantic relationship RN and RO as an example (more information about UMLS Relationship Table finds here: https://www.nlm.nih.gov/research/umls/knowledge_sources/metathesaurus/release/abbreviations.html). We collected all the CUIs from the reference dataset and their one step (RN/RO) related CUIs. We used our concept based w2v model to represent each concept as vector. You can find this file in this folder (cui_vecs_PubMedCUI10_RN_RO.txt) You can build you own vector as your informtion needs. 

Step 4: Retrofit this vector file using semantic lexicons we build (umls_structure_RN_RO.txt). The format of umls_structure_RN_RO.txt like this:  

Line 1: CUI1 CUI2 CUI3 ...
Line 2: CUI4 CUI5 CUI6 ...
...

Each line share the same semantic relationship (RN or RO)

In ther terminal, RUN 

"Python retrofit.py"

A output file named "Re_cui_vecs_PubMedCUI10_RN+RO.txt" will created in the current folder. This is our retrofitted vectors

Step 5: Compare these two results with reference data

RUN "Python test.py"

The output like this:

"Spearman Correlation Coefficient result comparing with reference Set 

*******Similarity*********

Without Retrofitting:  SpearmanrResult(correlation=0.63901547596985031, pvalue=1.0426455553394516e-61)

With Retrofitting RN+RO:  SpearmanrResult(correlation=0.68880357872014775, pvalue=3.1905125515381359e-75)

*********Relatedness********

Without Retrofitting:  SpearmanrResult(correlation=0.58485729932498276, pvalue=3.8574793801766251e-51)

With Retrofitting RN+RO:  SpearmanrResult(correlation=0.61923908588316456, pvalue=8.4545212393655436e-59)
"

Please contact Zhiguo Yu (zhiguoyu1989@gmail.com) or Dr. Cohen (Trevor.Cohen@uth.tmc.edu) for questions or comments.

Also please cite this paper if you find this work useful.
