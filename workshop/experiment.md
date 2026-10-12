# Vlastní experiment: retrieval paměti

Měřeno 12. 10. 2026 v připojeném prostředí. Scénáře napodobují reálnou práci s incidenty a vlastnictvím služeb; **data jsou syntetická**. Není zde volán LLM.

## Výsledky referenčního běhu

| Metoda | Úplné důkazy | Recall | Precision | Kontext B | Čas ms* |
|---|---:|---:|---:|---:|---:|
| full | 24/24 | 1.000 | 0.028 | 4447 | 0.000972 |
| vector | 16/24 | 0.708 | 0.375 | 196 | 0.199675 |
| graph | 16/24 | 0.667 | 0.667 | 67 | 0.000130 |
| hybrid | 24/24 | 1.000 | 0.833 | 175 | 0.000230 |

* Medián 24 per-query mediánů; každý z 50 warm opakování. p95 jednotlivých dotazů v CSV/JSON. Bez sítě, DB procesu, plánování, extrakce a generování odpovědi. Malé submikrosekundové lookupy jsou zatížené overheadem časovače; nesrovnávat s produkčními latencemi.

## Podle typu otázky

| Metoda | Podobnost | Dvě vazby | Aktuální stav |
|---|---:|---:|---:|
| full | 8/8 | 8/8 | 8/8 |
| vector | 8/8 | 0/8 | 8/8 |
| graph | 0/8 | 8/8 | 8/8 |
| hybrid | 8/8 | 8/8 | 8/8 |

## Citlivost na top-k

| k | Úplné důkazy vector | Kontext B |
|---|---:|---:|
| 1 | 16/24 | 98 |
| 2 | 16/24 | 196 |
| 4 | 16/24 | 407 |
| 8 | 16/24 | 803 |

## Protokol a rozsah

- 8 služeb, 6 dokumentů na službu, 3 dotazy na službu; opakované šablony, bez náhodné generace. Gold dokumenty jsou ručně určené a obsažené v JSON.
- TF‑IDF tokenizuje celé identifikátory `svc-0` (regex zachovává pomlčku); L2 normalizace, sparse dot product = cosine, stabilní pořadí při shodě. Vektorový index prohledává všech 48 textů, top‑k=2. Není ANN, žádný neural embedding ani externí vector DB.
- Grafový lookup má ručně vytvořený seznam ID dvou hran. Aktuální stav má explicitní ruční mapu. Epizodický retrieval graf nemá, proto na podobnosti vrací prázdno.
- Hybrid zná intent a entitu z query fixture a přepíná mezi těmito dvěma mechanismy. **Jde o oracle routing**, nikoli měření automatické klasifikace.
- Full vrací všech 48 textů, nemá budget. Je horní mez dostupnosti důkazů, nikoli důkaz správné odpovědi modelu.
- Úplnost = gold ⊆ returned; recall = |gold ∩ returned| / |gold|. Precision = |gold ∩ returned| / |returned|; pro prázdný výstup konvence 0. Souhrny jsou makroprůměry přes dotazy.
- Kontext je součet UTF‑8 bajtů plných vrácených textů včetně newline. Neobsahuje instrukce a query; **bajty nejsou tokeny**.
- Python 3.12.14; platform: `Linux-6.18.44-x86_64-with-glibc2.41`. Ingest TF‑IDF 2.534 ms; CSR data+indices+indptr 6244 B. Toto není velikost celého indexu: nezahrnuje vocabulary, IDF, texty, objekty ani RSS.

## Interpretace

Hybrid zde snižuje vrácený kontext z 4 447 na 175 B (přibližně 96 %) při úplných důkazech 24/24. To podporuje názornou myšlenku směrování podle otázky; **neprokazuje nadřazenost architektury v produkci**. Graf má proti vektorům navíc kurátorované struktury a známé entity. Extrakce i údržba mají cenu a chyby, které zde neměříme.

U dvoukrokové úlohy text druhé hrany neobsahuje jméno služby. Vektorové hledání proto typicky vrátí první hranu a jiný text se stejnou službou. Samotný graf zde nedokáže najít podobnou epizodu. Aktuální stav lze efektivně řešit SQL/JSON; není důvod vyžadovat grafovou DB.

## Co zlepšit pro rozhodnutí týmu

Stejný korpus, skutečné parafráze a časové otázky, metadata-filtered lexical i neural baseline, vektorový iterative retrieval, SQL join, automatická extrakce + routing. Pak měřit při shodném token budgetu s konkrétním LLM odpovědi i citace, latenci end-to-end, peak RSS, disk, cenu ingestu, náklady změn a chování při chybějícím důkazu. Vyhodnotit nezávislý test set; 8 variant jedné šablony nedává smysluplný interval spolehlivosti o obecném chování.
