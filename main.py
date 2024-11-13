from typing import Union

from fastapi import FastAPI, HTTPException

app = FastAPI()


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    if item_id < len(items):
        return {"item_id": item_id, "q": q}
    else:
        raise HTTPException(status_code=404, detail="Item not found")

