from rdflib import Graph, Namespace
import json

# Standard namespaces that we can refer to
# See: https://www.w3.org/TR/rdf-schema/
RDF = Namespace('http://www.w3.org/1999/02/22-rdf-syntax-ns#')
RDFS = Namespace('http://www.w3.org/2000/01/rdf-schema#')

# See: https://www.w3.org/TR/2004/REC-owl-guide-20040210/
OWL = Namespace('http://www.w3.org/2002/07/owl#')

# See: https://brickschema.org/ontology
BRICK = Namespace('https://brickschema.org/schema/1.1.0/Brick#')

# We define our own namespace to avoid naming conflicts
# This is used to represent build information like git repository, branch, commit id, etc.
BUILD = Namespace('https://github.com/Xitric/IoT-Exercises/releases/tag/v1.0.0/Metadata/Build#')


def model():
    g = Graph()

    g.parse('turtle/demo/Brick_expanded.ttl', format='turtle')

    # Read file describing our data types and relationships for build information
    g.parse('turtle/buildinfo/Build_extension.ttl', format='turtle')

    g.bind('rdf', RDF)
    g.bind('rdfs', RDFS)
    g.bind('owl', OWL)
    g.bind('brick', BRICK)
    g.bind('build', BUILD)

    return g


def query(g, q):
    r = g.query(q)
    return list(map(lambda row: list(row), r))


def update(g, q):
    r = g.update(q)


def pprint(structure):
    pretty = json.dumps(structure, sort_keys=True, indent=4, separators=(',', ': '))
    print(pretty)
