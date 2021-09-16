from elasticsearch import Elasticsearch
from elasticsearch_dsl import Search, Q


def konekt(job="", availability="", price="", mobility="", status="", experience="", skills=""):
    client = Elasticsearch(['<url_elastic>'])
    q = Q("bool", should=[Q("match", job=job),
        Q("match", availability=availability),
        Q("match", price=price),
        Q("match", mobility=mobility),
        Q("match", status=status),
        Q("match", experience=experience),
        Q("match", skills=skills)], minimum_should_match=1)
    s = Search(using=client, index="mysql_elk").query(q)[0:100]
    response = s.execute()
    search = get_results(response)
    return search


def get_cv_by_id(cvid=""):
    es = Elasticsearch(['<url_elastic>'])
    res = es.get(index="mysql_elk", id=cvid)
    return res['_source']


def get_results(response):
    results = []
    for hit in response:
        if isinstance(hit.skills, str):
            skills = []
            skills = hit.skills.strip('[]').replace('"', '')
        else:
            skills = hit.skills
        result_tuple = (hit.job, hit.availability, hit.price, hit.mobility, hit.status, skills, hit.meta.id, hit.link)
        results.append(result_tuple)
    return results
