# Paměť LLM agenta: 30minutový workshop

České podklady pro vývojáře se základní znalostí agentů. Cílem je názorně odlišit podobnost textu, přesný stav a vztahy mezi entitami a zvolit strukturu podle typu dotazu.

## Použití na meetingu

- **[presentation.html](presentation.html)** — 12 slidů, šipky ←/→, poznámky moderátora, interaktivní důkazy; funguje offline po stažení.
- **[demo.html](demo.html)** — samostatná ukázka tří dotazů a čtyř strategií, odhalování gold a skutečně vrácených dokumentů.
- **[source-demo.html](source-demo.html)** — reálný zdrojový kód scikit-learn: AST graf importů/reexportů versus vektorové hledání; [měření](real-source-experiment.md).
- **[facilitator.md](facilitator.md)** — minutový scénář 0–30, otázky, očekávané odpovědi a záložní postup.
- **[handout.md](handout.md)** — srovnání metod, schema, aktualizace, návrh pilotu a další čtení.
- **[experiment.md](experiment.md)** — výsledky a omezení měření.
- `presentation.pptx` a `presentation.pdf` — lokálně vygenerované exporty; lze obnovit pomocí `export_slides.py`.

HTML na GitHubu stáhněte (Raw → Save as), GitHub je nezobrazuje jako aplikaci. Stáhněte celý repozitář přes Code → Download ZIP, rozbalte a otevřete `workshop/presentation.html`. Lze také spustit `python -m http.server 8000` v adresáři workshop a otevřít http://localhost:8000/presentation.html. Není potřeba API klíč ani síťové volání.

## Reprodukce měření

```bash
cd workshop
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python benchmark.py
python build_materials.py
python real_source_benchmark.py
python build_source_demo.py
```

`benchmark.py` vytváří 48 dokumentů a 24 dotazů, provádí skutečný retrieval a 50 opakování na kombinaci metoda/dotaz. `results.json` obsahuje zdroje, gold, každé vrácené ID, latence, souhrn a top‑k sweep. `results.csv` umožňuje vlastní rozbor. Časy se při opakování mění.

HTML ukázka přepíná **předpočítané výsledky**, nespouští benchmark ani LLM v prohlížeči. Pro nový běh spusťte uvedené příkazy.

## Co lze z ukázky vyvodit

Modelové provozní příklady: incident connection pool, dvoukroková eskalace a změna vlastníka. Nejde o skutečný incident log ani produkční benchmark. Vektor = TF‑IDF + exact cosine nad sparse maticí; graf = ručně připravené hrany a dictionary lookup; current = materializovaný stav. Nejde o srovnání výkonu Neo4j a konkrétní vektorové DB ani neural embeddingů.

Hybrid má **předem známý intent i entitu**; jejich rozpoznání, extrakce hran, model a API nejsou v měření. Bajty nejsou tokeny a velikost kontextu není kompletní RAM. Referenční běh: full 24/24, vector 16/24, graph 16/24, hybrid 24/24 úplných sad důkazů. Podrobnosti a meze v `experiment.md`.

## Časový plán

| Minuty | Obsah |
|---|---|
| 0–6 | Hlasování, rozpočty, menu struktur |
| 6–10 | Předpověď + graf versus vektory |
| 10–15 | Interaktivní ukázka |
| 15–21 | Metodika, výsledky, top‑k |
| 21–24 | Hybrid a zápis paměti |
| 24–27 | Návrh ve dvojicích |
| 27–30 | Rozhodnutí a dotazy |

## Export PDF a PowerPoint

```bash
pip install -r requirements-export.txt
python export_slides.py
```

PowerPoint obsahuje poznámky moderátora; HTML má interaktivní demo a graf vztahů. Export do PDF používá DejaVu Sans na cestě `/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf` (Linux); jinde upravte cestu v exportním skriptu.

## Reálný zdrojový příklad

`real_source_benchmark.py` čte skutečný instalovaný kód scikit-learn (verze je připnutá v requirements.txt), z AST vytáhne import a reexport normalize a projde tento řetězec až k definici. Výsledky a snapshot zdrojů: `real-source-results.json`. Vector@3 našel 2/3 důkazů v 2 600 B; vector@8 3/3 v 6 904 B; graf 3/3 v 1 030 B. Jde o jeden diagnostický dotaz se známým symbolem a modulem, nikoli univerzální benchmark. Zdrojové fragmenty scikit-learn mají licenci v SCIKIT-LEARN-COPYING.txt.
