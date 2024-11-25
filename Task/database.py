from sqlalchemy.ext.asyncio import AsyncSession,create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base


engine1=create_async_engine('sqlite+aiosqlite:///clientserver.db',echo=True)
engine2=create_async_engine('sqlite+aiosqlite:///serviceserver.db',echo=True)
session_local1=sessionmaker(engine1,class_=AsyncSession,expire_on_commit=False)
session_local2=sessionmaker(engine2,class_=AsyncSession,expire_on_commit=False)
Base1=declarative_base()
Base2=declarative_base()



async def get_db1():
    db=session_local1()
    try:
        yield db
    finally:
        db.close()
        
async def get_db2():
    db=session_local2()
    try:
        yield db
    finally:
        db.close()
    



        



    


    
    
    
    