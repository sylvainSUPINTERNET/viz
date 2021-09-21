import pprint
class ProfileRepository:
    def __init__(self, db, collectionName):
        self.db = db;
        self.collectionName = collectionName;
        self.collection = db[f"{collectionName}"]

    '''
    Extract interessting values to build neo4j nodes
    '''
    def find_all_and_extract_nodes(self):
       return self.collection.find({});
         
        
    
