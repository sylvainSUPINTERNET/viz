import pprint

'''
Create Nodes labels
'''
def proccess_label(profiles_cursor, labels):
    response = {}
    for label in labels:
        response[label] = set()


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
            else:
                response[i].add(profile[i])
    # pprint.pprint(response)
    return response