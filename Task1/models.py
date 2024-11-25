from sqlalchemy import Column,Integer,String,Float
from .database import Base1,Base2


class User(Base1):
    __tablename__="users"
    id=Column(Integer,primary_key=True,index=True)
    username=Column(String,index=True)
    phone=Column(String)
    gen=Column(String)
    balance=Column(Float)
    
class Service(Base2):
    __tablename__="services"
    id=Column(Integer,primary_key=True,index=True)
    client_id=Column(Integer,index=True)
    category=Column(String,index=True)
    types=Column(String)
    summapay=Column(Float)
    ispaid=Column(String)
    
    def get_client(self,session):
        return session.query(User).filter(User.id==self.client_id).first()
        


        

    