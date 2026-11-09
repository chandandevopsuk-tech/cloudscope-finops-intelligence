from datetime import date,timedelta
from fastapi.testclient import TestClient
from cloudscope.engine import Cost,analyse
from cloudscope.api import app

def test_spike_after_baseline_is_anomaly():
    costs=[Cost(date(2026,1,1)+timedelta(days=i),'account-a','compute',float(v)) for i,v in enumerate([10,12,11,9,10,100])]
    report=analyse(costs)
    assert len(report['anomalies'])==1
    assert report['anomalies'][0]['cost']==100
    assert report['observed_total']==152

def test_account_isolation_and_forecast():
    costs=[Cost(date(2026,1,1),'a','storage',12),Cost(date(2026,1,1),'b','storage',8)]
    report=analyse(costs,forecast_days=7)
    assert len(report['forecasts'])==2
    assert report['forecast_total']==140

def test_summarizes_multiple_rows_same_day():
    costs=[Cost(date(2026,1,1),'a','ec2',5),Cost(date(2026,1,1),'a','ec2',7)]
    assert analyse(costs)['by_service'][0]['observed_cost']==12

def test_api_rejects_negative_cost():
    client=TestClient(app)
    assert client.get('/healthz').status_code==200
    assert client.post('/v1/analyse',json={'costs':[{'date':'2026-01-01','account':'a','service':'ec2','amount':-1}]}).status_code==422
