from fastapi import FastAPI, HTTPException
import dockstring
import jsonpickle


app = FastAPI()

@app.get("/")
async def dock(target: str, smiles: str, return_mol: bool = False):

    try:
        docking_output = dockstring.load_target(target).dock(smiles)
    except Exception as e:
        print(e)
        raise HTTPException(status_code=400, detail=str(e))
    
    score, details = docking_output

    if return_mol:
        details["ligand"] = jsonpickle.encode(details["ligand"])
    else:
        details["ligand"] = None

    return {
        "score": score,
        "details": details
    }
