from rdflib import Literal

from wrapper import *

# The file to store our triplets inside once we have created some concrete data
TTL_FILENAME = 'turtle/build/Build_generated.ttl'

g = model()

# Repository representation
repos = {
    'Temperature sensor repository': {
        'master': {
            'ace86a1': 'Did some stuff',
            '7b6aafb': 'Did some more stuff'
        },
        'develop': {
            'ace86a1': 'Did some stuff',
            '7b6aafb': 'Did some more stuff',
            '7395bb9': 'Final commit',
            '5df40e4': 'Final final commit',
            'dedccf8': 'It works now, I promise!',
        },
        'feature/kelvin': {
            'ace86a1': 'Did some stuff',
            '7b6aafb': 'Did some more stuff',
            '7395bb9': 'Final commit',
            '3106788': 'Implemented kelvin measurement'
        }
    },
    'Humidity sensor repository': {
        'master': {
            '84d70a7': 'Initial commit',
            '45bb7d1': 'Added .gitignore'
        },
    }
}
repo_map = {}
branch_map = {}
commit_map = {}

# Build the concrete ontology
# Basically just iterate over the map and create triplets from it
for repo_name in repos:
    repo_name_internal = repo_name.replace(' ', '_')
    repo = BUILD['/repository/%s' % repo_name_internal]
    g.add((repo, RDF.type, BUILD.repository))
    g.add((repo, RDFS.label, Literal(repo_name)))
    repo_map[repo_name] = repo

    branches = repos[repo_name]
    for branch_name in branches:
        branch = BUILD['repository/%s/branch/%s' % (repo_name_internal, branch_name)]
        g.add((branch, RDF.type, BUILD.branch))
        g.add((branch, BUILD.branchIn, repo))
        g.add((branch, RDFS.label, Literal(branch_name)))
        branch_map[branch_name] = branch

        commits = branches[branch_name]
        for commit_id in commits:
            commit = BUILD['repository/%s/branch/%s/commit/%s' % (repo_name_internal, branch_name, commit_id)]
            g.add((commit, RDF.type, BUILD.commit))
            g.add((commit, BUILD.commitTo, branch))
            g.add((commit, BUILD.hasId, Literal(commit_id)))
            g.add((commit, RDFS.label, Literal(commits[commit_id])))
            commit_map[commit_id] = commit

# Create a sensor which is running a certain commit
sensor = BUILD['sensor/0']
g.add((sensor, RDF.type, BRICK.Temperature_Sensor))
g.add((sensor, RDFS.label, Literal('Sensor 0')))
g.add((sensor, BUILD.runningCodeFrom, commit_map['5df40e4']))

# Spill to file and recreate graph before querying
g.serialize(TTL_FILENAME, 'turtle')
del g
g = Graph()
g.parse(TTL_FILENAME, format='turtle')

# Query to see what branches the commit with id "7395bb9" exists on
q_commit = \
    '''
    SELECT DISTINCT ?branch_name ?commit_message
    WHERE {
        ?branch     rdf:type        build:branch .
        ?branch     rdfs:label      ?branch_name .
        
        ?commit     rdf:type        build:commit .
        ?commit     build:hasId     "7395bb9" .
        ?commit     rdfs:label      ?commit_message .
        ?commit     build:commitTo  ?branch
    }
    '''
pprint(query(g, q_commit))

# Query to find out which repository and branch our sensor is running code from
q_buildinfo = \
    '''
    SELECT DISTINCT ?repo_name ?branch_name ?commit_id ?commit_message
    WHERE {
        ?repo       rdf:type                    build:repository .
        ?repo       rdfs:label                  ?repo_name .
        
        ?branch     rdf:type                    build:branch .
        ?branch     build:branchIn              ?repo .
        ?branch     rdfs:label                  ?branch_name .
        
        ?commit     rdf:type                    build:commit .
        ?commit     build:commitTo              ?branch .
        ?commit     build:hasId                 ?commit_id .
        ?commit     rdfs:label                  ?commit_message .
        
        ?sensor     rdf:type                    brick:Temperature_Sensor .
        ?sensor     build:runningCodeFrom       ?commit .
    }
    '''
pprint(query(g, q_buildinfo))
