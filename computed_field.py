from pydantic import BaseModel,EmailStr,AnyUrl,Field,computed_field
from typing import List,Dict,Optional,Annotated
#learning pydantic
class Patient(BaseModel):
    name: Annotated[str,Field(max_length=100,title='name of the patient',description='GIve the name of the patient in less than 50 chars', examples=['Nitish','Amit'])]
    email:EmailStr
    age: int=Field(gt=0,lt=100)
    linkedin_url=AnyUrl
    weight:Annotated[float,Field(gt=0,strict=True)]
    married:bool
    allergies:Optional[List[str]]=None
    contact_details:Dict[str,str]
    @computed_field
    @property
    def bmi(self)->float:
        bmi=round(self.weight/(self.height**2),2)
        return bmi
    


    

def insert_patient_data(patient: Patient):
    print(f"Inserting patient: {patient.name}, {patient.age}")
    print('inserted')

def update_patient_data(patient: Patient):
    print(f"Updating patient: {patient.name}, {patient.age}")
    print('BMI',patient.bmi)
    print('updated')

# Insert patient
patient_info = {'name': 'hitesh', 'age': 30,'weight':50,'married':True,'allergies':['pollen','peanut'],'contact_details':{'email':'saisha@gmail.com','phone':'9825667788'}}
patient1 = Patient(**patient_info)
insert_patient_data(patient1)

# Update patient
patient_info = {'name': 'nitesh', 'age': 31}
patient2 = Patient(**patient_info)
update_patient_data(patient2)
