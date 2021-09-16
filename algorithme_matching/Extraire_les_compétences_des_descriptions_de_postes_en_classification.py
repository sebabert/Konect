import numpy as np 
import pandas as pd 
import string
import nltk
from nltk.corpus import stopwords
from sklearn.naive_bayes import MultinomialNB
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
from wordcloud import WordCloud

import matplotlib.pyplot as plt
%matplotlib inline
from textblob import Word


data_of = pd.read_csv('data_of.csv')
data_of.head()
data_of['OF'][0]

test = data_of.dropna()

print("\n ** brut data **\n")
print(test.head())
print("\n ** data shape **\n")
print(test.shape)

fig=plt.figure(figsize=(10, 5), dpi= 80, facecolor='w', edgecolor='k')
test.JOB.hist()

test['OF'] = test['OF'].apply(lambda x: " ".join(x.lower()for x in x.split()))
## supprimer tabulation et ponctuation
test['OF'] = test['OF'].str.replace('[^\w\s]',' ')
## chiffres
test['OF'] = test['OF'].str.replace('\d+', '')

#remove stop words
stop = stopwords.words('french')
test['OF'] = test['OF'].apply(lambda x: " ".join(x for x in x.split() if x not in stop))

## lemmatization
test['OF'] = test['OF'].apply(lambda x: " ".join([Word(word).lemmatize() for word in x.split()]))

print("Preprocessed data: \n")
print(test.head())

jda = test.groupby(['JOB']).sum().reset_index()
print("Aggregé job descriptions: \n")
print(jda)

jobs_list = jda.JOB.unique().tolist()
for job in jobs_list:

    # Commencez par un examen:
    text = jda[jda.JOB == job].iloc[0].OF
    #print(text)
    # Créer et générer une image de mots:
    wordcloud = WordCloud().generate(text)
    print("\n***",job,"***\n")
    # Afficher l'image générée:
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis("off")
    plt.show()    
    
other_stop_words = ['quipe', 'qualit','experience','mission','client','projet','conception','participer',
                    'rience','application','technique','connaissance','exp','velopper','dõun','tant','dõana',
                   ' recherch', 'ee','lõ','veloppeur','dõune','dõautres','dõau','ætre','dõexp','lõensemble',
                   'op','syst','programming','veloppement','jee','spring','code','ing','el','an','etc','mener','impliqu','bon',
                    'chez','websphere','indispensables','dot','management','fran','construire','partir','disposez','renforcer',
                    'fonctions','impl','significative','rement','produit','composants','micro','issu','donn','lioration',
                   'javaee','gion','gradleé','gité','volu','developpe','dõinvestissement','outils','nieur']

test['OF'] = test['OF'].apply(lambda x: " ".join(x for x in x.split() if x not in other_stop_words))

## Convertir le texte en caractéristiques 
vectorizer = TfidfVectorizer()
#Tokenize et construit vocabulaire 
X = vectorizer.fit_transform(test.OF)
#print(X)
y = test.JOB

# diviser les données en 80% de formation et 20% de test
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2,random_state=109) 
print("train data shape: ",X_train.shape)
print("test data shape: ",X_test.shape)

# entrainement modèle 
clf = MultinomialNB()
clf.fit(X_train, y_train)
## Prediction
y_predicted = clf.predict(X_test)

y_train.hist()
y_test.hist()

#évaluer les prédictions
print("Accuracy score est: ",accuracy_score(y_test, y_predicted))
print("Classes: (pour aider à lire la matrice de confusion\n", clf.classes_)
print("Confusion Matrix: ")

print(confusion_matrix(y_test, y_predicted))
print("Classification Raport: ")
print(classification_report(y_test, y_predicted))

print(clf.coef_)
print(clf.coef_.shape)

from textblob import TextBlob
technical_skills = ['python', 'c','r', 'c++','java','hadoop','scala','flask','pandas','spark','scikit-learn',
                    'numpy','php','sql','mysql','css','mongdb','nltk','fastai' , 'keras', 'pytorch','tensorflow',
                   'linux','Ruby','JavaScript','django','react','reactjs','ai','bi','ui','tableau','machine learnig','statistiques',
                   'selenium','nlp','git','angular','agile','maven','jenkins','cassandra']
feature_array = vectorizer.get_feature_names()
#print(feature_array)

features_numbers = len(feature_array)
#print(features_numbers)

## nombre maximum de caractéristiques triées
n_max = int(features_numbers * 0.1)
#print(n_max)

##initialise output dataframe
output = pd.DataFrame()
for i in range(0,len(clf.classes_)):
    print("\n****" ,clf.classes_[i],"****\n")
    class_prob_indices_sorted = clf.feature_log_prob_[i, :].argsort()[::-1]
    raw_skills = np.take(feature_array, class_prob_indices_sorted[:n_max])
    print("liste des compétences non traitées :")
    print(raw_skills)
    
    ## Extraction technique compétence
    top_technical_skills= list(set(technical_skills).intersection(raw_skills))[:10]
    #print("Top technical skills",top_technical_skills)
    
    ## Extract adjectives
    
    # Supprimer les compétences techniques de la liste des compétences brutes
    ## A ce stade, la liste des compétences brutes ne contient pas les compétences techniques.

    raw_skills = [x for x in raw_skills if x not in top_technical_skills]
    raw_skills = list(set(raw_skills) - set(top_technical_skills))

    # transformer la liste en chaîne de caractères
    txt = " ".join(raw_skills)
    blob = TextBlob(txt)
    #top 6 adjective
    top_adjectives = [w for (w, pos) in TextBlob(txt).pos_tags if pos.startswith("JJ")][:6]
    #print("Top 6 adjectives: ",top_adjectives)
    
    output = output.append({'job_title':clf.classes_[i],
                        'technical_skills':top_technical_skills,
                         },
                       ignore_index=True)
                      
print(output.T)
