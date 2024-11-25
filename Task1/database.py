from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
engine1=create_engine('sqlite:///./clientserver.db')
engine2=create_engine('sqlite:///./serviceserver.db')
session_local1=sessionmaker(autoflush=False,bind=engine1,autocommit=False)
session_local2=sessionmaker(autoflush=False,bind=engine2,autocommit=False)

Base1=declarative_base()
Base2=declarative_base()



    


    
    
    
    