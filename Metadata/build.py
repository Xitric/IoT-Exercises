from rdflib import Literal

from wrapper import *

TTL_FILENAME = 'turtle/build_gen.ttl'

g = model()

my_repo = BUILD['/repository/0']
g.add((my_repo, RDF.type, BUILD.repository))
g.add((my_repo, RDFS.label, Literal('Cool repo')))

my_branch = BUILD['/branch/0']
g.add((my_branch, RDF.type, BUILD.branch))
g.add((my_branch, BUILD.branchIn, my_repo))
g.add((my_branch, RDFS.label, Literal('Feature branch')))

g.serialize(TTL_FILENAME, 'turtle')
del g
g = Graph()
g.parse(TTL_FILENAME, format='turtle')

q_branch = \
    '''
    SELECT DISTINCT ?branch_name
    WHERE {
        ?repo       rdf:type        build:repository .
        ?branch     build:branchIn  ?repo .
        ?branch     rdfs:label      ?branch_name .
    }
    '''
pprint(query(g, q_branch))
