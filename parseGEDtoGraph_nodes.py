#! Python3

import os
import pprint
from neo4j import GraphDatabase, basic_auth

def log_query(func):
    def wrapper(*args, **kwargs):
        print(f'{args[1]}')
        result = func(*args, **kwargs)
        print(f'Result: {result}')
    return wrapper

@log_query
def update_graph_db(query, parameters):
    session.run(query, parameters=parameters)


driver = GraphDatabase.driver(
    "bolt://35.153.194.5:35960",
    auth=basic_auth("neo4j", "pot-cans-multimeter"))
session = driver.session()

GEDFile = open(os.path.join(os.getcwd(),"data","sample.GED"), encoding="ISO-8859-1")
content = GEDFile.readlines()


currentID = ''
lastTag = ''
listnum = 1
famnum = 0
fam = ''

node_query = '''
WITH {person} as person
MERGE (p:Person {id:person[0],name:person[1],sex:person[2]})
'''

node_property_birthdate_query = '''
WITH {property} as property
MATCH (p:Person {id:property[0]})
SET p.birth_date=property[1]
'''

node_property_deathdate_query = '''
WITH {property} as property
MATCH (p:Person {id:property[0]})
SET p.death_date=property[1]
'''

rel_query = '''
UNWIND {relationship} as rel
MATCH (p {id:rel[0]})
MATCH (c {id:rel[1]})
MERGE (p)-[:HAS_CHILD]->(c)
'''


for i in range(len(content)):
    line = content[i].strip()
    if line[0] == '0' and line[-4:] == 'INDI':
        event = 'INDI'
        birthCount = 0
        deathCount = 0
        indiID = line[3:9]
        data = [indiID]
    elif line[:6] == '1 NAME':
        data.append(line[7:])
    elif line[:5] == '1 SEX':
        data.append(line[6])
        parameters = {"person": data}
        update_graph_db(node_query, parameters)
        data = []
    elif line[:6] == '1 BIRT':
        birthCount += 1
        label = 'BIRT'
    elif line[:6] == '1 DEAT':
        deathCount += 1
        label = 'DEAT'
    elif line[:6] == '2 DATE':
        date = line[7:len(line)]
        if label == 'BIRT':
            if birthCount == 1:
                data = [indiID, date]
                parameters = {"property": data}
                update_graph_db(node_property_birthdate_query, parameters)
                data = []
        if label == 'DEAT':
            if deathCount == 1:
                data = [indiID, date]
                parameters = {"property": data}
                update_graph_db(node_property_deathdate_query, parameters)
                data = []
    # elif[:5 == '2 PLAC':
    #     if label == 'DEAT' and deathCount == 1:
    #        data=[[indiID],["death_"],[date]]
    #       session.run(node_property_query, parameters={person_property: data})

GEDFile.close()
print('Import Complete')
# pprint.pprint(person)
# print(person[10])