from fastapi import APIRouter,Depends
from .schemas import UserCreate,User as UserDb,ServiceCreate
from sqlalchemy.ext.asyncio import AsyncSession
from .database import get_db1,get_db2
from .models import User,Service
from fastapi import HTTPException,Depends
from sqlalchemy.future import select

router=APIRouter(
    prefix="/api"
)
async def create_user(user:UserCreate,udb:AsyncSession):
    db_user=User(username=user.username,phone=user.phone,gen=user.gen,balance=user.balance)
    udb.add(db_user)
    await udb.commit()
    await udb.refresh(db_user)
    return db_user
    
async def create_service(serv:ServiceCreate,udb:AsyncSession,sdb:AsyncSession):
    db_serv=Service(category=serv.category,types=serv.types,summapay=serv.summapay,ispaid=serv.ispaid,client_id=serv.client_id)
    db_user=await udb.execute(select(User).where(User.id==serv.client_id))
    user=db_user.scalar_one_or_none()
    if user is None:
        raise HTTPException(status_code=404,detail="Клиент не найден")
    if serv.category.lower()=="расходы" and db_serv.summapay>0:
        if user.balance<db_serv.summapay:
            return{"message":"У вас недостаточно средств"}
        user.balance-=db_serv.summapay
        await udb.commit()
        await udb.refresh(user)
    if serv.category.lower()=="доходы" and db_serv.summapay>0:
        user.balance+=serv.summapay
        await udb.commit()
        await udb.refresh(user)
    db_serv.ispaid="Оплачено"
    sdb.add(db_serv)
    await sdb.commit()
    await sdb.refresh(db_serv)
    return db_serv
        
   
async def print_service_pay_status(udb:AsyncSession,sdb:AsyncSession):
    user=select(User)
    serv=select(Service)
    db_user=await udb.execute(user)
    db_serv=await sdb.execute(serv)
    user_res=db_user.scalars().all()
    serv_res=db_serv.scalars().all()
    return {"client":user_res,"services":serv_res}

@router.post("/users",response_model=UserCreate)
async def add_user(user:UserCreate,udb:AsyncSession=Depends(get_db1)):
    return await create_user (user=user,udb=udb)
    
@router.post("/services")
async def add_service(serv:ServiceCreate,udb:AsyncSession=Depends(get_db1),sdb:AsyncSession=Depends(get_db2)):
    return await create_service(serv=serv,udb=udb,sdb=sdb)
    
@router.get("/userservpay",description="Получить список пользователей и их успешных платежей")
async def print_users(udb:AsyncSession=Depends(get_db1),sdb:AsyncSession=Depends(get_db2)):
     return await print_service_pay_status(udb=udb,sdb=sdb)
    

    

 

