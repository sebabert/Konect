import numpy as np 
import pandas as pd 
import string
import nltk
from nltk.corpus import stopwords
from gensim.models import Word2Vec
from gensim.models.phrases import Phrases, Phraser

#je charge les données 

data_oft.to_csv("data_algo.csv", index=False)
test = data_oft.dropna()
print("\n ** brut data **\n")
print(test.head())
print("\n ** data shape **\n")
print(test.shape)

# nettoyage des données 

test['OF'] = test['OF'].apply(lambda x: " ".join(x.lower()for x in x.split()))
## supprimer tabulation and ponctuation
test['OF'] = test['OF'].str.replace('[^\w\s]',' ')
## chiffres
test['OF'] = test['OF'].str.replace('\d+', '')

#supprime stop words
stop = stopwords.words('french')
test['OF'] = test['OF'].apply(lambda x: " ".join(x for x in x.split() if x not in stop))


other_stop_words = ['quipe', 'qualit','experience','mission','client','projet','conception','participer',
                    'rience','application','technique','connaissance','exp','velopper','dõun','tant','dõana',
                   ' recherch', 'ee','lõ','veloppeur','dõune','dõautres','dõau','ætre','dõexp','lõensemble',
                   'op','syst','programming','veloppement','jee','spring','code','ing','el','an','etc','mener','impliqu','bon',
                    'chez','websphere','indispensables','dot','management','fran','construire','partir','disposez','renforcer',
                    'fonctions','impl','significative','rement','produit','composants','micro','issu','donn','lioration',
                   'javaee','gion','gradleé','gité','volu','developpe','dõinvestissement','outils','nieur','mod','é''création',
                    'p','comp tences','v','si','b','re','entreprise','u','afin','h','f','e','o','sou','a','i','flux',
                   'métier','domaines','comp', 'tences','pr','comp tences','ritable','g','ion','tier','appr','diff','faire',
                   'tous','vers','ainsi','plus','concur','via','confi','r','li','bonnes','documentation','rapport','matiques']

 
test['OF'] = test['OF'].apply(lambda x: " ".join(x for x in x.split() if x not in other_stop_words))

## lemmatization
test['OF'] = test['OF'].apply(lambda x: " ".join([Word(word).lemmatize() for word in x.split()]))

print("Preprocessed data: \n")
print(test.head())

# nombre de phrase
sent = [row for row in test['OF']]
len_count = []
for l in sent:
    #print(l)
    len_count.append(len(l))

print("Totale nombre de ligne : ", len(len_count))

# Tokenization pour chaque phrase
token_sent = [doc.split(" ") for doc in sent]
# Configurer les phrase pour bigram
bigram = Phrases(token_sent, min_count=20, threshold=2,delimiter=b' ')

# Intialialise phrase pour bigrame
bigram_phraser = Phraser(bigram)

# Extraire bigrams pour gensim word2vec
bigram_token = []
for sen in token_sent:
    bigram_token.append(bigram_phraser[sen])

word_freq = defaultdict(int)
for sen in bigram_token:
    for i in sen:
        word_freq[i] += 1
len(word_freq)

# print les mot les plus fréquent 
sorted(word_freq, key=word_freq.get, reverse=True)[:10]

# entrainement word2vec
model = Word2Vec (bigram_token, min_count = 1, size = 300, workers = 3, window = 3,sg = 1)

print("nombre total de mot unique dans le modèle  : ", len(model.wv.vocab))
# Sauvegarde le modèle
model.save("sophiemodel.model")
