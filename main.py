from fastapi import Depends, FastAPI, HTTPException, Query
from app.startup import lifespan
from app.users import router
from app.job_application import router as JBRouter
from app.resume import router as ResumeRouter

app = FastAPI(lifespan=lifespan)
app.include_router(router=router)
app.include_router(JBRouter)
app.include_router(ResumeRouter)

@app.get('/home')
async def home():
    pass