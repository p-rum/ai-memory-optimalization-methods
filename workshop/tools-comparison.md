# Graphify a srovnatelné nástroje

Ověřeno podle primárních zdrojů 2026-10-12. Dokumentační srovnání; tyto produkty jsme v benchmarku nespouštěli.

Graphify zde znamená Graphify-Labs/graphify (oficiální balíček `graphifyy`). Srovnání se vztahuje k popsanému OSS workflow; Graphify Cloud je samostatná nabídka.

## Rychlé srovnání

| Nástroj | Zaměření | Reprezentace | Vybavení |
|---|---|---|---|
| [Graphify](https://github.com/Graphify-Labs/graphify) | Kód | Graf kódu a artefaktů; bez vektorového indexu v popsaném OSS workflow. | query, path, explain; CLI a MCP nad uloženým grafem. |
| [GitNexus](https://github.com/abhigyanpatwari/GitNexus) | Kód | AST graf symbolů a toků; BM25 a volitelné sémantické embeddingy. | Hybrid query, context, impact, trace; CLI a MCP. |
| [Graphiti](https://github.com/getzep/graphiti) | Paměť | Temporální graf entit a faktů, epizody jako zdroje; hybridní retrieval. | Sémantika + keyword + grafový průchod, časová platnost. |
| [Cognee](https://docs.cognee.ai/core-concepts/overview) | Paměť | Relační metadata / provenance + vektory + graf; pipeline pro paměť. | recall s výběrem strategie; improve a forget pro správu paměti. |
| [Mem0](https://github.com/mem0ai/mem0) | Paměť | Extrahované vzpomínky a entity; aktuální retrieval kombinuje více signálů. | search; sémantické, keyword a entity signály dle verze a nasazení. |
| [LightRAG](https://github.com/HKUDS/LightRAG) | Dokumenty | Entity / vztahy v grafu spolu s vektorovými reprezentacemi. | Dvouúrovňové vybavení detailů i širších konceptů. |
| [Microsoft GraphRAG](https://microsoft.github.io/graphrag/) | Dokumenty | Graf entit, hierarchie komunit a jejich souhrny. | Global, Local, DRIFT a Basic Search podle rozsahu otázky. |

## Zápis, změny a pilot

### Graphify

- Zápis: Lokální Tree-sitter pro kód; modelová extrakce pro dokumenty a média.
- Změny: Obnova přes update / git hook; sama o sobě nedokládá historickou platnost faktů.
- Vhodné použití: Struktura repozitáře a propojení kódu s dokumentací.
- Co ověřit: EXTRACTED a INFERRED hrany, čerstvost po změně branch, rozlišení stejných názvů.
- Pilotní úloha: Původ zdrojů weekly_report a dopady změny calculate_margin_buffer.
- Primární zdroj: [Graphify](https://github.com/Graphify-Labs/graphify)

### GitNexus

- Zápis: Tree-sitter a rozlišení vazeb mezi soubory; lokální analyze.
- Změny: Reindexace kódu; detect_changes mapuje diff na dopady. Časové vlastnictví není hlavní model.
- Vhodné použití: Call chain, dopady refactoringu a orientace v repozitáři.
- Co ověřit: Podpora jazyka, dynamické vazby; maxTokens je odhad 4 UTF-8 bajty/token, ne tokenizer LLM.
- Pilotní úloha: Stejný commit platformy: přímé i nepřímé dopady what-if margin.
- Primární zdroj: [GitNexus](https://github.com/abhigyanpatwari/GitNexus)

### Graphiti

- Zápis: Inkrementální ingest epizod; extrakce a entity resolution s modely.
- Změny: Explicitní časová platnost faktů a zachování historie při invalidaci.
- Vhodné použití: Kdo je vlastník teď a kdo byl vlastníkem k určitému datu?
- Co ověřit: Správnost extrakce a invalidace, ingest latency; OSS potřebuje vlastní grafový backend. Graphiti není totéž co managed Zep.
- Pilotní úloha: Nasazené a historické verze mechanismu; přidání návrhu nesmí změnit současný fakt.
- Primární zdroj: [Graphiti](https://github.com/getzep/graphiti)

### Cognee

- Zápis: remember; konfigurace extrakce a embeddingů určuje model i náklady.
- Změny: Správa položek, datasetů a session; temporalitu ověřit pro konkrétní pipeline.
- Vhodné použití: Sdílená paměť dokumentů, znalostí a agentových session.
- Co ověřit: Synchronizace indexů, provenance, přesnost entity resolution a chování při forget.
- Pilotní úloha: Dokumentace reportu, rozhodnutí o mechanismu a jejich zdroje; test forget.
- Primární zdroj: [Cognee](https://docs.cognee.ai/core-concepts/overview)

### Mem0

- Zápis: add nad konverzacemi a událostmi; user/session/agent scope.
- Změny: Ověřit konkrétní OSS / Platform verzi; současná Platform má nativní Graph Memory, staré enable_graph není aktuální návod.
- Vhodné použití: Preference a dlouhodobý kontext uživatele napříč interakcemi.
- Co ověřit: Izolace user_id, konflikt vzpomínek; vlastnosti a benchmarky Platform nepřenášet automaticky na OSS.
- Pilotní úloha: Kontext podpory obchodníka a preference; oddělení klientů a změny v čase.
- Primární zdroj: [Mem0](https://github.com/mem0ai/mem0); [Graph Memory Platform](https://docs.mem0.ai/platform/features/graph-memory)

### LightRAG

- Zápis: Indexace dokumentů, extrakce znalostí a embeddingy.
- Změny: Inkrementální aktualizace a selektivní mazání; testovat opravu navázaných vztahů.
- Vhodné použití: Otázky spojující fakta z více dokumentů.
- Co ověřit: Cena extrakce, kvalita citací; časová platnost není totéž co aktualizace indexu.
- Pilotní úloha: Propojení popisu reportu, datového katalogu a výpočtové metodiky.
- Primární zdroj: [LightRAG](https://github.com/HKUDS/LightRAG)

### Microsoft GraphRAG

- Zápis: TextUnits → extrakce vztahů → komunity → souhrny.
- Změny: Při změnách řešit dopad na extrakci a souhrny; nejde samo o sobě o temporal memory.
- Vhodné použití: Co jsou hlavní témata či problémy napříč korpusem?
- Co ověřit: Cena indexace/souhrnů a ztráta detailů; celokorpusovou otázku nehodnotit jen malým top-k testem.
- Pilotní úloha: Souhrn změn metodik a problémů reportingu napříč dokumenty.
- Primární zdroj: [Microsoft GraphRAG](https://microsoft.github.io/graphrag/)

## Jak vybrat pro našeho agenta

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
