from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uuid
import subprocess
from pydantic import BaseModel

app = FastAPI()

origins = [
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

resources = {
    "dgx01": {
        "gpu": {
            "1g.10gb": 4,
            "7g.80gb": 3,
        },
        "cpu": 256,
        "memory": 2048
    }
}

@app.get("/")
async def root():
    return {"message": "success"}

class AllocateBody(BaseModel):
    gpuSpec: str
    gpuInstance: int

@app.post("/allocate")
async def allocate():
    id = uuid.uuid4()
    cmds = ['./job.sh']
     
    result = subprocess.run(cmds, stdout=subprocess.PIPE, shell=True)

    return {
        "message": "success",
        "id": id,
        "stdout": result.stdout
    }
