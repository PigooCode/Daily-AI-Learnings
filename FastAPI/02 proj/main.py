from fastapi import FastAPI , Path , Query , HTTPException
import json
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field , computed_field
from typing import Annotated

def load_data():
    with open("patients.json", "r") as f:
        data = json.load(f)
        return data

def save_data(data):
    with open("patients.json", "w") as f:
        json.dump(data, f)
    
class Patient(BaseModel):
    
    id: Annotated[str, Field(...,description="Patient ID")]
    name: Annotated[str, Field(...,description="Patient Name")]
    age: Annotated[int, Field(...,gt=0,description="Patient Age")]
    weight: Annotated[float, Field(...,gt=0,description="Patient Weight")]
    height: Annotated[float, Field(...,gt=0,description="Patient Height")]

    @computed_field
    @property
    def bmi(self) -> float:
        return round(self.weight / (self.height / 100) ** 2, 2)


app = FastAPI()

@app.get("/view_patients")
def get_patients():
    return load_data()

@app.post("/add_patient")
def add_patient(patient: Patient):
    
    data = load_data()
    
    if patient.id in data:
        raise HTTPException(status_code=400, detail="Patient ID already exists")

    data[patient.id] = patient.model_dump(exclude={"id"})
    save_data(data)
    return JSONResponse(content={"message": "Patient added successfully"}, status_code=201)

