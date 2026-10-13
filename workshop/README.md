# Paměť agenta pro podporu obchodníků na burze — 30 minut

Názorný český meeting o tom, jak agent dohledá správné podklady pro platformu podpory burzovních obchodníků. Méně zkušený moderátor má k dispozici slovníček, text k přednesu, přesné kroky a očekávané výsledky.

## Začněte zde — bez instalace

1. GitHub → **Code → Download ZIP**, rozbalit celý repozitář.
2. Přečíst [scénář moderátora](facilitator.md), zejména přípravu a slide 6.
3. Otevřít `workshop/presentation.html` v prohlížeči. Návod ponechat na vlastní obrazovce.
4. Nacvičit čtyři kroky v `bank-visual.html`: Uložení → Otázka → Hledání → Důkazy.

Není potřeba Python, API klíč ani síť. HTML na GitHubu ukazuje zdrojový text; spusťte stažený soubor. PowerPoint obsahuje stejný scénář v poznámkách pro zobrazení prezentujícího. PDF je statická záloha s finálními diagramy.

## Tři příklady pro váš tým

| Otázka | Co ukazujeme |
|---|---|
| Odkud se berou data pro týdenní report? | Lineage od reportu přes výpočty k pozicím, cenám, FX, cash-flow, maržím a profilu. |
| Které části kódu ovlivní nová feature? | Dopad what-if margin od měněné funkce přes skóre k reportu a dashboardu. |
| Jaký je současný mechanismus finančního zdraví klienta? | Nasazenou v2 versus historickou v1 a draft v3; váhy, kód a původ vstupů. |

Platforma i klient jsou **modeloví**, nejde o vaše produkční bankovní pravidlo. Kód je spustitelný, AST hrany a výsledky jsou skutečně získané. [Průvodce příklady](bank-guide.md) vysvětluje vzorce a přesné soubory.

## Podklady

- [Prezentace HTML](presentation.html), [PowerPoint](presentation.pptx), [PDF](presentation.pdf): 12 slidů, 30 minut.
- [Grafické bankovní srovnání](bank-visual.html): stejná otázka, textové pořadí vlevo, vazby/verze vpravo; postupné odhalování.
- [Scénář moderátora](facilitator.md): text k přednesu, slovníček, kliknutí, řešení a FAQ.
- [Bankovní příklady podrobně](bank-guide.md), [vlastní měření](bank-experiment.md), [raw JSON](bank-results.json), [CSV](bank-results.csv).
- [Graphify a šest dalších nástrojů](tools-comparison.md), [interaktivní porovnání dvojice](tools-comparison.html).
- [Technický tahák](handout.md): další struktury, schémata a návrh produkčního pilotu.

Barvy: zelená = potřebný důkaz; oranžová = podobný záznam, který pro otázku nestačí; modrá = místo změny. Hodnota podobnosti není pravděpodobnost pravdivosti.

## Časový plán

| Minuty | Obsah |
|---|---|
| 0–6 | Paměť aplikace, rozpočty a typy struktur |
| 6–10 | Tři bankovní otázky a grafické porovnání lineage |
| 10–15 | Dopady feature a platný mechanismus |
| 15–19 | Metodika a vlastní výsledky |
| 19–21 | Graphify a další kandidáti |
| 21–24 | Vysvětlení mechanismu a jeho zdrojů |
| 24–27 | Návrhové cvičení |
| 27–30 | Dotazy a závěr |

## Co měření říká a neříká

Tři otázky nad modelovým kódem: celý archiv 3/3 úplných sad, TF-IDF top-4 0/3, graf + registr 3/3. Průměrný kontext 5 885 / 1 089 / 2 650 B. Nejde o obecné pořadí metod: otázky vyžadují strukturu, budget není stejný a české dotazy/anglický kód znevýhodňují lexical baseline. Gold reportu má devět důkazů, takže top-4 nemůže být úplný ani při dokonalém pořadí.

Počáteční symbol a typ otázky jsou známé. Neměříme kvalitu odpovědí LLM, neuronové embeddingy, produkční RAM ani výkon Graphify, Graphiti či jiných produktů. Současný mechanismus kombinuje AST graf s přesným registrem stavu a času. Měření je názorné; produkční závěr potřebuje skutečný bankovní commit, schválenou metodiku, stejné rozpočty a nezávislé úlohy.

## Reprodukce a úpravy

```bash
cd workshop
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python run_bank_demo.py
python bank_benchmark.py
python build_bank_visuals.py
python build_materials.py
```

`run_bank_demo.py` ověří PnL 460 EUR, skóre 54,67, shodu report/dashboard a platnost verzí. `bank_benchmark.py` vytvoří JSON/CSV. Grafický builder běží offline přes Pillow a vlastní renderer jednoduchých SVG, bez Chromia.

Text slidů a poznámek upravujte ve `workshop-content.json`; úvod a FAQ v `presenter-intro.md` / `presenter-faq.md`. Potom spusťte `build_materials.py`. `facilitator.md` a `slides.json` jsou generované. Po novém benchmarku zkontrolujte číselné hodnoty v poznámkách a bank-experiment.md.

Exporty:

```bash
pip install -r requirements-export.txt
python export_slides.py
```

Export používá Linux font `/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf`; jinde upravte jeho cestu. Grafika je také ve verzích `bank-*-stored.svg/png` a `bank-*-evidence.svg/png`. Pro srovnání nástrojů upravte tools.json a spusťte build_tools_comparison.py.

## Doplňkové původní příklady

[Obecné incidentové demo](demo.html), [jeho měření](experiment.md), [importní řetězec skutečného scikit-learn](source-demo.html) a [zdrojové měření](real-source-experiment.md) jsou samostatné přílohy. Jejich výsledky jsou v results.json a real-source-results.json a nepatří do bankovního benchmarku. Fragmenty scikit-learn mají licenci SCIKIT-LEARN-COPYING.txt.

Podrobnější bankovní scénář: 13. 10. 2026. Dokumentační srovnání nástrojů: ověřeno 12. 10. 2026, nejde o vlastní produktový benchmark.
