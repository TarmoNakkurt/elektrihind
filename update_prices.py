import json
import urllib.request
import datetime
from zoneinfo import ZoneInfo

URL = 'https://borsihind.s3.eu-central-1.amazonaws.com/15min/V4.json'
request = urllib.request.Request(URL, headers={'User-Agent': 'Elektrihind-personal-dashboard/1.1'})
with urllib.request.urlopen(request, timeout=25) as response:
    data = json.load(response)

zone = ZoneInfo('Europe/Tallinn')
rows = []
for v in data:
    if len(v) < 6:
        continue
    dt = datetime.datetime(*map(int, v[:5]), tzinfo=zone)
    # API spot-price field is in EUR/kWh; convert to cents/kWh.
    spot_cents = float(v[5]) * 100
    if not -100 <= spot_cents <= 1000:
        raise ValueError(f'Unexpected spot price: {spot_cents} cents/kWh')
    rows.append({'ts': int(dt.timestamp() * 1000), 'spot': round(spot_cents, 5)})

if not rows:
    raise ValueError('No prices in upstream response')
with open('prices.json', 'w', encoding='utf-8') as f:
    json.dump({'updated': datetime.datetime.now(datetime.timezone.utc).isoformat(), 'rows': rows}, f, separators=(',', ':'))
