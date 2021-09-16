# pour cette fiche de mission 
prc_description = test['OF'][76]
prc_description

# charger le modèle Word2Vec
model = Word2Vec.load("sophiemodel.model")

# algo matching

def get_closest(word, n):
    #Cette fonction permet d'obtenir des mots similaires à des phrases...
    word = word.lower()
    words = [word]
    similar_vals = [1]
    try:
        similar_list = model.most_similar(positive=[word],topn=n)
        
        for tupl in similar_list:
            words.append(tupl[0])
            similar_vals.append(tupl[1])
    except:
        
        pass
    
    return words, similar_vals
    
# obtenir des mots simillaire(sémantique) dans la fiche de mission 
word_value = {}
similar_words_needed = 2
for word in prc_description.split():
    similar_words, similarity = get_closest(word, similar_words_needed)
    for i in range(len(similar_words)):
        word_value[similar_words[i]] = word_value.get(similar_words[i], 0)+similarity[i]
        print(similar_words[i], word_value[similar_words[i]])
 
# je charge la base de données CV 
cvs = pd.read_csv('prc_data.csv', sep='\t')
cvs = cvs.set_index('Unnamed: 0')
cvs

import os, math
import pandas as pd
import numpy as np
no_of_cv = 150

####################################""
count = {}
idf = {}
for word in word_value.keys():
    count[word] = 0
    for i in range(no_of_cv):
        try:
            if word in cvs.loc(0)['skill'][i].split() or word in cvs.loc(0)['exp'][i].split():
                count[word] += 1
        except:
            pass
    if (count[word] == 0):
        count[word] = 1
    idf[word] = math.log(no_of_cv/count[word])
print(count)
print(idf)
####################################""

score = {}
for i in range(no_of_cv):
    score[i] = 0
    try:
        for word in word_value.keys():
            tf = cvs.loc(0)['skill'][i].split().count(word) + cvs.loc(0)['exp'][i].split().count(word)
            score[i] += word_value[word]*tf*idf[word]
    except:
        pass
sorted_list = []
for i in range(no_of_cv):
    sorted_list.append((score[i], i))
    
sorted_list.sort(reverse = True)

for s, i in sorted_list:
    #if list(cvs)[i] != '.DS_Store':
        print(list(cvs)[i], ':', s)
