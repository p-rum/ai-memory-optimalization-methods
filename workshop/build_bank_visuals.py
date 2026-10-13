"""Build banking SVG walkthrough and offline UI without browser or external services."""
import json,html,textwrap
from render_diagram import render
from pathlib import Path
R=Path(__file__).parent;D=json.loads((R/'bank-results.json').read_text());docs={d['id']:d for d in D['documents']}
COL=dict(bg='#101728',panel='#152138',card='#21334f',green='#75dfc8',orange='#ffb58c',white='#edf3ff',muted='#a5b6d1',blue='#80bfff')
def rect(x,y,w,h,fill=None,stroke=None):return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="12" fill="{fill or COL["card"]}" stroke="{stroke or "#465977"}" stroke-width="2"/>'
def txt(x,y,s,size=22,color=None):return f'<text x="{x}" y="{y}" fill="{color or COL["white"]}" font-family="DejaVu Sans" font-size="{size}">{html.escape(str(s))}</text>'
def arrow(x,y,x2,y2,on=True):return f'<path d="M{x} {y} L{x2} {y2}" stroke="{COL["green"] if on else "#465977"}" stroke-width="{4 if on else 2}" fill="none" marker-end="url(#arr)"/>'
def node(x,y,w,label,sub='',on=False,color=None):
 c=color or (COL['green'] if on else COL['muted']);return rect(x,y,w,64,'#19473f' if on else COL['card'],c)+txt(x+12,y+26,label,19,c)+txt(x+12,y+50,sub,15,COL['muted'])
def label(id):
 if id.startswith('data:'):return id[5:]
 if id.startswith('cfg:'):return id[4:]
 return docs[id]['label']
def create(qid,stage=3,k=4):
 q=next(q for q in D['queries'] if q['id']==qid);gold=set(q['gold']);chosen=[x['id'] for x in D['rankings'][qid][:k]];hit=len(gold&set(chosen));g=next(r for r in D['rows'] if r['query']==qid and r['method']=='structure');rank=D['rankings'][qid]
 out='<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1440 720" role="img" aria-label="Vektorové pořadí textů a strukturované vazby bankovní platformy"><defs><marker id="arr" markerWidth="9" markerHeight="9" refX="8" refY="4" orient="auto"><path d="M0 0 L0 8 L8 4 Z" fill="#75dfc8"/></marker></defs>'
 out+=rect(0,0,700,708,COL['panel'])+rect(728,0,700,708,COL['panel'])+txt(24,40,'VEKTOR · co zní podobně?',27)+txt(752,40,'GRAF + STAV · co je propojené a platné?',24)
 out+=txt(24,72,'TF-IDF: pořadí textů podle slov v otázce',19,COL['muted'])+txt(752,72,'Volání kódu, datové zdroje a nasazená verze',19,COL['muted'])
 if stage<2:
  for i,id in enumerate([qid.replace('bank-report','doc-weekly-report').replace('bank-feature','doc-feature-proposal').replace('bank-health','doc-health-old')]+q['gold'][:3]):
   out+=rect(24,102+i*104,650,88)+txt(42,133,label(id)[:43],21)+txt(42,166,'Uložený text → číselná reprezentace',18,COL['blue'])
 else:
  for i,r in enumerate(rank[:4]):
   color=COL['green'] if r['id'] in gold else COL['orange'];y=100+i*112
   out+=rect(24,y,650,98,stroke=color)+txt(42,y+28,f'{r["rank"]}. {label(r["id"])[:38]}',20,color)+txt(42,y+57,'podobnost '+f'{r["score"]:.3f}',18,COL['muted'])
   snippet=docs[r['id']]['text'].replace('\n',' ')
   hint={'doc-weekly-report':'Popis reportu, ne úplná datová lineage.','doc-feature-proposal':'Návrh feature, ne seznam všech volajících míst.','doc-health-old':'Starší pravidlo: platnost skončila.','doc-health-draft':'Návrh pravidla: není nasazený.'}.get(r['id'],'Zdrojový text / kód; nutno ověřit jeho roli.')
   out+=txt(42,y+83,hint,18)
  if k>4:out+=txt(24,570,f'Zobrazeny první 4; do kontextu vybráno {k} záznamů.',18,COL['muted'])
  else:out+=txt(24,570,'Podobný dokument nemusí obsahovat potřebné důkazy.',18,COL['muted'])
 if qid=='bank-report':
  out+=node(940,110,300,'weekly_report','report.py',stage>=1)+node(760,250,275,'weekly_pnl','pnl.py',stage>=2)+node(1110,250,285,'financial_health','health.py',stage>=2)
  out+=node(752,110,170,'profil klienta','čte report',stage>=3)+arrow(940,143,927,143,stage>=3)+arrow(1020,174,900,245,stage>=2)+arrow(1160,174,1250,245,stage>=2)
  for i,(left,right) in enumerate([('pozice','cash-flow'),('uzavírací ceny','maržový snapshot'),('FX sazby','pozice · sdílený zdroj')]):
   y=350+i*78;out+=node(760,y,275,left,'datový zdroj',stage>=3)+node(1110,y,285,right,'datový zdroj',stage>=3)
  for right,spine in [(1035,1050),(1395,1410)]:
   color=COL['green'] if stage>=3 else '#465977'
   out+=f'<path d="M{right} 282 L{spine} 282" stroke="{color}" stroke-width="3" fill="none"/>'
   out+=f'<path d="M{spine} 282 L{spine} 538" stroke="{color}" stroke-width="3" fill="none"/>'
   for yy in [382,460,538]:out+=arrow(spine,yy,right,yy,stage>=3)
  out+=txt(752,616,'Zjednodušená lineage; čte přes load_* funkce.',17,COL['muted'])
  out+=txt(752,640,'Profil čte report přímo; pozice také vstupují do skóre.',16,COL['muted'])
 elif qid=='bank-feature':
  out+=node(890,120,365,'calculate_margin_buffer','měněná funkce · what-if margin',stage>=1,COL['blue'])
  out+=arrow(1070,184,1070,270,stage>=2)+txt(1090,236,'kdo ji volá?',18,COL['green'])
  out+=node(890,280,365,'calculate_financial_health','přímý dopad',stage>=2)
  out+=arrow(985,344,900,455,stage>=3)+arrow(1150,344,1270,455,stage>=3)
  out+=node(760,465,280,'weekly_report','nepřímý dopad',stage>=3)+node(1110,465,285,'trader_dashboard','nepřímý dopad',stage>=3)
  out+=txt(752,585,'Směr analýzy je obrácený: od změny k volajícím.',19,COL['muted'])+txt(752,616,'Statický graf neodhalí všechny dynamické vazby.',17,COL['muted'])
 else:
  out+=node(752,115,204,'v1 · historická','do 30. 9. 2026',False)+node(974,115,204,'v2 · nasazená','od 1. 10. 2026',stage>=2)+node(1196,115,204,'v3 · DRAFT','nenasazený návrh',False,COL['orange'])
  out+=txt(760,230,'1. Z registru vybereme deployed + datum platnosti.',18,COL['green'] if stage>=2 else COL['muted'])
  out+=arrow(1075,179,1075,270,stage>=2)+node(865,280,420,'financial_health(weights)','health.py + mechanisms.json',stage>=2)
  for i,(name,w) in enumerate([('likvidita','50 %'),('maržová rezerva','30 %'),('diverzifikace','20 %')]):
   out+=node(752+i*222,390,204,name,w,stage>=3)
  out+=arrow(1075,344,1075,380,stage>=3)
  out+=rect(810,494,536,73,'#19473f' if stage>=3 else COL['card'],COL['green'])+txt(832,525,'Modelový klient: skóre 54,67 / 100',24,COL['green'])+txt(832,551,'Výpočet skutečně spustí run_bank_demo.py',17,COL['muted'])
  out+=txt(752,612,'Shoda názvu dokumentu ≠ aktuální nasazený mechanismus.',17,COL['muted'])
 if stage==3:
  out+=rect(24,653,650,43,'#19473f' if hit==len(gold) else '#3c2b29',COL['green'] if hit==len(gold) else COL['orange'])+txt(42,681,f'Potřebné důkazy: {hit}/{len(gold)} · top-{k}',22,COL['green'] if hit==len(gold) else COL['orange'])
  out+=rect(752,653,652,43,'#19473f',COL['green'])+txt(770,681,f'Potřebné důkazy: {len(gold)}/{len(gold)} · úplné',22,COL['green'])
 out+='</svg>';return out
assets={}
for q in D['queries']:
 for stage in range(4):
  for k in ([4] if stage<2 else [4,8,12]):assets[f'{q["id"]}:{stage}:{k}']=create(q['id'],stage,k)
 for stage in [0,3]:
  name=q['id']+('-stored' if stage==0 else '-evidence');(R/(name+'.svg')).write_text(create(q['id'],stage))
  render(R/(name+'.svg'),R/(name+'.png'))

css='''#bankviz{font:17px system-ui;color:#edf3ff}#bankviz *{box-sizing:border-box}#bankviz .controls{display:flex;gap:8px;align-items:center;flex-wrap:wrap;margin:10px 0}#bankviz button,#bankviz select{font:inherit;background:#23344f;color:white;padding:9px 12px;border:1px solid #627494;border-radius:8px;margin:0;cursor:pointer}#bankviz button.active{background:#19473f;border-color:#75dfc8}#bankviz svg{width:100%;height:auto;max-height:none;display:block}#bankviz .caption{color:#75dfc8;font-size:18px;line-height:1.4}#bankviz .muted{color:#adbed8;font-size:14px;line-height:1.4}#bankviz .legend{display:flex;gap:18px;flex-wrap:wrap;font-size:15px}@media(max-width:750px){#bankviz .scene{overflow:auto}#bankviz svg{min-width:900px}}'''
component='<div id="bankviz"><div class="controls"><label>Otázka <select id="bank-case">'+''.join(f'<option value="{q["id"]}">{html.escape(q["title"])}</option>' for q in D['queries'])+'</select></label><label>top-k <select id="bank-k"><option>4</option><option>8</option><option>12</option></select></label></div><div class="controls">'+''.join(f'<button data-bankstage="{i}">{i+1} · {t}</button>' for i,t in enumerate(['Uložení','Otázka','Hledání','Důkazy']))+'<button id="bank-next">Další krok →</button></div><div id="bank-scene" class="scene"></div><p id="bank-caption" class="caption" aria-live="polite"></p><div class="legend"><span style="color:#75dfc8">● potřebný důkaz</span><span style="color:#ffb58c">● podobné, ale nestačí</span><span style="color:#80bfff">● místo změny</span></div><p class="muted">Modelová platforma, nikoli vaše bankovní pravidla. Skóre textů je skutečný TF-IDF výsledek; graf je extrahovaný z AST. U současného mechanismu se přidává přesný registr verzí. Český dotaz nad anglickými názvy kódu je omezení baseline. top-k není stejný rozpočet jako celý průchod grafem.</p></div>'
js='''(()=>{let stage=0;const $=id=>document.getElementById(id);const captions=['Stejný modelový kód a dokumenty: vektory uchovají podobnost, graf explicitní vazby.','Určete otázku a počáteční objekt. V ukázce je intent i objekt zadaný předem.','Vlevo řadíme texty. Vpravo sledujeme kódové/datové vazby nebo platnost mechanismu.','Kontrolujte potřebné důkazy, ne jen podobný název. Zvýšením top-k přidáte text, ne jistotu správné vazby.'];function render(){const q=$('bank-case').value,k=stage<2?'4':$('bank-k').value;$('bank-scene').innerHTML=BANK_SVG[q+':'+stage+':'+k];$('bank-caption').textContent=captions[stage];document.querySelectorAll('[data-bankstage]').forEach(b=>{b.classList.toggle('active',Number(b.dataset.bankstage)===stage);b.setAttribute('aria-pressed',String(Number(b.dataset.bankstage)===stage))})}document.querySelectorAll('[data-bankstage]').forEach(b=>b.addEventListener('click',()=>{stage=Number(b.dataset.bankstage);render()}));$('bank-next').addEventListener('click',()=>{stage=(stage+1)%4;render()});$('bank-case').addEventListener('change',()=>{stage=0;render()});$('bank-k').addEventListener('change',render);render();})();'''
fragment='<style>'+css+'</style>'+component+'<script>const BANK_SVG='+json.dumps(assets,ensure_ascii=False)+';'+js+'</script>'
(R/'bank-visual-fragment.html').write_text(fragment)
(R/'bank-visual.html').write_text('<!doctype html><html lang="cs"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Bankovní platforma: vektory a grafy</title><style>body{background:#101728;color:#edf3ff;margin:0;font:18px system-ui}main{max-width:1300px;margin:auto;padding:24px}a{color:#75dfc8}</style><main><h1>Co agent najde pro obchodníka?</h1>'+fragment+'<p><a href="presentation.html">Prezentace</a> · <a href="bank-results.json">Naměřené podklady</a> · <a href="facilitator.md">Návod moderátora</a></p></main></html>')
print('Built banking walkthrough and 6 SVG/PNG exports')
