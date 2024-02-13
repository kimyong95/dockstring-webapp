# Run: uvicorn main:app

from fastapi import FastAPI, HTTPException
import dockstring
import jsonpickle
from pydantic import BaseModel, Field

app = FastAPI()

class Query(BaseModel):
    target: str
    smiles: str
    return_mol: bool = Field(default=False)

@app.post("/")
async def dock(query: Query):

    try:
        docking_output = dockstring.load_target(query.target).dock(query.smiles)
    except Exception as e:
        print(e)
        raise HTTPException(status_code=400, detail=str(e))
    
    score, details = docking_output

    if query.return_mol:
        details["ligand"] = jsonpickle.encode(details["ligand"])
    else:
        details["ligand"] = None

    return {
        "score": score,
        "details": details
    }
