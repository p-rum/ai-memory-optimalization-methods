# Scénář moderátora — 30 minut

Příprava: otevřít presentation.html a demo.html; není potřeba internet. Připravit Python pouze pro přepočet benchmarku. Účastníci nemusí nic instalovat.

## 1. Paměť agenta: co uložit, co vybavit

0–2 min: hlasování. Kde dnes držíte paměť: historie, summary, SQL, vektory, graf? Vyberte jednu zkušenost účastníka.

## 2. Tři různé rozpočty

2–4 min: ukažte cestu událost → zápis → index → retrieval → prompt. V našem měření počítáme UTF‑8 bajty, nikoli tokeny. KV cache je jiná vrstva optimalizace.

## 3. Menu struktur

4–6 min: preference uživatele patří do stavu, incident do epizody, závislost do vztahu. Stejný záznam lze indexovat několika způsoby. Procedurální paměť = ověřené postupy/runbooky; sémantická = fakta; epizodická = události.

## 4. Stejná data, jiné otázky

6–8 min: dejte 30 sekund ve dvojicích. Jde o realistické, ale syntetické scénáře, nikoli záznamy skutečného incidentu. Každý typ má osm variant.

## 5. Knowledge Graph × vektorový index

8–10 min: ukažte diagram svc-0 → db-0 → team-0. Druhá hrana neobsahuje svc-0; textová podobnost nemá důvod ji vrátit. GraphRAG je širší rodina postupů, ne synonymum pro každý graf.

## 6. Živá ukázka: najdi chybějící hranu

10–15 min: A 90 s, B 90 s, skutečný kód 2 min (source-demo.html); C volitelně po meetingu. U B ukažte očekávané ID i chybějící ID. C není kompletní temporal engine: aktuální stav je ručně materializovaný. Nezavádějte žádné API klíče, vše běží offline.

## 7. Jak jsme měřili

15–17 min: celé tělo textu je vraceno, žádné ořezávání do stejného budgetu. full má neomezený kontext. Dotazy sdílejí šablony: 24 není 24 nezávislých problémů. Latence neobsahuje LLM, síť, ingest ani klasifikaci dotazu.

## 8. Vlastní výsledky

17–19 min: ukažte graf a důkazy. Hybrid vrací asi o 96 % méně bajtů než full, ale data i routování jsou idealizované. Čísla nepřenášet na produkční vector DB / graph DB. Grafové cesty jsou dictionary lookup, vektory sparse exact cosine, ne ANN.

## 9. Změňme top‑k

19–21 min: před odhalením tipněte, zda k=8 opraví B. Všechny hodnoty jsou skutečně změřené nad stejnými daty. Zvyšování k není náhradou za návaznost vztahů a časové filtry.

## 10. Hybrid: oddělte text, stav a vazby

21–24 min: v našem hybridu známe intent a entity ze zadání. V produkci změřte chyby routeru, extrakce i entity resolution; graf nevymyslí chybějící hranu. Aktualizace vlastníka má uzavřít valid_to starého tvrzení, zachovat audit a invalidovat cache.

## 11. Cvičení: návrh paměti pro vašeho agenta

24–27 min: 2 min práce + 1 min dvě odpovědi. Očekávané řešení: preference přesný stav, incidenty epizody, vlastnictví verzované vztahy/stav. Test: historický vlastník k datu, nezáměnné identifikátory, konflikt zdrojů, tenant isolation.

## 12. Rozhodnutí a další experiment

27–30 min: 2 min otázky, 1 min závěr. Vyberte 20 skutečných dotazů vašeho týmu a porovnejte na stejném token budgetu: lexical, neural, SQL, graph a hybrid. Předem definujte gold, validitu, abstenci a náklady. Na 30 min skončete.

## Záchranný scénář

Při problému s prohlížečem použijte PDF/PPTX a results.csv. Demo je předpočítané, ne živý volaný LLM. Pokud dojde čas, přeskočte sweep a zkraťte návrhové cvičení na hlasování; konec nejpozději ve 30:00.

## Otázky a odpovědi

- Graf vždy lepší? Ne; u podobných incidentů zde nemá žádný mechanismus retrievalu. Lze ho doplnit fulltextem či vektory.
- Proč ne neuronové embeddingy? Základní ukázka funguje offline a izoluje strukturu retrievalu. TF‑IDF je lexical vektorová reprezentace, ne test parafrází.
- Proč je graf tak rychlý? Ruční dictionary lookup nad miniaturními daty, bez query planneru a sítě. Nejde o srovnání výkonu databázových produktů.
- Co s chybnou hranou? Vyžadovat zdroj, validitu, schema validation, rozlišení entit a testy aktualizací. Měřit i přesnost extrakce.
- Optimalizujeme RAM? Přímo měříme jen sparse matici indexu a délku kontextu, ne kompletní RAM. K tomu je potřeba izolované měření RSS, stejný korpus a oba reálné DB procesy.
- Jak ověřit odpovědi LLM? Stejný prompt/model/teplota a token budget, gold odpovědi, citace, abstence, několik běhů a slepé hodnocení.
