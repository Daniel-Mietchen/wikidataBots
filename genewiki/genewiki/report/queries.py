from django.conf import settings
from django.db import models

import PBB_Core, PBB_login

def get_genes():
    #Query wikidata to get the number of human genes
    prefix = '''
    PREFIX wdt: <http://www.wikidata.org/prop/direct/>
    PREFIX wd: <http://www.wikidata.org/entity/>
    PREFIX p: <http://www.wikidata.org/prop/>
    PREFIX v: <http://www.wikidata.org/prop/statement/>
    PREFIX prov: <http://www.w3.org/ns/prov#>
    PREFIX reference: <http://www.wikidata.org/prop/reference/>
    '''

    query = '''
    SELECT (COUNT(DISTINCT ?ncbigeneId) AS ?count) WHERE {
    ?gene wdt:P279 wd:Q7187 .
    ?gene p:P351 ?ncbigeneId .
    ?gene wdt:P703 wd:Q5 .
    ?ncbigeneId prov:wasDerivedFrom ?derivedFrom .
    ?derivedFrom reference:P143 wd:Q20641742 .
    }
    '''

    sparql_results = PBB_Core.WDItemEngine.execute_sparql_query(prefix=prefix, query=query)['results']['bindings']
    count = ''
    for i in sparql_results:
        count = i['count']['value'].split('/')[-1]
    return(count)

def get_proteins():
    #Query wikidata to get the number of human proteins
    prefix = '''
    PREFIX wdt: <http://www.wikidata.org/prop/direct/>
    PREFIX wd: <http://www.wikidata.org/entity/>
    PREFIX p: <http://www.wikidata.org/prop/>
    PREFIX v: <http://www.wikidata.org/prop/statement/>
    PREFIX prov: <http://www.w3.org/ns/prov#>
    PREFIX reference: <http://www.wikidata.org/prop/reference/>
    '''

    query = '''
    SELECT (COUNT(?ncbigeneId) AS ?count) WHERE {
    ?gene wdt:P279 wd:Q7187 .
    ?gene p:P351 ?ncbigeneId .
    ?gene wdt:P703 wd:Q5 .
    ?gene ?p ?o .
    ?o prov:wasDerivedFrom ?derivedFrom .
    ?derivedFrom reference:P143 wd:Q20641742 .
    }
    '''
    sparql_results = PBB_Core.WDItemEngine.execute_sparql_query(prefix=prefix, query=query)['results']['bindings']
    count = ''
    for i in sparql_results:
        count = i['count']['value'].split('/')[-1]
    return(count)

def get_diseases():
    #Query wikidata to get the number of disease ontology terms
    prefix = '''
    PREFIX wd: <http://www.wikidata.org/entity/> 
    PREFIX wdt: <http://www.wikidata.org/prop/direct/>
    PREFIX p: <http://www.wikidata.org/prop/>
    PREFIX wikibase: <http://wikiba.se/ontology#>
    '''

    query = '''
    SELECT DISTINCT (COUNT(?diseases) as ?count)  WHERE {
    ?diseases p:P699 ?doid .
    ?doid wikibase:rank ?rank .
    }
    '''
    sparql_results = PBB_Core.WDItemEngine.execute_sparql_query(prefix=prefix, query=query)['results']['bindings']
    count = ''
    for i in sparql_results:
        count = i['count']['value'].split('/')[-1]
    return(count)

def get_compounds():
    #Query wikidata to get the number of compounds (drugs)
    prefix = '''
    PREFIX wd: <http://www.wikidata.org/entity/>
    PREFIX wdt: <http://www.wikidata.org/prop/direct/>
    PREFIX p: <http://www.wikidata.org/prop/>
    PREFIX v: <http://www.wikidata.org/prop/statement/>
    '''

    query = '''
    SELECT (COUNT (DISTINCT ?chembl) AS ?count)  WHERE {
    ?compound wdt:P592 ?chembl .
    OPTIONAL  {?compound rdfs:label ?label filter (lang(?label) = "en")}
    }
    '''
    sparql_results = PBB_Core.WDItemEngine.execute_sparql_query(prefix=prefix, query=query)['results']['bindings']
    count = ''
    for i in sparql_results:
        count = i['count']['value'].split('/')[-1]
    return(count)

def get_mspecies():
    #Query wikidata to get the number of microbial species 
    prefix = '''
    PREFIX wd: <http://www.wikidata.org/entity/>
    PREFIX wdt: <http://www.wikidata.org/prop/direct/>
    PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
    '''
    
    query = '''
    SELECT   (COUNT (DISTINCT ?species) AS ?count)  WHERE {
    ?gene wdt:P351 ?entrezID . # P351 Entrez Gene ID
    ?gene wdt:P703 ?species . # P703 Found in taxon
    ?species wdt:P171* wd:Q10876 .
    ?species rdfs:label ?label filter (lang(?label) = "en") .
    }
    '''
    sparql_results = PBB_Core.WDItemEngine.execute_sparql_query(prefix=prefix, query=query)['results']['bindings']
    count = ''
    for i in sparql_results:
        count = i['count']['value'].split('/')[-1]
    return(count)

def get_mgenes():
    #Query wikidata to get the number of microbial genes
    prefix = '''
    PREFIX wd: <http://www.wikidata.org/entity/>
    PREFIX wdt: <http://www.wikidata.org/prop/direct/>
    PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
    '''

    query = '''
    SELECT (COUNT (DISTINCT ?gene) AS ?count)  WHERE {
    ?gene wdt:P351 ?entrezID . # P351 Entrez Gene ID
    ?gene wdt:P703 ?species . # P703 Found in taxon
    ?species wdt:P171* wd:Q10876 .
    ?species rdfs:label ?label filter (lang(?label) = "en") .
    }
    '''
    sparql_results = PBB_Core.WDItemEngine.execute_sparql_query(prefix=prefix, query=query)['results']['bindings']
    count = ''
    for i in sparql_results:
        count = i['count']['value'].split('/')[-1]
    return(count)

def get_mproteins():
    #Query wikidata to get the number of microbial proteins
    prefix = '''
    PREFIX wd: <http://www.wikidata.org/entity/>
    PREFIX wdt: <http://www.wikidata.org/prop/direct/>
    PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
    '''
    
    query = '''
    SELECT (COUNT (DISTINCT ?protein) AS ?count)  WHERE {
    ?protein wdt:P352 ?uniprotID . # P352 UniProt ID
    ?protein wdt:P703 ?species . # P703 Found in taxon
    ?species wdt:P171* wd:Q10876 .
    ?species rdfs:label ?label filter (lang(?label) = "en") .
    }
    '''
    sparql_results = PBB_Core.WDItemEngine.execute_sparql_query(prefix=prefix, query=query)['results']['bindings']
    count = ''
    for i in sparql_results:
        count = i['count']['value'].split('/')[-1]
    return(count)
