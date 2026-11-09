from datetime import date
from fastapi import FastAPI
from pydantic import BaseModel,Field
from .engine import Cost,analyse

app=FastAPI(title='CloudScope FinOps API',version='0.1.0')

class CostPayload(BaseModel):
    date:date
    account:str=Field(min_length=1,max_length=100)
    service:str=Field(min_length=1,max_length=100)
    amount:float=Field(ge=0,le=1_000_000_000)

class AnalyseRequest(BaseModel):
    costs:list[CostPayload]=Field(min_length=1,max_length=50000)
    history_days:int=Field(default=7,ge=3,le=90)
    forecast_days:int=Field(default=7,ge=1,le=90)

@app.get('/healthz')
def health():return {'status':'ok'}

@app.post('/v1/analyse')
def report(payload:AnalyseRequest):
    return analyse([Cost(**x.model_dump()) for x in payload.costs],payload.history_days,payload.forecast_days)
