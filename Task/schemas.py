from pydantic import BaseModel
from typing import Optional

class UserBase (BaseModel):
    username:str
    phone:str
    gen:str
    balance:float
class UserCreate(UserBase):
    pass
class User(UserBase):
    id:int
    
   
class ServiceBase (BaseModel):
    category:str
    types:str
    summapay:float
    ispaid:Optional[str]=None
    client_id:int
    
class ServiceCreate(ServiceBase):
    pass
class ServiceResponse(ServiceBase):
    id:int
    
    
    
    
    
    