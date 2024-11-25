from fastapi import FastAPI,HTTPException,Depends
from sqlalchemy.orm import Session
from .models import User,Service,Base1,Base2
from .database import engine1,engine2,session_local1,session_local2
from .schemas import UserCreate,User as UserDb,ServiceCreate


app=FastAPI()
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

Base1.metadata.create_all(bind=engine1)
Base2.metadata.create_all(bind=engine2)
   
   



@app.post("/users",response_model=UserDb)
async def create_user(user:UserCreate,db:Session=Depends(get_db1))->User:
    db_user=User(username=user.username,phone=user.phone,gen=user.gen,balance=user.balance)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

@app.post("/service")
async def create_service(serv:ServiceCreate,servdb:Session=Depends(get_db2),userdb:Session=Depends(get_db1)):
    db_serv=Service(category=serv.category,types=serv.types,summapay=serv.summapay,ispaid=serv.ispaid,client_id=serv.client_id)
    user=userdb.query(User).filter(User.id==serv.client_id).first()
    if user is None:
        raise HTTPException(status_code=404,detail="Клиент не найден")
    if serv.category.lower()=="расходы" and db_serv.summapay>0:
        if user.balance<db_serv.summapay:
            return{"message":"У вас недостаточно средств"}
        user.balance-=db_serv.summapay
        userdb.commit()
        userdb.refresh(user)
    if serv.category.lower()=="доходы" and db_serv.summapay>0:
        user.balance+=serv.summapay
        userdb.commit()
        userdb.refresh(user)
    db_serv.ispaid="Оплачено"
    servdb.add(db_serv)
    servdb.commit()
    servdb.refresh(db_serv)
    return db_serv
        

    
@app.get("/service_pay")
async def print_service_pay_status(userdb:Session=Depends(get_db1),servdb:Session=Depends(get_db2)):
    user=userdb.query(User).all()
    serv=servdb.query(Service).all()
    if user is None and serv is None:
        raise HTTPException(status_code=404,detail="Client and Service pay info not found")
  
    return {"client":user,"services":serv}
    
