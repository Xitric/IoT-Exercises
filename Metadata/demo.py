from rdflib import Literal

from wrapper import *

TTL_FILENAME = 'turtle/building.ttl'

g = model()

###############################################################################
################################################################# building ####

building = N['/building']
g.add((building, RDF.type, BRICK['Building']))

###############################################################################
################################################################### floors ####

floors = []
for floor_number in range(2):
    floor = N['building/floors/%u' % floor_number]
    g.add((floor, RDF.type, BRICK['Floor']))
    g.add((building, BRICK.contains, floor))
    floors.append(floor)

###############################################################################
############################################################# room mapping ####

rooms = {
    'room 1': {
        'floor': 0,
        'temp-sensor': 'd0fcec33-af08-44a8-b74b-7a51f1902d13',
        'temp-actuator': '5c2e2bdb-5142-464d-ad91-ae483633dfd6',
        'temp-setpoint': 'c087d1ba-03f6-4c60-85de-b95d82e63248',
    },
    'room 2': {
        'floor': 1,
        'temp-sensor': '18407632-8e81-4bb9-ae77-4ecc96f30f46',
        'temp-actuator': 'ec883cad-3235-46d5-a901-7bae169dda0a',
        'temp-setpoint': 'd2b54605-58b1-44ef-89f9-0a9adabbfbb1',
    },
    'room 3': {
        'floor': 1,
        'temp-sensor': 'e528f733-2e3a-4f65-93aa-6fb2e36d4b27',
        'temp-actuator': '9be52aed-0e12-49b5-8680-47778b9b2adf',
        'temp-setpoint': 'd2b54605-58b1-44ef-89f9-0a9adabbfbb1',
    },
}

###############################################################################
#################################################################### rooms ####

roommap = {}
for roomname in rooms:
    data = rooms[roomname]
    room = N['building/rooms/%s' % roomname.replace(' ', '_')]
    g.add((room, RDF.type, BRICK['Room']))
    g.add((room, BRICK.label, Literal(roomname)))
    g.add((floors[data['floor']], BRICK.contains, room))
    roommap[roomname] = room

###############################################################################
####################################################### temperature points ####

for roomname in rooms:
    data = rooms[roomname]
    room = roommap[roomname]

    sensor = N['building/rooms/%s/temp-sensor' % roomname.replace(' ', '_')]
    g.add((sensor, RDF.type, BRICK['Temperature_Sensor']))
    g.add((sensor, BRICK.label, Literal(data['temp-sensor'])))
    g.add((sensor, BRICK.pointOf, room))

    setpoint = N['building/rooms/%s/temp-setpoint' % roomname.replace(' ', '_')]
    g.add((setpoint, RDF.type, BRICK['Temperature_Setpoint']))
    g.add((setpoint, BRICK.label, Literal(data['temp-setpoint'])))
    g.add((setpoint, BRICK.pointOf, room))

    actuator = N['building/rooms/%s/temp-actuator' % roomname.replace(' ', '_')]
    g.add((actuator, RDF.type, BRICK['Radiator_Valve_Position']))
    g.add((actuator, BRICK.label, Literal(data['temp-actuator'])))
    g.add((actuator, BRICK.pointOf, room))

###############################################################################
########################## store-load cycle to simulate applications split ####

g.serialize(TTL_FILENAME, 'turtle')
del g
g = Graph()
g.parse(TTL_FILENAME, format='turtle')

###############################################################################
########################################################### dashbard query ####

q_dashboard = \
    '''
    SELECT DISTINCT ?room_name ?sensor_uuid
    WHERE {
        ?room     rdf:type/brick:subClassOf* brick:Room .
        ?sensor   rdf:type/brick:subClassOf* brick:Temperature_Sensor .
        
        ?sensor   brick:pointOf ?room .
        
        ?room     brick:label ?room_name .
        ?sensor   brick:label ?sensor_uuid .
    }
    '''
pprint(query(g, q_dashboard))

###############################################################################
######################################################### thermostat query ####

q_thermostat = \
    '''
    SELECT DISTINCT ?room_name ?sensor_uuid ?setpoint_uuid ?actuator_uuid
    WHERE {
        ?room     rdf:type/brick:subClassOf* brick:Room .
        ?sensor   rdf:type/brick:subClassOf* brick:Temperature_Sensor .
        ?setpoint rdf:type/brick:subClassOf* brick:Temperature_Setpoint .
        ?actuator rdf:type/brick:subClassOf* brick:Radiator_Valve_Position .
        
        ?sensor   brick:pointOf ?room .
        ?setpoint brick:pointOf ?room .
        ?actuator brick:pointOf ?room .
        
        ?room     brick:label ?room_name .
        ?sensor   brick:label ?sensor_uuid .
        ?setpoint brick:label ?setpoint_uuid .
        ?actuator brick:label ?actuator_uuid .
    }
    '''
pprint(query(g, q_thermostat))

###############################################################################
################################################################### update ####

q_update = \
    '''
    DELETE {
        ?actuator brick:label "ec883cad-3235-46d5-a901-7bae169dda0a" .
    }
    WHERE {
        ?actuator rdf:type/brick:subClassOf* brick:Radiator_Valve_Position .
        ?actuator brick:label "ec883cad-3235-46d5-a901-7bae169dda0a" .
    }
    '''
update(g, q_update)

###############################################################################
################################################## repeat thermostat query ####

pprint(query(g, q_thermostat))

###############################################################################
###############################################################################
