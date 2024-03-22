from fastapi import FastAPI, status
from pydantic import BaseModel
from fastapi.responses import JSONResponse

#http://127.0.0.1:8000/docs
#для запуска
#uvicorn main:app --reload

description = """
## Издания

* Вы можете получить информацию о всех издания;
* Вы можете создать запись об издании;
* Вы можете получить информацию об одном издании;
* Вы можете обносить информацию об одном издании;
* Вы можете удалить запись об издании;

"""

app = FastAPI(title='Издательство', description=description)

class Edition(BaseModel):
    id: int #код издания
    author: str #автор
    name: str #назание
    printProductType: str #вид печатной продукции
    numbersSheets: int #количество печатных листов
    countEditions: int #количество экземляров


editions = [
    {
        'id': 1, 
        'author':'Джордж Оруэлл', 
        'name':'1984', 
        'printProductType':'Книжный', 
        'numbersSheets': 320, 
        'countEditions': 1500
     },

    {
        'id': 2, 
        'author':'О.Зимина', 
        'name': 'Самоучитель игры на фортепиано', 
        'printProductType':'Нотный', 
        'numbersSheets': 150, 
        'countEditions': 800
     },

    {
        'id': 3, 
        'author':'', 
        'name':'Glamour', 
        'printProductType':'Журнальный', 
        'numbersSheets': 80, 
        'countEditions': 2100
     }
]

@app.get("/editions", tags=['Издания'], status_code=200)
def get_editions():
    return editions

@app.get("/editions/{id}", tags=['Издания'], status_code=200)
def get_edition(id: int):
    edition = next((edition for edition in editions if edition['id'] == id), None)
    if edition:
        return edition
    return JSONResponse(
        status_code = status.HTTP_404_NOT_FOUND,
        content = {'message': 'Еdition is not found'})

@app.post("/editions", tags=['Издания'], status_code=201)
def create_edition(Edition: Edition):
    new_edition = {
        'id': len(editions)+1,
        'author': Edition.author, 
        'name': Edition.name, 
        'printProductType': Edition.printProductType, 
        'numbersSheets': Edition.numbersSheets, 
        'countEditions': Edition.countEditions
    }
    editions.append(new_edition)
    return new_edition


@app.put("/editions/{id}", tags=['Издания'], status_code=200)
def update_edition(id: int, Edition: Edition):
    edition = next((edition for edition in editions if edition['id'] == id), None)
    if edition:
        #edition['id'] = Edition.id
        edition['author'] = Edition.author
        edition['name'] = Edition.name
        edition['printProductType'] = Edition.printProductType
        edition['numbersSheets'] = Edition.numbersSheets
        edition['countEditions'] = Edition.countEditions
        return edition
    return JSONResponse(
        status_code = status.HTTP_404_NOT_FOUND,
        content = {'message': 'Еdition is not found'})

@app.delete("/editions/{id}", tags=['Издания'], status_code=200)
def delete_edition(id: int):
    global editions
    edition = next((edition for edition in editions if edition['id'] == id), None)
    if edition:
        editions = [edition for edition in editions if edition['id'] != id]
        return {'message': 'Еdition deleted'}
    return JSONResponse(
        status_code = status.HTTP_404_NOT_FOUND,
        content = {'message': 'Еdition is not found'})
