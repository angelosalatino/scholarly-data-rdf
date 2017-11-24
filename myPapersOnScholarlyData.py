from SPARQLWrapper import SPARQLWrapper, JSON

sparql = SPARQLWrapper("http://www.scholarlydata.org/sparql/")
sparql.setQuery("""
PREFIX conf: <https://w3id.org/scholarlydata/ontology/conference-ontology.owl#>
PREFIX made: <http://xmlns.com/foaf/0.1/>
PREFIX el: <http://purl.org/dc/elements/1.1/>
SELECT DISTINCT ?person ?title ?paper
WHERE{
?person conf:name "Angelo Antonio Salatino" .
?person made:made ?paper .
?paper conf:title ?title .
}
""")
sparql.setReturnFormat(JSON)
results = sparql.query().convert()

print(results["results"]["bindings"])

for result in results["results"]["bindings"]:
    print(result["title"]["value"])
    print()
