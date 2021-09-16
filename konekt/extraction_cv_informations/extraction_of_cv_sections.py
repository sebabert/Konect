# -*- coding: utf-8 -*-
"""
Created on Mars 2021

@author: alass
"""

# Importation des librairies nécéssaires
import re
import os
from datetime import date

import pandas as pd
from tika import parser

import logging

import spacy
from spacy.matcher import Matcher
from spacy.matcher import PhraseMatcher

import sys
import operator
import string

from pdf2image import convert_from_path, convert_from_bytes
import pytesseract
from pytesseract import Output

# pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
if os.name == 'nt':
  pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

# Constiution des dictionnaires de termes pour chaque titre de section de cv

objectif = (
  "objectif",
  "objectif de carrière",
  "objectif professionnel",
  "résumé",
  "résumé de carrière",
  "résumé professionnel",
  "résumé des qualifications",
  "profil",
  "description",
  "présentation",
  "A propos de moi",
  "profil",
  "souhait",
  "souhait professionnel",
  "souhait de carrière",
)

experiences = (
  "expérience",
  "expérience professionnelle",
  "EXPÉRIENCES PROFESSIONNELLES",
  "EXPERIENCES PROFESSIONNELLES",
  "expérience supplémentaire",
  "expérience liée à la carrière",
  "expérience connexe",
  "expérience en programmation",
  "freelance",
  "EXPERIENCE",
  "expérience en freelance",
  "parcours professionnel",
  "historique d'emploi",
  "historique du travail",
  "carrière",
  "missions",
  "experience"
)

formation = (
  "formation",
  "éducation",
  "diplôme",
  "diplômes",
  "formation académique",
  "expérience académique",
  "programmes",
  "cours",
  "FORMATION",
  "cours connexes",
  "qualifications éducatives",
  "formation scolaire",
  "éducation et formation",
  "formation",
  "formation universitaire",
  "formation professionnelle",
  "expérience de projet de cours",
  "projets de cours connexes",
  "expérience de stage",
  "les stages",
  "apprentissages",
  "activités universitaires",
  "certifications",
  "formation spéciale",
  "diplômes et formations"
)

competences = (
  "compétences",
  "qualifications",
  "titres de compétences",
  "domaines d'expertise",
  "domaines de connaissances",
  "domaine d’expériences professionnelles",
  "autres compétences",
  "autres aptitudes",
  "compétences liées à la carrière",
  "compétences professionnelles",
  "compétences spécialisées",
  "compétences techniques",
  "compétence techniques"
  "compétences informatiques",
  "compétences personnelles",
  "connaissances informatiques",
  "technologies",
  "expérience technique",
  "compétences et aptitudes linguistiques",
  "langages de programmation",

)

centres_d_interet = (
  "centres d'intérêt",
  "activités et distinctions",
  "activités",
  "affiliations",
  "affiliations professionnelles",
  "associations",
  "associations professionnelles",
  "adhésions",
  "adhésions professionnelles",
  "participation sportive",
  "engagement communautaire",
  "arbitrage",
  "activités civiques",
  "activités extra-scolaires",
  "activités professionnelles",
  "travail bénévole",
  "CENTRES D’INTÉRÊT",
  "expérience de bénévolat",
  "informations complémentaires",
  "loisir"
)

realisations = (
  "présentations",
  "accomplissement",
  "présentations de conférences",
  "expositions",
  "articles",
  "publications",
  "publications professionnelles",
  "recherche",
  "bourses de recherche",
  "projets de recherche",
  "projets personnels"
  "intérêts de recherche actuels",
  "thèse",
  "thèses",
  "projets académiques",
  "projet"
)

langues = (
  "langues",
  "linguistique",
  "compétences linguistiques",
  "langue vivante",
  "langues pratiquées",
  "compétences langagières"
)

contact = (
  "contact",
  "coordonnées"
)


# Nous allons définir plusieurs fonctions dont leurs descriptions se trouvent
# à l'intérieure des fonctions elles-mêmes.

def extract_text_from_cv_in_pdf(cv_in_pdf_file):
  """
  Cette fonction permet d'extraire le texte brut d'un cv en pdf.

  Entrée :
      cv_in_pdf_file : le chemin du cv en format pdf;

  Sorties :
      cv_lines : les textes de chaque ligne du cv;
      text : le texte brute du cv.
  """
  # Après l'ouverture du fichier à l'aide de la méthode "from_file" de
  # l'objet "parser" de tika, on extrait et on stocke le texte brut dans
  # "text"

  text = parser.from_file(cv_in_pdf_file, service='text')['content']

  # Nettoyage du texte brute et stockage du texte nettoyé dans "cleaned_text"

  cleaned_text = re.sub(r'\n+', '\n', text)
  cleaned_text = cleaned_text.replace("\r", "\n")
  cleaned_text = cleaned_text.replace("\t", " ")
  cleaned_text = re.sub(r"\uf0b7", " ", cleaned_text)
  cleaned_text = re.sub(r"\(cid:\d{0,2}\)", " ", cleaned_text)
  cleaned_text = re.sub(r'• ', " ", cleaned_text)

  # Division du texte nettoyé en lignes individuelles (cv_lines)

  cv_lines = cleaned_text.splitlines(True)

  # Suppression des espaces vides dans "cv_lines"
  cv_lines = [re.sub('\s+', ' ', line.strip()) for line in cv_lines if line.strip()]

  return (cv_lines, text)


def extract_text_from_all_cv_in_pdf(cv_in_pdf_file):
  """
  Cette fonction permet d'extraire le texte brut d'un cv en pdf.

  Entrée :
      cv_in_pdf_file : le chemin du cv en format pdf;

  Sorties :
      cv_lines : les textes de chaque ligne du cv;
      text : le texte brute du cv.
  """
  # Après converssion du fichier pdf en image, on extrait et on stocke le
  # texte brut dans "text"

  try:
    from PIL import Image
  except ImportError:
    import Image
  images = convert_from_path(cv_in_pdf_file)
  text = pytesseract.image_to_string(images[0], lang='fra')
  for t in range(1, len(images)):
    text += pytesseract.image_to_string(images[t], lang='fra')

  # Nettoyage du texte brute et stockage du texte nettoyé dans "cleaned_text"

  cleaned_text = re.sub(r'\n+', '\n', text)
  cleaned_text = cleaned_text.replace("\r", "\n")
  cleaned_text = cleaned_text.replace("\t", " ")
  cleaned_text = re.sub(r"\uf0b7", " ", cleaned_text)
  cleaned_text = re.sub(r"\(cid:\d{0,2}\)", " ", cleaned_text)
  cleaned_text = re.sub(r'• ', " ", cleaned_text)

  # Division du texte nettoyé en lignes individuelles (cv_lines)

  cv_lines = cleaned_text.splitlines(True)

  # Suppression des espaces vides dans "cv_lines"
  cv_lines = [re.sub('\s+', ' ', line.strip()) for line in cv_lines if line.strip()]

  for i in range(len(cv_lines)):
    try:
      if cv_lines[i][1] == " ":
        cv_lines[i] = cv_lines[i].replace(cv_lines[i][0], "", 1).strip()
    except:
      cv_lines[i] = cv_lines[i]
    try:
      if cv_lines[i][2] == " ":
        cv_lines[i] = cv_lines[i].replace(cv_lines[i][:2], "", 1).strip()
    except:
      cv_lines[i] = cv_lines[i]

  return (cv_lines, text)


def extract_text_from_cv_in_docx(cv_in_docx_file):
  """
  Cette fonction permet d'extraire le texte brut d'un cv en format docx.

  Entrée :
      cv_in_docx_file : le chemin du cv en format docx;

  Sorties :
      cv_lines : les textes de chaque ligne du cv;
      text : le texte brute du cv.
  """

  # Après l'ouverture du fichier à l'aide de la méthode "from_file" de
  # l'objet "parser" de tika, on extrait et on stocke le texte brut dans
  # "text"

  text = parser.from_file(cv_in_docx_file, service='text')['content']

  # Nettoyage du texte brute et stockage du texte nettoyé dans "cleaned_text"

  cleaned_text = re.sub(r'\n+', '\n', text)
  cleaned_text = cleaned_text.replace("\r", "\n").replace("\t", " ")

  # Division du texte nettoyé en lignes individuelles (cv_lines)

  cv_lines = cleaned_text.splitlines()
  cv_lines = [re.sub('\s+', ' ', line.strip()) for line in cv_lines if line.strip()]

  return (cv_lines, text)


def extract_text_from_cv(cv_file):
  """
  Cette fonction permet d'extraire le texte brut d'un cv en pdf ou docx.

  Entrée :
      cv_file : le chemin du cv;

  Sorties :
      texte : les textes de chaque ligne du cv;
  """
  if os.path.splitext(cv_file)[-1] == '.pdf':
    texte = extract_text_from_all_cv_in_pdf(cv_file)[0]
  # if os.path.splitext(cv_file)[-1] == '.doc':
  #     texte = extract_text_from_all_cv_in_doc(cv_file)[0]
  else:
    texte = extract_text_from_cv_in_docx(cv_file)[0]
  return (texte)


def detect_cv_section_indices(section_title_to_detect, cv_sections, cv_indices):
  """
  Fonction permettant de détecter les titres de sections de cv selon les
  critères prédefinis(voir rapport technique)

  Parameters
  ----------
  section_title_to_detect : titre de section à détecter;

  cv_sections : sections du cv à chercher;

  cv_indices : critères pour détecter les titres de sections de cv.


  Returns
  -------
  None.

  """
  for i, line in enumerate(section_title_to_detect):

    if line[0].islower():
      continue

    header = line.lower()

    if [j for j in objectif if header.startswith(j)]:
      try:
        cv_sections['objectif'][header]
      except:
        cv_indices.append(i)
        header = [j for j in objectif if header.startswith(j)][0]
        cv_sections['objectif'][header] = i
    elif [k for k in experiences if header.startswith(k)]:
      try:
        cv_sections['experiences'][header]
      except:
        cv_indices.append(i)
        header = [k for k in experiences if header.startswith(k)][0]
        cv_sections['experiences'][header] = i
    elif [n for n in formation if header.startswith(n)]:
      try:
        cv_sections['formation'][header]
      except:
        cv_indices.append(i)
        header = [n for n in formation if header.startswith(n)][0]
        cv_sections['formation'][header] = i
    elif [p for p in competences if header.startswith(p)]:
      try:
        cv_sections['competences'][header]
      except:
        cv_indices.append(i)
        header = [p for p in competences if header.startswith(p)][0]
        cv_sections['competences'][header] = i
    elif [m for m in centres_d_interet if header.startswith(m)]:
      try:
        cv_sections['centres_d_interet'][header]
      except:
        cv_indices.append(i)
        header = [m for m in centres_d_interet if header.startswith(m)][0]
        cv_sections['centres_d_interet'][header] = i
    elif [q for q in realisations if header.startswith(q)]:
      try:
        cv_sections['realisations'][header]
      except:
        cv_indices.append(i)
        header = [q for q in realisations if header.startswith(q)][0]
        cv_sections['realisations'][header] = i
    elif [r for r in realisations if header.startswith(r)]:
      try:
        cv_sections['langues'][header]
      except:
        cv_indices.append(i)
        header = [r for r in realisations if header.startswith(r)][0]
        cv_sections['langues'][header] = i


def slice_cv(section_title_to_detect, cv_sections, cv_indices):
  """


  Parameters
  ----------
  section_title_to_detect : TYPE
      DESCRIPTION.
  cv_sections : TYPE
      DESCRIPTION.
  cv_indices : TYPE
      DESCRIPTION.

  Returns
  -------
  None.

  """
  cv_sections['contact'] = section_title_to_detect[:cv_indices[0]]

  for section, value in cv_sections.items():
    if section == 'contact':
      continue

    for sub_section, start_idx in value.items():
      end_idx = len(section_title_to_detect)
      if (cv_indices.index(start_idx) + 1) != len(cv_indices):
        end_idx = cv_indices[cv_indices.index(start_idx) + 1]

      cv_sections[section][sub_section] = section_title_to_detect[start_idx:end_idx]


def detect_cv_section(section_title_to_detect):
  """
  ...cv_lines.....

  Parameters
  ----------
  section_title_to_detect : TYPE
      DESCRIPTION.

  Returns
  -------
  cv_sections : TYPE
      DESCRIPTION.

  """
  cv_sections = {
    'objectif': {},
    'experiences': {},
    'formation': {},
    'competences': {},
    'realisations': {},
    'centres_d_interet': {},
    'langues': {}
  }

  cv_indices = []

  detect_cv_section_indices(section_title_to_detect, cv_sections, cv_indices)
  if len(cv_indices) != 0:
    slice_cv(section_title_to_detect, cv_sections, cv_indices)
  else:
    cv_sections['contact'] = []

  return cv_sections


def extraction_of_exp_sections(experiences):
  """
  Function permettant d'extraire les différentes expériences d'un cv.

  Parameters
  ----------
  experiences : pdf file or docx file

  Returns
  -------
  exps : dictionnaire contenant les différentes expériences d'un cv.

  """

  # Chargement du modèle de spacy en langue française
  nlp = spacy.load("fr_core_news_sm")

  # Extraction et stockage de la section "expérience" d'un cv dans "texte"
  try:
    sections_cv = detect_cv_section(extract_text_from_cv(experiences))
    texte = list(sections_cv["experiences"].values())[0][1:]
  except:
    sections_cv = detect_cv_section(extract_text_from_cv_in_pdf(experiences)[0])
    texte = list(sections_cv["experiences"].values())[0][1:]

  # Traitement sémantique du texte
  doc = nlp(' '.join(texte))

  # Expréssion régulière pour détecter les différents formats de dates
  expression = '(((01)|(02)|(03)|(04)|(05)|(06)|(07)|(08)|(09)|(10)|(11)|(12)|(jan)|(feb)|(mar)|(apr)|(may)|(jun)|(jul)|(aug)|(sep)|(oct)|(nov)|(dec)|(Janvier)|(Février)|(Mars)|(Avril)|(Mai)|(Juin)|(Juillet)|(Âout)|(Septembre)|(Octobre)|(Novembre)|(Décembre))[^a-zA-Z\\d]?((20|19)(\\d{2})|(\\d{2}))([^a-zA-Z\\d]{1,4}|(\\s*to\\s*))(((\\d{2})?[^a-zA-Z\\d]?((01)|(02)|(03)|(04)|(05)|(06)|(07)|(08)|(09)|(10)|(11)|(12)|(jan)|(feb)|(mar)|(apr)|(may)|(jun)|(jul)|(aug)|(sep)|(oct)|(nov)|(dec)|(Janvier)|(Février)|(Mars)|(Avril)|(Mai)|(Juin)|(Juillet)|(Âout)|(Septembre)|(Octobre)|(Novembre)|(Décembre))[^a-zA-Z\\d]?((20|19)(\\d{2})|(\\d{2})))|(present|current)))|(((20|19)(\\d{2}))([^a-zA-Z\\d]{1,4}|(\\s*to\\s*))(((20|19)(\\d{2}))|(présent|aujourd\'hui)))'

  # Recherche des différents formats de dates en effectuant une correspondance
  # sur le texte (doc.text) avec la méthode finditer du module re et en
  # utilisant la méthode char_span de la classe "doc" de spacy pour créer un
  # span (ind_span) à partir des indices de caractères de la correspondance
  ind_span = []
  for match in re.finditer(expression, doc.text):
    start, end = match.span()
    span = doc.char_span(start, end)
    ind_span.append(match.span())

  # On utilise les indices de début et de fin des dates trouvées pour
  # extraire les différentes expériences de la section "expérience" d'un cv.
  # On crée un dictionnaire qu'on a nommé "exps" qui contient les
  # dictionnaires "exp1", "exp2", ... "expN" avec N le nombre d'expériences.
  # Chaque dictionnaire expN a trois clés à savoir "durationN", "descriptionN",
  # et "position_and_companyN" qui ont pour valeurs respectivement les dates
  # détectées precedemment, les textes comprises entre deux dates consécutives
  # et les postes et entreprises que nous chercherons à détecter plutard.
  # Pour bien comprendre, par exemple pour constituer les expériences de
  # notre cv de test qui contient trois expériences, après avoir détecter les
  # trois dates :
  #     - on stocke respectivement les trois dates dans "duration1",
  #       "duration2" et "duration3",
  #     - on sélectionne le texte comprise entre la première date et la
  #       séconde et on le stocke ce texte dans "description1",
  #     - on sélectionne le texte comprise entre la deuxième date et la
  #       troisième et on le stocke ce texte dans "description2",
  #     - et on sélectionne et on stocke le texte qui vient après la troisième
  #       date dans "description3".
  # On utilise la même procedure pour extraire ci-dessous les sept premières
  # expériences d'un cv

  if doc[2].text in doc.text[ind_span[0][0]:ind_span[0][1]]:
    exps = []
    for i in range(len(ind_span)):
      if i < len(ind_span) - 1:
        exps.append({
          "exp" + str(i + 1): {"duration": doc.text[ind_span[i][0]:ind_span[i][1]],
                               "description": doc.text[ind_span[i][1]:ind_span[i + 1][0]],
                               "company_name": "",
                               "job_title": "",
                               "job_location": "",
                               "tools": ""}
        })
      else:
        exps.append({
          "exp" + str(i + 1): {"duration": doc.text[ind_span[i][0]:ind_span[i][1]],
                               "description": doc.text[ind_span[i][1]:],
                               "company_name": "",
                               "job_title": "",
                               "job_location": "",
                               "tools": ""}
        })
  if doc[2].text not in doc.text[ind_span[0][0]:ind_span[0][1]]:
    exps = []
    for i in range(len(ind_span)):
      if i < len(ind_span) - 1:
        exps.append({

          "exp" + str(i + 1): {"duration": doc.text[ind_span[i][0]:ind_span[i][1]],
                               "description": doc.text[ind_span[i][1]:ind_span[i + 1][0]],
                               "company_name": "",
                               "job_title": "",
                               "job_location": "",
                               "tools": ""}
        })
      else:
        exps.append({
          "exp" + str(i + 1): {"duration": doc.text[ind_span[i][0]:ind_span[i][1]],
                               "description": doc.text[ind_span[i][1]:],
                               "company_name": "",
                               "job_title": "",
                               "job_location": "",
                               "tools": ""}
        })

  return (exps)


def extraction_name(texte):
  """
  Function permettant d'extraire le nom d'un cv.

  Parameters
  ----------
  texte : cv's text.

  Returns
  -------
  span.text : name in string.

  """
  # Chargement du modèle français
  nlp = spacy.load('fr_core_news_sm')

  # initialisation du matcher
  matcher = Matcher(nlp.vocab)
  # Traitement du texte
  nlp_texte = nlp(texte)

  # définition motif pour détecter nom et prénom
  pattern = [{'POS': 'PROPN'}, {'POS': 'PROPN'}]

  matcher.add('NAME', [pattern])

  matches = matcher(nlp_texte)

  for match_id, start, end in matches:
    span = nlp_texte[start:end]
    return span.text


def extraction_email(texte):
  """
  Function permettant d'extraire l'email d'un cv.

  Parameters
  ----------
  texte : cv's text.

  Returns
  -------
  email : email in string.
  """
  email = re.findall("([^@|\s]+@[^@]+\.[^@|\s]+)", texte)
  if email:
    try:
      return email[0].split()[0].strip(';')
    except IndexError:
      return ("...")
  else:
    return ("...")


def extraction_phone(texte):
  """
  Function permettant d'extraire le numéro de téléphone d'un cv.

  Parameters
  ----------
  texte : str
      cv's text.

  Returns
  -------
  str
      phone number in string.

  """
  phone = re.findall(re.compile(r'([\+]?33[-]?|[0])?([0]\d{1})\D*(\d{2})\D*(\d{2})\D*(\d{2})\D*(\d*)'), texte)

  if phone:
    number = ''.join(phone[0])
    if len(number) > 10:
      return '00' + number
    else:
      return number
  else:
    return ("...")
