from SPARQLWrapper import SPARQLWrapper, JSON

from igraph import *
from cairo import *


sparql = SPARQLWrapper("http://www.scholarlydata.org/sparql/")

g = Graph()
g.vs['name']=""
#get papers from the dataset 


sparql.setQuery("""
PREFIX person: <https://w3id.org/scholarlydata/person/>
PREFIX conf: <https://w3id.org/scholarlydata/ontology/conference-ontology.owl#>
SELECT DISTINCT ?confe ?date ?proc
WHERE{
  ?confe conf:startDate ?date . 
  ?confe conf:hasProceedings ?proc .
  FILTER (?date > "2015"^^xsd:gYear)
}
""")
sparql.setReturnFormat(JSON)
conferences = sparql.query().convert()
conferences = conferences["results"]["bindings"]
for result in conferences:
    print("* " + result["confe"]["value"] + " ** " + result["date"]["value"] + " ** " + result["proc"]["value"])
    print()


for result in conferences:
    papersQuery = """
    PREFIX person: <https://w3id.org/scholarlydata/person/>
    PREFIX conf: <https://w3id.org/scholarlydata/ontology/conference-ontology.owl#>
    PREFIX cr: <http://purl.org/dc/elements/1.1/>
    PREFIX nm: <http://xmlns.com/foaf/0.1/>
    SELECT DISTINCT ?paper (group_concat(distinct ?author ; separator = ";") AS ?authors)
    WHERE{
      <%s> conf:hasPart ?paper . 
      ?paper cr:creator ?author 
    }
    ORDER BY ?paper
    """ %(result["proc"]["value"])
    sparql.setQuery(papersQuery)
    sparql.setReturnFormat(JSON)
    authors = sparql.query().convert()
    authors = authors["results"]["bindings"]
    for result in authors:
        auths = result["authors"]["value"].split(";")
        for i in range(0,len(auths)):
            for j in range(i+1,len(auths)):
                #check if the edge exists
                if auths[i] not in g.vs['name']: g.add_vertices(auths[i])
                if auths[j] not in g.vs['name']: g.add_vertices(auths[j])
                g.add_edges([(auths[i],auths[j])])
        #print("* " + result["paper"]["value"] + " ** " + result["authors"]["value"])
        
        
        
layout = g.layout("kk")
plot(g, layout = layout)

