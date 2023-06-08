from fastapi import FastAPI

app = FastAPI()

@app.get('/todos')
def get_todos(done: bool | None = None):
    if done != None:
        return f"Tässä palautetaan myöhemmin todot joiden done status on: {done}"
    return "Tässä palautetaan myöhemmin todo-lista"

@app.get('/todos/{id}')
def get_todo_by_id(id:int):
    return f"Tässä palautetaan myöhemmin yksittäinen todo item id:llä {id}"
