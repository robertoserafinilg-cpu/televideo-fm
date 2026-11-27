import json, urllib.request, urllib.parse, xml.etree.ElementTree as ET, datetime, pathlib, concurrent.futures
queries={110:"pulizie multiservizi facility management",120:"igiene ambientale raccolta rifiuti",201:'"Cosp Tecno Service"',202:"Rekeep",203:"Dussmann Italia",204:"Coopservice",205:"Idealservice",206:"Markas",207:'"Euro&Promos"',208:'"Miorelli Service"',209:'"Consorzio Nazionale Servizi"',300:"gara appalto pulizie rifiuti aggiudicazione",310:"cambio appalto pulizie multiservizi",410:"accordo sindacale multiservizi igiene ambientale",420:"sciopero pulizie rifiuti",430:"CCNL multiservizi igiene ambientale",500:"sentenza appalto pulizie rifiuti",600:"bilancio facility management rifiuti",610:"rating legalità multiservizi rifiuti",620:"sanzione appalto pulizie rifiuti",700:"Umbria pulizie appalti rifiuti"}
path=pathlib.Path("news.json")
old=json.loads(path.read_text()) if path.exists() else {}
def get(pair):
 n,q=pair
 try:
  url="https://news.google.com/rss/search?"+urllib.parse.urlencode({"q":q+" when:30d","hl":"it","gl":"IT","ceid":"IT:it"})
  with urllib.request.urlopen(urllib.request.Request(url,headers={"User-Agent":"Mozilla/5.0"}),timeout=25) as r: root=ET.fromstring(r.read())
  items=[{"title":i.findtext("title",""),"url":i.findtext("link",""),"source":i.findtext("source",""),"date":i.findtext("pubDate","")} for i in root.findall("./channel/item")[:15]]
  return str(n),items,True
 except Exception as e:
  print(n,e)
  return str(n),old.get("pages",{}).get(str(n),[]),False
with concurrent.futures.ThreadPoolExecutor(max_workers=5) as pool: results=list(pool.map(get,queries.items()))
if not any(ok for n,items,ok in results): raise SystemExit("Nessuna fonte raggiungibile")
pages={n:items for n,items,ok in results}
from email.utils import parsedate_to_datetime
def date(i):
 try:return parsedate_to_datetime(i["date"]).timestamp()
 except:return 0
pages["100"]=sorted({i["url"]:i for items in pages.values() for i in items}.values(),key=date,reverse=True)[:30]
path.write_text(json.dumps({"updated":datetime.datetime.now(datetime.timezone.utc).isoformat(),"pages":pages},ensure_ascii=False),encoding="utf-8")
