# Tuodaan FastAPI luokka fastapi paketista
from fastapi import FastAPI

# Luodaan uusi fastapi instanssi app nimiseen muuttujaan.
# Muuttujan nimellä on merkitystä sillä uvicorn tarvitsee tämän 
# nimen palvelinta käynnistäessä, tässä tapauksessa se on main:app
app = FastAPI()

# Käytetään fastapi:n @app.get dekoraattoria todos endpointin luomiseen.
# Decorator funktio suoritetaan aina ennen sen alapuolella olevaa funktiota
# Decorator välittää sen alapuolelle määritetylle funktiolle argumentteja. 
# Tässä tapauksessa turvaudutaan FastAPI:n dokumentaatioon jotta tiedetään mitä
# argumentteja dekoraattorin alapuolella oleva 
# funktio ottaa vastaan missäkin tapauksessa.
@app.get('/todos')
def getTodos():
    return "Tässä palautetaan myöhemmin todo-lista"
