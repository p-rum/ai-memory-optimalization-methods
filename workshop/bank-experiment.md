# Vlastní měření bankovní modelové platformy

Referenční běh 13. 10. 2026. Spustitelná syntetická platforma, žádná produkční bankovní data. Číselná měření vznikla skutečným retrievalem; report a skóre se také skutečně spočítaly.

| Otázka | Metoda | Potřebné důkazy | Úplnost | Kontext B | Medián ms |
|---|---|---:|---|---:|---:|
| bank-report | full | 9/9 | ANO | 5885 | 0.000641 |
| bank-report | vector | 0/9 | NE | 822 | 0.207752 |
| bank-report | structure | 9/9 | ANO | 3826 | 0.017486 |
| bank-feature | full | 3/3 | ANO | 5885 | 0.000651 |
| bank-feature | vector | 1/3 | NE | 1425 | 0.227486 |
| bank-feature | structure | 3/3 | ANO | 1393 | 0.003905 |
| bank-health | full | 6/6 | ANO | 5885 | 0.000661 |
| bank-health | vector | 0/6 | NE | 1021 | 0.206125 |
| bank-health | structure | 6/6 | ANO | 2732 | 0.025848 |

## Protokol

- Tři konkrétní české otázky; nejde o nezávislý reprezentativní test set.
- Textový korpus obsahuje celé funkce modelového kódu, deklarace datasetů, konfigurace a dokumenty. Gold seznamy jsou ručně zadané v bank_benchmark.py, nezávisle na pořadí textového hledání.
- Vektor: TF-IDF, L2 normalizace, exact cosine, top-4. Nejlépe podobný dokument může být příběhový popis, nikoli požadovaný kód nebo zdroj.
- Graf: AST extrakce přímých volání a deklarací datových zdrojů. U reportu průchod dopředu; u feature obráceně od místa změny k volajícím. U současného mechanismu přesný filtr nasazeného registru + průchod implementací. Označení `structure` proto neznamená samotnou grafovou DB.
- Intent a počáteční symbol jsou zadané. Automatické rozpoznání otázky, síť, LLM odpověď, modelová extrakce a výkon produktů nejsou v měření.
- 50 warm opakování na kombinaci metoda/otázka. Medián a p95 v JSON/CSV; náklady ingestu se nepromítají do retrieval časů.
- Kontext = UTF-8 bajty plných vrácených textů oddělených newline. Nejde o tokeny ani peak RAM.

## Důležité meze srovnání

Tyto otázky vyžadují strukturu a platnost. Nehodnotíme podobné incidenty ani parafráze. Český dotaz nad anglickým kódem znevýhodňuje jednoduchý lexical baseline; neural embeddings by mohly dopadnout jinak.

Budget není stejný. Pro lineage je nutných devět důkazů, takže top-4 **nemůže** vytvořit úplnou sadu ani při ideálním pořadí. Strukturální traversal vrací více textu a zdrojů. Nulová úplnost vektoru proto není důkaz, že vektorové databáze nefungují pro bankovní platformu. Pro produkční závěr je nutné porovnat shodný token budget, více nastavení k, lepší embeddingy, filtry a iterativní retrieval.

full vrací vše: má úplné důkazy, ale neprokazuje, že LLM vybere správný mechanismus z historických a draft verzí. structure oproti archivu vrací v průměru 2 650 místo 5 885 B, tedy asi o 55 % méně textu. Vektor vrací ještě méně, ale jeho potřebné důkazy jsou neúplné.

AST graf neumí obecný Python runtime, dynamické importy ani všechny důsledky změny API. Diagram záměrně zkracuje některé cesty; úplné hrany obsahují source/evidence odkaz v JSON. Před rozhodnutím pro Graphify/GitNexus a další nástroje použijte skutečný bankovní commit, schválenou metodiku a vlastní gold sadu.

## Artefakty

- bank_benchmark.py: kód měření a gold definice.
- bank-results.json/CSV: jednotlivé výsledky, skóre pořadí textů, source odkazy a AST hrany.
- bank_demo/: spustitelný modelový kód a registry verzí.
- run_bank_demo.py: PnL 460 EUR, skóre 54,67 a kontroly platnosti / vstupů.
- bank-visual.html: interaktivní odhalování uložených výsledků.
- bank-guide.md: srozumitelný výklad tří příkladů.

Původní výsledky results.json a real-source-results.json zůstávají samostatnými obecnými příklady v příloze. Nepřičítejte je bankovnímu experimentu.
