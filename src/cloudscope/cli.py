import argparse
import csv
import json
from datetime import date
from .engine import Cost,analyse

def main():
    parser=argparse.ArgumentParser(description='Analyse billing CSV: date,account,service,amount')
    parser.add_argument('csv_path')
    parser.add_argument('--output',default='finops.json')
    args=parser.parse_args()
    with open(args.csv_path,newline='',encoding='utf-8-sig') as fh:
        costs=[Cost(date.fromisoformat(row['date']),row['account'],row['service'],float(row['amount'])) for row in csv.DictReader(fh)]
    result=analyse(costs)
    with open(args.output,'w',encoding='utf-8') as fh:json.dump(result,fh,indent=2)
    print(f"Observed total: {result['observed_total']:.2f}; anomalies: {len(result['anomalies'])}")

if __name__=='__main__':main()
