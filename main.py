import os
from dotenv import load_dotenv
load_dotenv()

MONGO_USER = os.getenv('MONGO_USER')
MONGO_PASSWORD = os.getenv('MONGO_PASSWORD')

from flask import Flask
from repository.profile_repository import ProfileRepository
from dto.ProfileDto import ProfileDto

from pymongo import MongoClient
client = MongoClient(f"mongodb+srv://{MONGO_USER}:{MONGO_PASSWORD}@cluster0.vhh4x.mongodb.net") # do not forget to add your IP in acceptable list of IP in cluster atlas or add 0.0.0.0/0
db = client.bot;

profilesRepo = ProfileRepository(db=db, collectionName="bumbleProfiles");
profiles_cursor = profilesRepo.find_all_and_extract_nodes();

from neo4j import GraphDatabase
neo_client = GraphDatabase.driver(f"{NEO_CLUSTER}", auth=(f"{NEO_USER}", f"{NEO_PASSWORD}"))

def create_node_tx(tx, name, profiles_cursor):
    #result = tx.run("CREATE (n:NodeExample { name: $name }) RETURN id(n) AS node_id", name=name)
    for profile in profiles_cursor:
        profileDto = ProfileDto(name=profile["name"]);

        result = tx.run("CREATE (n:Person {name: $name }) RETURN id(n) AS node_id", name=profileDto.name)
        record = result.single()
        print(record["node_id"])
    return 1;

with neo_client.session() as session:
    node_id = session.write_transaction(create_node_tx, "example", profiles_cursor=profiles_cursor)


#neo_client.close()

app = Flask(__name__)

@app.route("/")
def hello():
    return "Hello World!"

if __name__ == "__main__":
    app.run()