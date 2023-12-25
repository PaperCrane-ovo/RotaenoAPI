import fastapi 

from typing import Union
from pydantic import BaseModel
import chart
from examinetoken import check_token


app = fastapi.FastAPI()
chartlist = chart.ChartList()

@app.get('/')
async def root():
    return {"message":"Hello!"}

@app.get('/rotaeno/search/byalias/{alias}')
async def search(alias:str):
    return_value = chartlist.get_song_by_alias(alias)
    if return_value is None:
        return {"message":"Not Found Song by Alias"}
    return {"message":"OK","data":return_value}

@app.get('/rotaeno/search/byid/{id}')
async def search(id:str):
    return_value = chartlist.get_song_by_id(id)
    if return_value is None:
        return {"message":"Not Found Song by ID"}
    return {"message":"OK","data":return_value}

@app.get('/rotaeno/search/byname/{name}')
async def search(name:str):
    return_value = chartlist.get_song_by_name(name)
    if return_value is None:
        return {"message":"Not Found Song by Name"}
    return {"message":"OK","data":return_value}

@app.get('/rotaeno/search/{substring}')
async def search(substring:str):
    return_value = chartlist.search_song(substring)
    if return_value is None:
        return {"message":"Not Found Song by Substring"}
    return {"message":"OK","data":return_value}

@app.get('/rotaeno/list')
async def list():
    return_value = chartlist.get_song_list()
    return {"message":"OK","data":return_value}

@app.get('/rotaeno/approxsearch/{string}')
async def approxsearch(string:str):
    return_value = chartlist.get_song(string)
    if return_value is None:
        return {"message":"Not Found Song by Approximate Search"}
    return {"message":"OK","data":return_value}

@app.get('/rotaeno/getalias/{id}')
async def getalias(id:str):
    return_value = chartlist.get_alias(id)
    if return_value is None:
        return {"message":"Not Found Alias by ID"}
    return {"message":"OK","data":return_value}

@app.get('/rotaeno/addalias/')
async def addalias(id:str,alias:str,token:str):
    if not check_token(token):
        return {"message":"Wrong Token"}
    chart = chartlist.get_song_by_id(id)
    if chart is None:
        return {"message":"Not Found Song by ID"}
    if alias in chart.alias:
        return {"message":"Already Exist Alias"}
    chart.add_alias(alias)
    return {"message":"OK"}
