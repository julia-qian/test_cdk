def lambda1_handler(event, context=None):
    if event["info"]["fieldName"] == "createNote":
        return {"id": "111", "note": "Lambda1 createNote!"}
    else:
        return {"id": "112", "note": "Lambda1 Error!"} 

def lambda2_handler(event, context=None):
    if event["info"]["fieldName"] == "updateNote":
        return {"id": "222", "note": "Lambda2 updateNote!"}
    else:
        return {"id": "223", "note": "Lambda2 Error!"} 

def lambda3_handler(event, context=None):
    print(event)
    if event["info"]["fieldName"] == "listNotes":
        return [{"id": "333", "note": "Lambda3 listNotes!"}]
    else:
        return [{"id": "334", "note": "Lambda2 Error!"}]