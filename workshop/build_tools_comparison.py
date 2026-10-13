"""Build standalone offline comparison and sourced handout from tools.json."""
from pathlib import Path
import json,html
R=Path(__file__).parent;d=json.loads((R/'tools.json').read_text());items=d['tools']
md='# Graphify a srovnatelné nástroje\n\nOvěřeno podle primárních zdrojů '+d['verified_at']+'. '+d['measurement_status']+'\n\nGraphify zde znamená Graphify-Labs/graphify (oficiální balíček `graphifyy`). Srovnání se vztahuje k popsanému OSS workflow; Graphify Cloud je samostatná nabídka.\n\n## Rychlé srovnání\n\n| Nástroj | Zaměření | Reprezentace | Vybavení |\n|---|---|---|---|\n'
for t in items:md+=f"| [{t['name']}]({t['source']}) | {t['group']} | {t['model']} | {t['retrieval']} |\n"
md+='\n## Zápis, změny a pilot\n\n'
for t in items:
 md+=f"### {t['name']}\n\n- Zápis: {t['ingest']}\n- Změny: {t['updates']}\n- Vhodné použití: {t['fit']}\n- Co ověřit: {t['check']}\n- Pilotní úloha: {t['scenario']}\n- Primární zdroj: [{t['name']}]({t['source']})"+(f"; [Graph Memory Platform]({t['extra_source']})" if 'extra_source' in t else '')+'\n\n'
md+='''## Jak vybrat pro našeho agenta

Doporučení níže je interpretace popsaných architektur, nikoli změřené pořadí kvality:

- **Repozitář a závislosti:** nejbližší dvojice pro pilot je Graphify × GitNexus. Bankovní ukázka dopadů funkce tento problém ilustruje, ale náš AST skript není implementace ani benchmark těchto produktů.
- **Verze mechanismu a historie:** Graphiti je kandidát díky explicitní platnosti faktů. Přidejte SQL s verzovaným stavem jako jednodušší baseline.
- **Preference a session:** porovnat Mem0 a Cognee; rozhodnutí závisí také na potřebě modelovat vztahy a spravovat zdroje.
- **Podobné incidenty:** vector/keyword baseline plus memory nebo dokumentový systém. Nevyřazovat jednoduchý retrieval bez důkazu přínosu grafu.
- **Otázky přes dokumenty a celý korpus:** LightRAG a Microsoft GraphRAG; u GraphRAG oddělit lokální fakta od celokorpusových souhrnů.

Graf a vektory se nevylučují: GitNexus, Graphiti, Cognee a LightRAG kombinují strukturální a textové signály. Graphify ukazuje jinou variantu: grafové vybavení bez vektorového indexu v popsaném workflow.

## Férové porovnání produktů — návrh experimentu

Tento protokol **není provedené měření**. bank-results.json měří modelový kód; výsledky dalších příloh jsou oddělené baseline.

| Test | Stejný vstup a gold | Kandidáti | Co zaznamenat |
|---|---|---|---|
| Kód | Pevný commit modelové platformy, lineage reportu, změna maržové funkce | Graphify, GitNexus, AST baseline, lexical + neural retrieval | Pokrytí cest, přesnost hran, čerstvost, ingest, tokeny, RSS |
| Časová paměť | Nasazené, historické a draft mechanismy; gold k datu | Graphiti, Cognee, Mem0, verzované SQL | Aktuální i historické odpovědi, provenience, konflikty, ingest |
| Dokumenty | Stejný katalog reportů a metodiky, lokální i globální otázky | LightRAG, GraphRAG, vector baseline | Citace, souhrny, detailní odpovědi, cena indexace a změn |

Připnout release/commit, verzi modelu a embeddingů, konfiguraci, backend a corpus hash. Oddělit náklady zápisu, retrieval a generování; použít stejný model a skutečný token budget pro finální prompt. Zaznamenat i truncation, abstenci a chyby. Měřit cold/warm p50/p95 a přínos po aktualizaci. Vyžaduje-li nástroj odlišné předzpracování, ukázat jeho cenu a chyby samostatně.

Neporovnávat vendorové procentuální úspory s našimi bajty kontextu. Rozdíly modelů, datasetů, rozpočtů a OSS/hosted nabídky brání přímému pořadí. Dokumentace produktů se mění; pro implementaci ověřte připnutou verzi.

## Použití v meetingu

Slide 9 zabírá 19–21 min a nahrazuje živé top-k hlasování. Sweep zůstává v experiment.md a results.json pro následnou práci. V tools-comparison.html lze offline vybrat dva nástroje a porovnat stejné aspekty. Dvojice pro diskusi: Graphify/GitNexus (kód), Graphiti/Mem0 (paměť), LightRAG/GraphRAG (dokumenty).
'''
(R/'tools-comparison.md').write_text(md)
css='''*{box-sizing:border-box}body{background:#101728;color:#f0f4ff;font:19px system-ui;margin:0}main{max-width:1250px;margin:auto;padding:32px}h1{font-size:42px}h2,a{color:#75dfc8}select{font:inherit;background:#23334d;color:white;padding:12px;border-radius:8px;margin:8px}table{width:100%;border-collapse:collapse;table-layout:fixed}td,th{padding:16px;border-bottom:1px solid #3b4d68;text-align:left;vertical-align:top;overflow-wrap:anywhere}th:first-child{width:19%}small{color:#afc0d9}a{overflow-wrap:anywhere}@media(max-width:650px){main{padding:12px}td,th{padding:8px;font-size:15px}h1{font-size:30px}}'''
js='''const tools=DATA.tools;for(const id of ['left','right']){const s=document.getElementById(id);tools.forEach((t,i)=>{const o=document.createElement('option');o.value=i;o.textContent=t.name+' · '+t.group;s.append(o)});s.addEventListener('change',render)}document.getElementById('right').value=1;function render(){const a=tools[document.getElementById('left').value],b=tools[document.getElementById('right').value],table=document.getElementById('compare');table.replaceChildren();const rows=[['Aspekt',a.name,b.name],['Reprezentace',a.model,b.model],['Zápis',a.ingest,b.ingest],['Vybavení',a.retrieval,b.retrieval],['Změny / čas',a.updates,b.updates],['Vhodné použití',a.fit,b.fit],['Co ověřit',a.check,b.check],['Pilotní úloha',a.scenario,b.scenario]];rows.forEach((values,i)=>{const tr=document.createElement('tr');values.forEach(v=>{const cell=document.createElement(i===0?'th':'td');cell.textContent=v;tr.append(cell)});table.append(tr)});const tr=document.createElement('tr');const h=document.createElement('td');h.textContent='Primární zdroje';tr.append(h);[a,b].forEach(t=>{const td=document.createElement('td');const link=document.createElement('a');link.href=t.source;link.textContent=t.name;td.append(link);if(t.extra_source){const extra=document.createElement('a');extra.href=t.extra_source;extra.textContent=' · Platform Graph Memory';td.append(extra)}tr.append(td)});table.append(tr)}render();'''
(R/'tools-comparison.html').write_text('<!doctype html><html lang="cs"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Graphify a další nástroje</title><style>'+css+'</style><main><h1>Graphify a další nástroje</h1><p>Vyberte dvojici. Řádek „Vhodné použití“ říká, jakou otázku nástroj řeší. AST je struktura kódu, MCP rozhraní nástrojů agenta a OSS otevřená varianta softwaru. Vlastnosti dle primární dokumentace; ověřeno '+d['verified_at']+'.</p><p><small>'+html.escape(d['measurement_status'])+' Naše číselné výsledky měří baseline skripty.</small></p><label>První nástroj <select id="left"></select></label><label>Druhý nástroj <select id="right"></select></label><table id="compare" aria-live="polite"></table><p><a href="presentation.html">Prezentace</a> · <a href="tools-comparison.md">Podrobnosti a protokol pilotu</a></p></main><script>const DATA='+json.dumps(d,ensure_ascii=False)+';'+js+'</script></html>')
