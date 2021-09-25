import pprint

'''
Create Nodes labels
'''
def proccess_label(profiles_cursor, labels):
    response = {}
    
    build_relation = [];

    for label in labels:
        response[label] = set()

    # MATCH (a:age), (b:music) WHERE a.value = '<AGE>' AND b.value = 'PROFILE_MUSICIAN' CREATE (a)-[r:LISTEN]->(b) RETURN type(r);
    for profile in profiles_cursor:
        for i in response:
            if type(profile[i]) is list:
                if len(profile[i]) > 0:
                    for obj in profile[i]:
                        for key in obj:
                            if key == "name":
                                response[i].add(obj[key])
                            if key == "artistName":
                                response[i].add(obj[key])
                                build_relation.append(f"MATCH (a:age), (b:musics) WHERE a.value ='"+ profile["age"] +"' AND b.value = '"+ obj["artistName"] +"' CREATE (a)-[r:LISTEN]->(b) RETURN type(r)")
            else:
                response[i].add(profile[i])
    #  pprint.pprint(response)
    return [response, build_relation]