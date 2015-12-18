__author__ = 'andra'

__author__ = 'andra'

import time
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__))+"/../../../ProteinBoxBot_Core")
import PBB_login
import PBB_settings
import PBB_Core
import pprint

from SPARQLWrapper import SPARQLWrapper, JSON

logincreds = PBB_login.WDLogin(PBB_settings.getWikiDataUser(), PBB_settings.getWikiDataPassword())

sparql = SPARQLWrapper("https://query.wikidata.org/bigdata/namespace/wdq/sparql")
sparql.setQuery("""
PREFIX wikibase: <http://wikiba.se/ontology#>
PREFIX wd: <http://www.wikidata.org/entity/>
PREFIX wdt: <http://www.wikidata.org/prop/direct/>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX p: <http://www.wikidata.org/prop/>
PREFIX v: <http://www.wikidata.org/prop/statement/>

SELECT DISTINCT ?protein ?protein2 {
?protein wdt:P352 ?uniprot ;
         wdt:P705 ?ensemblp ;
         wdt:P638 ?pdb ;
         wdt:P637 ?refseqp ;
         wdt:P703 wd:Q5 .
?protein2 wdt:P352 ?uniprot ;
          wdt:P705 ?ensemblp ;
          wdt:P638 ?pdb ;
          wdt:P637 ?refseqp ;
          wdt:P703 wd:Q5 .
FILTER (?protein != ?protein2)
                   }
""")

sparql.setReturnFormat(JSON)
results = sparql.query().convert()

# pprint.pprint(results)
processed = []
counter = 0
for result in results["results"]["bindings"]:
    if result["protein"]["value"] not in processed and result["protein2"]["value"]:
        counter = counter + 1
        print(result["protein"]["value"],  result["protein2"]["value"])
        protein1 = result["protein"]["value"].replace("http://www.wikidata.org/entity/", "")
        protein2 = result["protein2"]["value"].replace("http://www.wikidata.org/entity/", "")
        if int(protein1[1:]) > int(protein2[1:]):
            mergefrom = protein1
            mergeto = protein2
        else:
            mergefrom = protein2
            mergeto = protein1

        processed.append(result["protein"]["value"])
        processed.append(result["protein2"]["value"])

        PBB_Core.WDItemEngine.merge_items(, , logincreds)
        sys.exit()
print(counter)