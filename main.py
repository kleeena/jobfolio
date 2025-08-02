from fastapi import Depends, FastAPI, HTTPException, Query

from app.startup import lifespan
from api.users import router
from api.job_application import router as JBRouter
from api.resume import router as ResumeRouter

app = FastAPI(lifespan=lifespan)
app.include_router(router=router)
app.include_router(JBRouter)
app.include_router(ResumeRouter)

@app.get('/home')
async def home():
    pass