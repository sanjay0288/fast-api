from fastapi import FastAPI, Depends, HTTPException
from application.auth import  get_current_user
from application.data import get_dummy_data

app = FastAPI()
@app.get("/health")
def health_check():
    return {"status": "ok"}
@app.get("/data")
def get_data(user:dict=Depends(get_current_user)):
    try:
        return{"user": user, "data": get_dummy_data()}
    except Exception as e:
        raise HTTPException(status_code=500, details=str(e))
