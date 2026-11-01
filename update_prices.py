import json, urllib.request, datetime
from zoneinfo import ZoneInfo
url='https://borsihind.s3.eu-central-1.amazonaws.com/15min/V4.json'
req=urllib.request.Request(url,headers={'User-Agent':'Elektrihind-personal-dashboard/1.0'})
with urllib.request.urlopen(req,timeout=25) as r: data=json.load(r)
zone=ZoneInfo('Europe/Tallinn')
rows=[]
for v in data:
    if len(v)<6: continue
    dt=datetime.datetime(*map(int,v[:5]),tzinfo=zone)
    rows.append({'ts':int(dt.timestamp()*1000),'spot':float(v[5])/10})
if not rows: raise ValueError('No prices in upstream response')
with open('prices.json','w',encoding='utf-8') as f:
    json.dump({'updated':datetime.datetime.now(datetime.timezone.utc).isoformat(),'rows':rows},f,separators=(',',':'))
