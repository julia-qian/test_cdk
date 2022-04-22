from aws_lambda_powertools.event_handler import AppSyncResolver

app = AppSyncResolver() #lambda handler

@app.resolver(type_name="Mutation", field_name="createNote")    # registers function
def create_note(note):                                          # generic python functions
    return {"id": "111", "name": "Alice", "note": "Lambda1 createNote!"}

@app.resolver(type_name="Mutation", field_name="updateNote")
def update_note(id: str):
    return {"id": "222", "note": "Lambda2 updateNote!"}

@app.resolver(type_name="Query", field_name="listNotes")
def list_notes():
    return [{"id": "333", "note": "Lambda3 listNotes!"}]
