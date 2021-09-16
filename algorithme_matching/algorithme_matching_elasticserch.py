competence = ["Gestion de projet", "lead-developer", "Machine Learning", "Gestion de l'accueil", "Python", "NLP", "Réglase des machines","java", "Maven", "DevOps", "Webservices REST / SOAP", "API management", "monitoring SI",
            "Postman", "Soap-ui", "Eclips","Mulesoft", "Dell boomi", "WSO2", "Jenkins Git", "Axway", "Talend", "webMethods","Es5", "TypeScript", "ReactJS/Redux", "Git", "Sass", "Jest", "React bootstrap", "Java/spring 5","PostgreSQL", "Docker","AWS","API"]

stopwords = ["le", "la", "les", "l", "'", "de", "du", "des", "et", "en"]

# nettoyage de textes et tokénisation de textes
import nltk
def pre_process(txt):
    tokens = nltk.wordpunct_tokenize(txt)
    tokens = [tok.lower() for tok in tokens if tok.lower() not in stopwords]
    return tokens

# construction de l'arbre de competence avec la liste de competence
import marisa_trie
pre_processed = [" ".join(pre_process(competence)) for competence in competence]
trie = marisa_trie.Trie(pre_processed)

# on cherche dans l'arbre les mots compétence du champ description de la fiche mission dans l'arbre de competence 
def trouver_keywords(description):
    tokens = pre_process(description)
    keywords = []
    i = 0
    courant_expression = []
    while i < len(tokens):
        courant_expression.append(tokens[i])
        if len(trie.keys("".join(courant_expression))) ==0:
            i+=1
            courant_expression = []
        elif "".join(courant_expression) in trie:
            keywords.append(" ".join(courant_expression))
            i += len(courant_expression)
            courant_expression = []
        else:
            i +=1
    return keywords

# teste 
competence_list=trouver_keywords(Data_fiche_mission['description'][1])
#print(competence_list)

#convertir liste en str
competence_list = competence_list
competence_list = " ".join(competence_list)
print(competence_list)

# construiction une expression regulière qui permet d'idetifier le nombre d'année experience de la fiche mission 
# à l'aide de cet regex, on cherche l'experience dans le champ desription de l afiche mission
import re
regex = re.compile(r"(?P<age>\d+) ans ?")
def trouver_année_mois_experience (texte):
    regex_anne = re.search(r"(?P<année_experience>\d+) an ?", texte)
    regex_mois = re.search(r"(?P<moi_experience>\d+) moi ?", texte)
    if regex_anne is not None:
        print (regex_anne.group('année_experience'))
    if regex_mois is not None:
        print (regex_mois.group('moi_experience'))
        
# test
experience=trouver_année_mois_experience(Data_fiche_mission['description'][1])
experience

metier = ["Senior Software Engineer","Développeur middleware confirmé","Développeur Fullstack Symfony","Ingénieur Concepteur Développeur ReactJs","Développeur middleware confirmé","Développeur Senior C# WPF","Développeur Full-Stack","Développeur / Développeuse Full Stack"]

# construction de l'arbre du metier avec la liste du metier
import marisa_trie
trie_title = marisa_trie.Trie(metier)

# on cherche dans l'arbre les nom du metier du champ description de la fiche mission dans l'arbre du metier 
def trouver_metier(title):
    metier = []
    i = 0
    courant_expressionn_metier = []
    while i < len(title):
        courant_expressionn_metier.append(title[i])
        if len(trie_title.keys("".join(courant_expressionn_metier))) ==0:
            i+=1
            courant_expressionn_metier = []
        elif "".join(courant_expressionn_metier) in trie_title:
            metier.append("".join(courant_expressionn_metier))
            i += len(courant_expressionn_metier)
            courant_expressionn_metier = []
        else:
            i +=1
    return metier

# test
job=trouver_metier(Data_fiche_mission['title'][1])
#convertir liste en str
job = " ".join(job)
print(job)

# import librairie permet de connecter avec elasticsearch
from elasticsearch import Elasticsearch 
from elasticsearch_dsl import Search, Q 

# construction des requetes du titre du poste,competence et experience, en recharches titre du poste,
#competence et experience extrait de l'offre d'emplois dasn la base de cv permet de filtrer les profils cv

def match(job="", skills="",experience=""):      
    mot = Elasticsearch()      
    q = Q("bool", should=[Q("match", job=job),
    Q("match", skills=skills),
    Q("match", experience=experience)],minimum_should_match=1)  
    s = Search(using=mot, index="matching1").query(q)[0:4] 
    response = s.execute()
    #print('Total% d hits found.' % response.hits.total)     
    search = get_results(response)    
    return search  
def get_results(response): 
    results = []  
    for hit in response: 
        result = (hit.skills,hit.job,hit.experience)   
        results.append(result)  
    return results

#execution avec la fonction match avec les mots clés extrait de l'offre d'emplois comme titre du poste et competence      
match(job=job, skills=competence_list)
