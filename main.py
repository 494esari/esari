
from datetime import datetime

from fastapi import FastAPI, Response
from pydantic import BaseModel

import sqlite3


con = sqlite3.connect("todos.sqlite", check_same_thread=False)


sql_create_todo_table = "CREATE TABLE IF NOT EXISTS todo(id INTEGER PRIMARY KEY, title VARCHAR, description VARCHAR, done INTEGER, created_at INTEGER)"


with con:
    con.execute(sql_create_todo_table)

class TodoItem(BaseModel):
    id: int       
    title: str    
    done: bool
    
    description: str 
    created_at: int 


class NewTodoItem(BaseModel):
    title: str
    description: str

app = FastAPI()

# Suljetaan tietokantatyhteys kun fastapi palvelin sammutetaan
@app.on_event("shutdown")
def database_disconnect():
    con.close()

@app.get('/todos')
def get_todos(done: bool | None = None):
    if done != None:
        return f"Tässä palautetaan myöhemmin todot joiden done status on: {done}"
    return "Tässä palautetaan myöhemmin todo-lista"

@app.get('/todos/{id}')
def get_todo_by_id(id:int):
    todo_item = TodoItem(id=id, title="testi", done=False)
    return todo_item

@app.post('/todos')
# Vaihdetaan TodoItem -> NewTodoItem
# Lisätään uusi parametri response jonka tietotyypiksi asetetaan Response luokka.
# response parametrin tietoja muokkaamalla voidaan lisätä responseen esimerkiksi räätälöityjä
# HTTP- headereita tai muuttaa responsen statuskoodia
def create_todo(todo_item: NewTodoItem, response: Response):

    # Tietokantakysely voi epäonnistua joten mahdollisen virheen tapahtuessa try-except
    # ottaa virheestä "kopin" jonka jälkeen voidaan palauttaa sopiva virheviesti 
    # clientille.
    try:
        # Otetaan tietokantayhteys käyttöön
        with con:
            # Luodaan aikaleima (Aikaleima on tässä kuluneet sekunnit vuodesta 1970 https://en.wikipedia.org/wiki/Unix_time).
            dt = datetime.now()
            ts = int(datetime.timestamp(dt))

            # Suoritetaan parametrisoitu tietokantakysely jolla luodaan uusi rivi todo kantaan.
            # Koska (todo_item.title, todo_item.description, int(False), ts,) on tyyppiä Tuple niin 
            # viimeinen pilkku ts:n jälkeen on tarpeellinen!
            # HUOM! Kun teet omia ratkaisuja koodiin niin katso että sql kyselyn 
            # parametrit menevät oikeille paikoille tuplessa!
            cur = con.execute("INSERT INTO todo(title, description, done, created_at) VALUES(?, ?, ?, ?)", (todo_item.title, todo_item.description, int(False), ts,))
            
            # Asetetaan responsen statuskoodiksi 201 eli created
            response.status_code = 201
        
            # Jotta ylimääräiseltä tietokantakyselyltä vältytytään niin voidaan palauttaa uusi TodoItem
            # tiedossa olevilla arvoilla jotka tiedetään nyt olevan samat myös tietokannassa.
            # cur.lastrowid sisältää luodun todo:n id:n tietokannasta.
            return TodoItem(id=cur.lastrowid, title=todo_item.title, done=False, description=todo_item.description, created_at=ts)
            
    except Exception as e:

        # Jos tietokantakysely epäonnistuu kerrotaan siitä tässä clientille asettamalla responselle 
        # sopiva statuskoodi, esim. 500 
        response.status_code = 500
        # Palautetaan virhe clientille
        return {"err": str(e)}
    
@app.put('/todos/{id}')
def update_todo(id: int, todo_item: TodoItem):
    return f"Myöhemmin tässä korvataan tietokannassa olevaa todoitem uudella jonka id on {id}"

@app.patch('/todos/{id}')
def update_todo_status(id: int, todo_item: TodoItem):
    return f"Myöhemmin tässä muokataan tietokannassa olevaa todoitemiä jonka id on {id}"

@app.delete('/todos/{id}')
def delete_todo(id:int):
    return f"Myöhemmin tässä poistetaan tietokannasta todoitem jonka id on {id}"
