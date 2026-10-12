from pathlib import Path
import json,html
R=Path(__file__).parent;d=json.loads((R/'real-source-results.json').read_text());byid={x['id']:x for x in d['documents']}
css='body{background:#101728;color:#f0f4ff;font:20px system-ui;max-width:1100px;margin:auto;padding:35px}h1{font-size:42px}h2{color:#75dfc8}pre{background:#23334d;padding:18px;white-space:pre-wrap;font:16px monospace}details{margin:20px 0}summary{cursor:pointer}a{color:#75dfc8}td,th{padding:12px;border-bottom:1px solid #556}table{border-collapse:collapse}'
body='<h1>Skutečný kód: odkud přichází normalize?</h1><p>scikit-learn '+d['sklearn']+' • skutečný instalovaný zdroj • AST import → reexport → definice</p><p>Otázka: které tři zdrojové úseky vysvětlují, jak se normalize dostane do sklearn.feature_extraction.text?</p><h2>Tipněte úplnost pro top‑k = 3</h2><p>Vektorový index vybírá podobný text. Graf prochází explicitní importy; počáteční modul a symbol jsou známé.</p>'
for row in d['rows']:
 body+='<details><summary>'+row['method']+' — odhalit důkazy</summary><p>Úplné: '+str(row['complete'])+' • recall '+str(round(row['recall'],3))+' • '+str(row['context_bytes'])+' B</p>'
 for id in row['retrieved']:body+='<pre>'+html.escape(id+'\n'+byid[id]['text'])+'</pre>'
 body+='</details>'
body+='<p>Jeden diagnostický dotaz, překryv chunků a důkazových fragmentů. Nejde o obecný benchmark. Grafový parser řeší pouze explicitní importy ve třech modulech; ne dynamický Python ani interpretaci otázky. Čas měří pouze vybavení již postaveného indexu.</p><p><a href="presentation.html">Zpět na prezentaci</a> · <a href="real-source-results.json">Surové výsledky</a></p>'
(R/'source-demo.html').write_text('<!doctype html><html lang="cs"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Skutečný zdroj: normalize</title><style>'+css+'</style>'+body+'</html>')
