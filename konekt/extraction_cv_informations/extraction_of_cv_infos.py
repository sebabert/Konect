# -*- coding: utf-8 -*-
"""
Created  APr 2021

"""

# Importation des modules et fonctions nécéssaires
from extraction_cv_informations.extraction_of_cv_sections import extract_text_from_cv_in_pdf, \
  extract_text_from_all_cv_in_pdf, extract_text_from_cv, detect_cv_section, \
  extract_text_from_cv_in_docx, extraction_of_exp_sections, extraction_name, \
  extraction_email, extraction_phone

import datetime


def extraction_of_cv_infos(cv_file):
    """
    Fonction permettant d'extraire des informations sur un cv en format pdf ou docx.

    Parameters
    ----------
    cv_file : str
    le chemin du cv en format pdf ou docx.

    Returns
    -------
    cv_infos : dict
    Le dictionnaire contenant les informations extraites du cv.

    """
    # Extraction du texte du cv
    text = extract_text_from_cv(cv_file)
    # Extraction des sections du cv
    cv_section = detect_cv_section(text)
    # Extraction des informations du cv
    try:
        cv_infos = {
            "name": text[0],
            "job": " ",
            "address": " ",
            "phone": extraction_phone(' '.join(extract_text_from_cv_in_pdf(cv_file)[0])),
            "email": extraction_email(' '.join(extract_text_from_cv_in_pdf(cv_file)[0])),
            "status": " ",
            "availability": " ",
            "mobility": " ",
            "price": " ",
            "salary": " ",
            "formations": {
                "date": " ",
                "name_of_diploma": cv_section['formation']
            },
            "experience": extraction_of_exp_sections(cv_file),
            "skills": cv_section['competences']
            # "day_of_info_collection": datetime.datetime.now().strftime("%d/%m/%Y"),
            # "id": " "
        }
    except:
        cv_infos = {
            "name": text[0],
            "job": " ",
            "address": " ",
            "phone": extraction_phone(' '.join(extract_text_from_cv_in_pdf(cv_file)[0])),
            "email": extraction_email(' '.join(extract_text_from_cv_in_pdf(cv_file)[0])),
            "status": " ",
            "availability": " ",
            "mobility": " ",
            "price": " ",
            "salary": " ",
            "formations": {
                "date": " ",
                "name_of_diploma": cv_section['formation']
            },
            "experience": [{
                "exp1": {
                    "job_title": '',
                    "job_location": '',
                    "duration": '',
                    "company_name": '',
                    "tools": '',
                    "description": cv_section['experiences']['expérience']
                }
            }],
            "skills": cv_section['competences'],
            # "day_of_info_collection": datetime.datetime.now().strftime("%d/%m/%Y"),
            # "id": " "
        }

    return cv_infos