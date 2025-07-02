from pydantic import BaseModel

class Address(BaseModel):
    city:str
    state:str
    pin:str

class Patient(BaseModel):
    name:str
    gender:str
    age:int
    address:Address

address_dict={'city':'gutgaon','state':'haryana','pin':'1220001'}
address1=Address(**address_dict)
patient_dict={'name':'samm','gender':'male','age':35,'address':address1}
patient2=Patient(**patient_dict)
print(patient2)
