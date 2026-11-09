from __future__ import annotations
from collections import defaultdict
from dataclasses import dataclass
from datetime import date
from statistics import median
from typing import Sequence

@dataclass(frozen=True)
class Cost:
    date:date
    account:str
    service:str
    amount:float


def analyse(rows:Sequence[Cost],history_days:int=7,forecast_days:int=7) -> dict:
    if not 3<=history_days<=90 or not 1<=forecast_days<=90:raise ValueError('invalid window')
    if any(c.amount<0 for c in rows):raise ValueError('amounts must be nonnegative')
    daily=defaultdict(float)
    for item in rows:
        daily[(item.account,item.service,item.date)]+=item.amount
    by_service=defaultdict(list)
    for (account,service,day),amount in daily.items():
        by_service[(account,service)].append((day,amount))
    anomalies=[]; estimates=[]; totals=defaultdict(float)
    for (account,service),observations in sorted(by_service.items()):
        ordered=sorted(observations)
        all_values=[amount for _,amount in ordered]
        totals[(account,service)]=sum(all_values)
        for i,(day,amount) in enumerate(ordered):
            baseline=all_values[max(0,i-history_days):i]
            if len(baseline)<3:continue
            center=median(baseline)
            mad=median([abs(x-center) for x in baseline])
            robust_score=(amount-center)/max(1.4826*mad,1.0)
            if amount>=center*1.6 and amount-center>=25 and robust_score>=3.5:
                anomalies.append({'account':account,'service':service,'date':day.isoformat(),'cost':round(amount,2),'baseline':round(center,2),'robust_score':round(robust_score,2)})
        window=all_values[-history_days:]
        projection=median(window)*forecast_days
        estimates.append({'account':account,'service':service,'daily_reference':round(median(window),2),'forecast_days':forecast_days,'forecast_cost':round(projection,2)})
    spending=[{'account':a,'service':s,'observed_cost':round(cost,2)} for (a,s),cost in sorted(totals.items(),key=lambda pair:(-pair[1],pair[0]))]
    return {'observed_total':round(sum(totals.values()),2),'by_service':spending,'anomalies':sorted(anomalies,key=lambda x:(x['date'],x['account'],x['service'])),'forecasts':estimates,'forecast_total':round(sum(p['forecast_cost'] for p in estimates),2)}
