from fastapi import FastAPI
from .database import get_db1,get_db2
from .router import router as useserv_router
from .database import get_db1,get_db2


app=FastAPI()
get_db1()
get_db2()
app.include_router(useserv_router)

