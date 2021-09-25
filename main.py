import os
from dotenv import load_dotenv

load_dotenv()

MONGO_USER = os.getenv('MONGO_USER')
MONGO_PASSWORD = os.getenv('MONGO_PASSWORD')

NEO_CLUSTER = os.getenv('NEO_CLUSTER')
NEO_USER = os.getenv('NEO_USER')
NEO_PASSWORD = os.getenv('NEO_PASSWORD')


from flask import Flask
from repository.profile_repository import ProfileRepository
from dto.ProfileDto import ProfileDto
from service.PrepareNodesLabel import proccess_label

from pymongo import MongoClient
client = MongoClient(f"mongodb+srv://{MONGO_USER}:{MONGO_PASSWORD}@cluster0.vhh4x.mongodb.net") # do not forget to add your IP in acceptable list of IP in cluster atlas or add 0.0.0.0/0
db = client.bot;

profilesRepo = ProfileRepository(db=db, collectionName="bumbleProfiles");
profiles_cursor = profilesRepo.find_all_and_extract_nodes();

nodes_labels = proccess_label(profiles_cursor, labels=["age", "citiesInfo", "hobbies", "musics"])
build_relation = nodes_labels[1]
nodes_labels = nodes_labels[0]

from neo4j import GraphDatabase
neo_client = GraphDatabase.driver(f"{NEO_CLUSTER}", auth=(f"{NEO_USER}", f"{NEO_PASSWORD}"))



def create_node_tx(tx, label, value):
    result = tx.run("CREATE (n:"+label+" { value: "+value+" } ) RETURN n");
    print(result)

def create_node_relation(tx, query):
    result = tx.run(query)
    print(result)

with neo_client.session() as session:
    for k in nodes_labels:
        node_type = k
        for node_value in nodes_labels[k]:
            node_value = "'"+ node_value + "'"
            print(f"type : {k} <=> {node_value}")
            print(k)
            res = session.write_transaction(create_node_tx, label=k, value=node_value)
            print(res)
    for relation_query in build_relation:
        print(relation_query)
        res = session.write_transaction(create_node_relation,query=relation_query)



# MATCH (a:age), (b:music) WHERE a.value = '<AGE>' AND b.value = 'PROFILE_MUSICIAN' CREATE (a)-[r:LISTEN]->(b) RETURN type(r);

# def create_node_tx(tx, name, profiles_cursor):
#     #result = tx.run("CREATE (n:NodeExample { name: $name }) RETURN id(n) AS node_id", name=name)
#     for profile in profiles_cursor:
#         profileDto = ProfileDto(name=profile["name"]);

#         result = tx.run("CREATE (n:Person {name: $name }) RETURN id(n) AS node_id", name=profileDto.name)
#         record = result.single()
#         print(record["node_id"])
#     return 1;

# with neo_client.session() as session:
#     node_id = session.write_transaction(create_node_tx, "example", profiles_cursor=profiles_cursor)

# def get_node(tx, node_type, value):
#     result = tx.run(f"MATCH (n:{node_type}) RETURN id(n), n.value");
#     for record in result:
#         print(record["node_id"]);
#         print(record["value"]);
#     return 1;

# with neo_client.session() as session:
#     node_id = session.write_transaction(get_node, node_type="Age", value=24)


#neo_client.close()

app = Flask(__name__)

@app.route("/")
def hello():
    return "Hello World!"

if __name__ == "__main__":
    app.run()