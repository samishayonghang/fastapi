from fastapi import FastAPI
import json
import os
from fastapi.responses import JSONResponse
from pydantic import BaseModel,Field,computed_field
from typing import Annotated,Optional
from fastapi import FastAPI,Path,HTTPException,Query
app=FastAPI()
DATA_FILE = 'patients.json'

def load_data():
    if not os.path.exists(DATA_FILE)or os.path.getsize(DATA_FILE)==0:
        with open(DATA_FILE,'w') as f:
            json.dump({},f)
    with open('patients.json','r') as f:
        data=json.load(f)
    
    if not isinstance(data,dict):
        data={}
        with open(DATA_FILE,'w') as f:
            json.dump(data,f)
    return data

def save_data(data):
    with open('patients.json','w')as f:
        json.dump(data,f)

class Patient(BaseModel):
    id:Annotated[str,Field(..., description="Id of the patient",examples=['p001'])]
    name:Annotated[str,Field(...,description="name of the patient",examples=['sagun mehta'])]
                   
    age:Annotated[int,Field(..., gt=0,lt=120,description='age of the patient')]

    city:str
    gender:str
    height:float
    weight:float

    @computed_field
    @property
    def bmi(self)->float:
        bmi=round(self.weight/(self.height**2),2)
        return bmi
    

    @computed_field
    @property
    def verdict(self)->str:
        if self.bmi< 18.5:
            return 'underweight'
        
        elif self.bmi<25:
            return 'Normal'
        
        else:
            return 'overweight'
        


@app.post('/create')
def create_patient(patient:Patient):
    data=load_data()

    if patient.id in data:
        raise HTTPException(status_code=400,detail='patient already exist')
    
    data[patient.id]=patient.model_dump(exclude=['id'])
    save_data(data)
    return JSONResponse(status_code=201,content={
            "detail": "Patient created successfully",
            "patient_id": patient.id,
            "bmi": patient.bmi,
            "verdict": patient.verdict
        })


class PatientUpdate(BaseModel):
    name:Annotated[Optional[str], Field(default=None)]
                   
    age:Annotated[Optional[int],Field(default=None)]

    city:Annotated[Optional[str],Field(default=None)]

    gender:Annotated[Optional[str],Field(default=None)]
    
    height:Annotated[Optional[str],Field(default=None)]
    
    weight:Annotated[Optional[str],Field(default=None)]

@app.put('/edit/{patient_id}')
def update_patient(patient_id:str,patient_update:PatientUpdate):
    data=load_data()
    if patient_id not in data:
        raise HTTPException(status_code=404,detail='not found patient')
    
    existing_patientinfo=data[patient_id]
    updated_patientinfo=patient_update.model_dump(exclude_unset=True)
    for key,value in updated_patientinfo.items():
        existing_patientinfo[key]=value
    existing_patientinfo['id']=patient_id

    patient_pydantic_obj=Patient(**existing_patientinfo)
    existing_patientinfo=patient_pydantic_obj.model_dump(exclude='id')
    data[patient_id]=existing_patientinfo
    save_data(data)
    return JSONResponse(
        status_code=200,
        content={
            "detail": "Patient updated successfully",
            "patient_id": patient_pydantic_obj.id,
            "bmi": patient_pydantic_obj.bmi,
            "verdict": patient_pydantic_obj.verdict
        }
    )

@app.delete('/delete/{patient_id}')
def delete_patient(patient_id:str):
    data=load_data()
    if patient_id not in data:
        raise HTTPException(status_code=404,detail='not found the patient')
    del data[patient_id]
    save_data(data)
    return JSONResponse(status_code=200,content={'message':'patient deleted successfully'})




    




