from rdflib import Graph, Namespace
import json

RDF = Namespace('http://www.w3.org/1999/02/22-rdf-syntax-ns#')
RDFS = Namespace('http://www.w3.org/2000/01/rdf-schema#')
OWL = Namespace('http://www.w3.org/2002/07/owl#')
BRICK = Namespace('https://brickschema.org/schema/1.1.0/Brick#')
N = Namespace('http://ses.sdk.dk/junk/example#')
BUILD = Namespace('https://hej.com/schema/1.0.0/Build#')  # Added for exercise


def model():
    g = Graph()

    # g.parse('turtle/Brick_expanded.ttl', format='turtle')
    g.parse('turtle/build.ttl', format='turtle')

    g.bind('rdf', RDF)
    g.bind('rdfs', RDFS)
    g.bind('owl', OWL)
    # g.bind('brick', BRICK)
    # g.bind('n', N)
    g.bind('build', BUILD)  # Added for exercise

    return g


def query(g, q):
    r = g.query(q)
    return list(map(lambda row: list(row), r))


def update(g, q):
    r = g.update(q)


def pprint(structure):
    pretty = json.dumps(structure, sort_keys=True, indent=4, separators=(',', ': '))
    print(pretty)
