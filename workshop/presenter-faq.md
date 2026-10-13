---

# Záložní postup a FAQ pro moderátora

## Když se ukázka nedaří

| Situace | Postup |
|---|---|
| HTML ukazuje zdroj na GitHubu | Stáhnout ZIP, rozbalit a otevřít HTML lokálně. |
| Grafické kroky se neposouvají | Kliknout přímo na „Důkazy“; k prvním krokům se lze vrátit. |
| Odkaz neotevře další kartu | Otevřít bank-visual.html přímo ze složky workshop. |
| Prohlížeč nefunguje | PDF/PPTX už obsahuje finální diagramy; očekávané hodnoty jsou v poznámkách. |
| Nemám druhou obrazovku | Scénář vytisknout nebo ponechat v jiné kartě mimo sdílené okno. |
| Jsem ve skluzu | Vynechat nástrojovou tabulku, cvičení zkrátit na 60 sekund a jednu odpověď. |
| Nevím detailní odpověď | „Tohle ukázka neměřila; ověřme konkrétní implementaci a přidejme test.“ |

## Krátké odpovědi, které lze použít nahlas

**Je to naše skutečné bankovní pravidlo?** Ne. Modelujeme otázky vašeho týmu; k produkčnímu kódu a metodice nemáme přístup. Skóre 54,67 patří jen výukovému klientovi a modelové formuli.

**Proč jsou všechny otázky pro graf?** Jsou vybrané podle původu dat, dopadů kódu a současné verze mechanismu. Potřebují vazby a platnost. Není to reprezentativní test podobných incidentů nebo parafrází, kde může stačit textové hledání.

**Proč top-4 neumí celé reportové podklady?** Gold má devět důkazů. Top-4 proto nemůže vytvořit úplnou sadu ani při dokonalém pořadí. Tento limit je součástí vysvětlení, nikoli důkaz nadřazenosti grafu. Pro rozhodnutí týmu je nutný stejný token budget nebo jiné férově zdokumentované nastavení.

**Není textový baseline slabý?** Je záměrně jednoduchý TF-IDF. České otázky a anglický kód jej znevýhodňují. Neuronové embeddingy, metadata a iterativní retrieval jsme zde netestovali. Přiložené výsledky nejsou obecné pořadí RAG systémů.

**Jak graf pozná správný start?** V našem pokusu je funkce i typ otázky zadaný předem. Produkční agent je musí rozpoznat a tuto chybu i cenu je třeba měřit zvlášť.

**Odkud jsou hrany?** Z AST našeho spustitelného Python kódu: importy, přímá volání a deklarace datových zdrojů. AST je strom struktury programu. Dynamická volání a všechny runtime závislosti parser nezachytí.

**Proč je u mechanismu graf plus stav?** Graf popisuje implementaci, ale nasazenou verzi vybírá přesný registr podle stavu a data. Tento filtr není sám o sobě vlastnost grafové databáze. Stejnou část lze řešit SQL.

**Znamená zelená správnou odpověď LLM?** Ne. Znamená potřebný důkaz. LLM zde nevoláme. Odpověď může stále potřebovat správnou interpretaci, citace a kontrolu platnosti.

**Znamená menší kontext menší RAM a cenu?** Tady měříme bajty textu. Index může úložiště a RAM zvětšit. Pro cenu API potřebujeme tokenizér, cenu extrakce a odpovědi a náklady aktualizací.

**Proč Graphify, ne Graphiti?** Nejsou zaměnitelné. Graphify/GitNexus jsou kandidáti pro repozitář a dopady feature. Graphiti je kandidát pro časově platná fakta. Podrobnosti a primární zdroje jsou v tools-comparison.md.

**Který nástroj máme zavést?** Tohle meeting nerozhoduje. Připravte skutečný report, jednu feature a schválený registr mechanismů. Porovnejte jednoduchou baseline s kandidáty na stejném zadání, rozpočtu a modelu. Tyto produkty jsme v našem benchmarku nespouštěli.

**Jaké další kontroly patří k trading platformě?** Práva ke klientským datům, čerstvost snapshotů, kalendář a měna, schválená verze konfigurace, změny kontraktů a testy. Graf sám nepovoluje přístup k datům ani nenahrazuje ověření finančního výpočtu.
