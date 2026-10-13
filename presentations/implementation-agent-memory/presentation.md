# Paměť implementačního agenta

28 minut výkladu + 2 minuty diskuse.

## 1. Paměť implementačního agenta

Struktura dat, výběr kontextu a skutečné náklady
SQL · vektory · znalostní grafy







### Poznámky pro přednášejícího (0.5 min)

Cílem je vybrat paměťovou architekturu pro agenta, který čte a mění kód. Pamětí zde myslíme uchovávaný a vyhledávaný kontext, nikoli RAM nebo trénování vah modelu. Přednáška má 28 minut a 2 minuty na diskusi. Příklady jsou ilustrativní, nejsou analýzou konkrétního bankovního systému.



---

## 2. Co budeme porovnávat




| Část | Čas |
|---|---|
| Paměť, SQL, vektory a grafy | 8 min |
| Kombinace a příklady změn v backendu | 8 min |
| Graphify a další nástroje | 5 min |
| Náklady, měření a doporučení | 7 min |
| Diskuse | 2 min |



### Poznámky pro přednášejícího (0.5 min)

Do první části patří i úvod. Zaměříme se na návrh, který může fungovat v různých IDE a agentech. Důležitý je rozdíl mezi uložením dat a rozhodnutím, které informace poslat modelu.



---

## 3. Čtyři vrstvy paměti




| Vrstva | Příklad | Životnost |
|---|---|---|
| Pracovní kontext | Zadání, otevřené soubory, chyby | Jeden krok / běh |
| Epizodická paměť | Co agent zkusil a jak dopadly testy | Úkoly a relace |
| Fakta o projektu | Symboly, závislosti, schéma DB | Platnost podle commitu |
| Pravidla a rozhodnutí | Konvence, ADR, omezení | Do nahrazení rozhodnutím |



### Poznámky pro přednášejícího (1 min)

Paměť nemusí být jeden produkt. Stav rozpracovaného úkolu potřebuje přesnou obnovu. Fakt o metodě potřebuje vazbu na konkrétní verzi kódu. Rozhodnutí má vlastní datum platnosti. Zkrácení historie je užitečné, ale shrnutí může ztratit důležitou podmínku. Ukládejme proto i odkazy na původní důkaz. Model sám vidí jen vybraný kontext, nikoli celou databázi.

- https://docs.langchain.com/oss/python/concepts/memory

---

## 4. Agent bez strukturované paměti




- 1  Hledá soubory a symboly
- 2  Opakovaně čte široký kontext
- 3  Odvozuje stejné vztahy
- 4  Při opravě znovu hledá důkazy

Cena roste s opakovaným vstupem,
počtem kroků a opravami.

Férový baseline už může používat grep, LSP, repo mapu, shrnutí i prompt cache.

### Poznámky pro přednášejícího (1 min)

Nezaměňujme baseline s karikaturou, která pokaždé pošle celý repozitář. Moderní agent běžně hledá soubory a pracuje s cache. Externí paměť má hodnotu, když sníží opakované objevování nebo počet chybných pokusů. V porovnání musíme nechat stejný model, nástroje, rozpočet a stejné úlohy. Pozdější model nákladů je záměrně čtecí, s velkým kumulativním vstupem.



---

## 5. Relační databáze: přesná fakta




- Symbol + cesta + commit
- Výsledky testů a stav úkolu
- Metadata, oprávnění a platnost
- JOIN a filtrování bez LLM

„Které migrace změnily
tabulku payment?“

PostgreSQL nebo SQLite stačí i pro počáteční seznam uzlů a hran.

### Poznámky pro přednášejícího (1.5 min)

Obyčejná databáze je často nejlevnější základ. Tabulky mohou uchovávat symboly, jejich zdrojový rozsah, build variantu i důkazy. SQL umí přesné dotazy a rekurzivní průchody. Samotné uložení do SQL ale nezaručí pravdivost: záleží na extraktoru a aktuálnosti. Fulltext pomůže s názvy a chybovými zprávami. Nevýhodou je potřeba schématu a horší hledání parafrází bez dalších indexů.



---

## 6. Vektorový index: podobnost významu




- Embedding textu nebo kódu
- Dotaz vrátí podobné úryvky
- Filtry omezí repo, verzi a typ dat
- Reranking vybere přesnější kontext

„Kde řešíme opakované
odeslání stejného požadavku?“

Podobnost najde kandidáta. Neprokazuje volání ani úplnost dopadů.

### Poznámky pro přednášejícího (1.5 min)

Dotaz může najít idempotenci, i když v něm není slovo idempotency. Dělení kódu podle funkcí a tříd obvykle zachová více smyslu než slepé bloky znaků. Uložme také signaturu, cestu a commit. Přesné identifikátory kombinujme s fulltextem. Přibližný index může minout relevantní výsledek, zejména po filtrování. Aktualizace vyžaduje přepočítat změněné embeddingy a odstranit zrušené položky.

- https://github.com/pgvector/pgvector
- https://qdrant.tech/documentation/search/hybrid-queries/

---

## 7. Znalostní graf: typované vztahy




- Uzel: metoda, endpoint, tabulka, ADR
- Hrana: volá, mapuje, čte, mění
- Průchod ukáže řetězec závislostí
- Každá hrana nese původ a platnost

„Co ovlivní změna
payment.external_id?“

Syntaktický vztah, staticky vyřešené volání a pozorovaný běh jsou různé důkazy.

### Poznámky pro přednášejícího (1 min)

Knowledge graf je datový model, nikoli synonymum grafové databáze nebo LLM. Hrany lze získat parserem, kompilátorem, introspekcí nebo modelovým odhadem. Tree-sitter poskytuje syntaxi, ale sám neřeší celý classpath a runtime chování Springu. Statický call graph může nadhodnocovat cíle. Trace ukazuje skutečně pozorovanou cestu, ne všechny možné cesty. U každé hrany potřebujeme druh, zdroj a status vyřešení.



---

## 8. Volba struktury podle dotazu




| Potřeba | První volba | Doplněk |
|---|---|---|
| Přesný symbol, verze, stav | SQL / index symbolů | Fulltext |
| Podobný problém nebo ADR | Vektory + fulltext | SQL filtry |
| Dopady napříč komponentami | Typovaný graf | Zdrojový kód |
| Obnovení rozpracované práce | Checkpoint / SQL | Stručné shrnutí |
| Přehled témat dokumentace | Hierarchická shrnutí | GraphRAG |



### Poznámky pro přednášejícího (1 min)

Struktury se nevylučují. Jedna PostgreSQL instance může kombinovat tabulky, fulltext a pgvector. Samostatná grafová databáze se vyplatí až podle složitosti průchodů, velikosti dat a provozních potřeb. Hierarchické shrnutí zrychluje orientaci, ale finální rozhodnutí musí být dohledatelné ke zdroji.

- https://github.com/pgvector/pgvector
- https://microsoft.github.io/graphrag/query/overview/

---

## 9. Kombinovaná paměť pro backend




| Fáze | Co proběhne |
|---|---|
| Získání faktů | Build model, parser, symboly, ORM, SQL migrace |
| Uložení | SQL jako evidence, vektory pro text, typované hrany |
| Výběr kandidátů | Přesný dotaz nebo fulltext + sémantické hledání |
| Rozšíření kontextu | Omezený průchod grafem, deduplikace, reranking |
| Práce agenta | Zdrojové úryvky v rozpočtu, úprava, build a testy |



### Poznámky pro přednášejícího (1.5 min)

Toto je návrh architektury, nikoli funkce jednoho konkrétního produktu. Router vybere retrieval podle otázky. Nemá smysl vždy spustit všechny databáze. Na dotaz na konkrétní metodu stačí index symbolů. U změny napříč moduly rozšiřme okolí grafem. Při nulovém nebo nejistém výsledku musí agent umět přejít k původním souborům. Pro sdílený index používejme stabilní identitu symbolu a vazbu na commit.



---

## 10. Příklad 1: idempotence REST endpointu




- Zadání: zabránit duplicitní platbě
- Vektory najdou ADR a podobné řešení
- Graf dohledá service a repository
- SQL vybere aktuální migrace

Výstup pro agenta:
endpoint, transakce, unikátní klíč,
relevantní testy a zdroj ADR.

Modelový Kotlin / Spring Boot projekt. Po úpravě následuje integrační test.

### Poznámky pro přednášejícího (1.5 min)

Představme si POST /payments. Sémantické hledání najde rozhodnutí o idempotency key. Symbolový graf vede od controlleru k service a JPA repository. Databázová evidence najde unikátní index a jeho migraci. Agent musí ověřit souběh dvou požadavků, rollback i chování při opakování po timeoutu. Testovací kód se vyhledává cíleně až jako důkaz pokrytí, ne jako produkční implementace.



---

## 11. Příklad 2: změna databázového sloupce




| Vazba | Důkaz | Omezení |
|---|---|---|
| Flyway migrace → sloupec | SQL parser + pořadí migrací | Odlišné nasazené prostředí |
| JPA atribut → sloupec | @Column + naming strategy | Implicitní názvy, konverze |
| Repository → atribut | Vyřešená query / metoda | Dynamické a native SQL |
| Service → repository | Typová analýza volání | Proxy, profily, reflexe |



### Poznámky pro přednášejícího (1.5 min)

Zadání je změnit external_id na nullable nebo upravit jeho typ. Agent potřebuje rozlišit schéma odvozené z migrací a skutečné nasazené schéma. Není správné tvrdit, že neexistuje další použití jen proto, že ho index nenašel. Dynamické SQL musí zůstat označeno jako nevyřešené. Praktický výstup obsahuje seznam známých závislostí, neznámá místa a testovací plán. Šipky v tabulce představují vazby, nikoli skutečný pořadový tok.



---

## 12. Příklad 3: paměť rozhodnutí




- V květnu: retry je vypnuté
- V červnu: retry jen pro timeout
- V říjnu: agent upravuje klienta

Vyhledat aktuální pravidlo
spolu s důvodem a historií.

commit, valid_from, valid_to, source a supersedes omezují použití zastaralých faktů.

### Poznámky pro přednášejícího (1 min)

Časová paměť se hodí pro ADR, incidenty a dohodnuté výjimky. Pouhé podobnostní hledání může vrátit staré rozhodnutí, protože je textově přesnější. Musíme filtrovat platnost nebo explicitně spojit nahrazující rozhodnutí. Graphiti je příkladem nástroje pro temporální vztahy. Pro několik desítek ADR může stačit obyčejná SQL tabulka.

- https://github.com/getzep/graphiti

---

## 13. Kvalita extrakce rozhoduje o kvalitě paměti




| Riziko | Opatření |
|---|---|
| Testy se tváří jako produkce | Source set a typ artefaktu jako povinný filtr |
| Enum je centrem kvůli četnosti | Ranking podle úkolu a typu vztahu |
| Konfigurace splývá s voláním | Oddělené vrstvy a explicitní typy hran |
| LLM odhad vypadá jako fakt | Původ, důkaz a status resolved / inferred |
| Index zaostává za kódem | Diff update, mazání, kontrola commitu |



### Poznámky pro přednášejícího (1.5 min)

Často používaný enum může být významný pro změnu číselníku, ale jeho degree není automaticky architektonická důležitost. Konfigurace je důležitá například pro výběr Spring profilu, jen nesmí být zaměněna za volání. Testy také nechceme zahodit: potřebujeme je v samostatném pohledu. Inkrementální aktualizace musí invalidovat i odvozené hrany sousedních symbolů a výstupy založené na změněném buildu.



---

## 14. Malý kontext s dohledatelnými důkazy




- Nejdříve filtr verze a oprávnění
- Potom relevance a závislosti
- Limity na počet hran i tokenů
- Shrnutí vždy s odkazem na zdroj

Příklad rozpočtu 12 000 tokenů:
2 000 zadání a pravidla
7 000 kód a důkazy
3 000 stav práce

Ilustrativní rozpočet. Chybějící důkaz spouští další cílené čtení.

### Poznámky pro přednášejícího (1 min)

Optimální počet tokenů není konstantní. Retrieval musí zachovat důležité signatury, kontrakty a chybová místa. Deduplikujme překrývající se úryvky. Není důvod v každém kroku vracet stejný log. Oddělme stabilní prefix pro případnou cache od dynamického výběru. Obsah dokumentů a paměti je vstupní evidence, nikoli oprávnění přepsat instrukce agenta.



---

## 15. Graphify a Aider: orientace v kódu




| Nástroj | Mechanismus | Vhodné použití |
|---|---|---|
| Graphify | AST graf, query / path / explain | Průzkum vztahů v repo + dokumenty |
| Aider repo map | Signatury a grafový ranking v token limitu | Kompaktní orientace při editaci |

U obou ověřit Kotlin, přesnost vazeb, rozlišení source setů a aktualizaci na změnách.

### Poznámky pro přednášejícího (1.5 min)

Graphify zde znamená Graphify-Labs/graphify. Aktuální README deklaruje lokální deterministický AST průchod pro kód, sémantickou fázi pro dokumenty a značky EXTRACTED a INFERRED. Tyto značky nejsou důkaz runtime volání. Aider vybírá relevantní části mapy repozitáře do tokenového rozpočtu. Nejde o plnohodnotný historický graf rozhodnutí. Toto je porovnání mechanismů podle dokumentace, nikoli vlastní benchmark.

- https://github.com/Graphify-Labs/graphify
- https://aider.chat/docs/repomap.html

---

## 16. GraphRAG, Graphiti a Mem0




| Nástroj | Primární role | Hlavní kompromis |
|---|---|---|
| Microsoft GraphRAG | Entity a souhrny dokumentových komunit | Indexace a globální dotazy mohou být nákladné |
| Graphiti / Zep | Časové vztahy a inkrementální paměť | Extrakce, řešení entit a provoz grafu |
| Mem0 | Výběr a aktualizace dlouhodobých vzpomínek | Paměť konverzace neřeší sama strukturu kódu |



### Poznámky pro přednášejícího (1.5 min)

GraphRAG má local, global a další režimy hledání, proto nelze paušálně označit každý jeho dotaz za drahý. Graphiti uchovává časovou platnost a původ faktů a kombinuje více způsobů hledání. Zep je související produktová infrastruktura, Graphiti open-source engine. Mem0 se zaměřuje na extrakci a správu relevantních vzpomínek. Žádný z těchto mechanismů automaticky nenahradí Kotlin compiler analysis.

- https://microsoft.github.io/graphrag/query/overview/
- https://github.com/getzep/graphiti
- https://github.com/mem0ai/mem0
- https://arxiv.org/abs/2504.19413

---

## 17. Úložiště a framework nejsou totéž




| Řešení | Co dodává | Co musíme doplnit |
|---|---|---|
| PostgreSQL
+ pgvector | Fakta, transakce, fulltext a vektory | Extrakci, routing, aktualizaci |
| Qdrant | Vektorové / hybridní vyhledávání | Autoritativní fakta a analýzu kódu |
| Grafová DB | Uložení vztahů a průchody | Schéma hran a kvalitní extraktor |
| LangGraph | Stav a řízení workflow / paměti | Doménový index a retrieval |

Doporučení pro první pilot: existující PostgreSQL, index symbolů a cílené doplňky.

### Poznámky pro přednášejícího (1 min)

Toto doporučení je architektonický úsudek pro backendový tým, ne univerzální vítězství jedné databáze. pgvector podporuje přesné i přibližné hledání. Qdrant nabízí hybridní dotazy a vícefázový retrieval. Pro složité grafové průchody lze přidat grafovou databázi až po měření. Pro malý lokální projekt může být jednodušší SQLite a souborový index.

- https://github.com/pgvector/pgvector
- https://qdrant.tech/documentation/search/hybrid-queries/
- https://docs.langchain.com/oss/python/concepts/memory

---

## 18. Co říkají publikované úspory




- Mem0: přes 90 % tokenové úspory
proti full-context v LOCOMO
- Graphify Cloud: tvrzení o 80 %
snížení spotřeby tokenů

Ani jedno číslo není zárukou
úspory na implementačních
úlohách v našem repozitáři.

Výsledky autorů / dodavatele. Odlišné úlohy, baseline a rozsah započtených nákladů.

### Poznámky pro přednášejícího (1 min)

Mem0 paper reportuje úsporu tokenů přes 90 procent a snížení p95 latence o 91 procent proti full-context přístupu v experimentu s konverzační pamětí LOCOMO. Na snímku ponecháváme pouze tokeny, abychom nesměšovali metriky. Graphify README uvádí 80 procent pro Cloud jako dodavatelské tvrzení. Nepřenášejme ho na lokální OSS ani na Kotlin změny. Srovnatelné vlastní měření všech nástrojů zde nemáme.

- https://arxiv.org/abs/2504.19413
- https://github.com/Graphify-Labs/graphify

---

## 19. Model nákladů jednoho úkolu


C = vstup + výstup + paměť + provoz + opravy

- 20 kroků × 75 000 vstupních tokenů
- Celkem 1,50 mil. vstup / 30 tis. výstup
- Modelová sazba 3 / 15 USD za mil. tokenů

Baseline bez cache
4,50 + 0,45 = 4,95 USD

Ilustrace, nikoli ceník nebo naměřený benchmark. Stejný model a úspěšnost.

### Poznámky pro přednášejícího (1.5 min)

Kumulativní vstup se sčítá přes všechna volání, nejde o maximální velikost okna. Sazby 3 a 15 USD jsou zvolené modelové parametry, ne aktuální cena konkrétního modelu. Další tabulka drží výstup 30 tisíc tokenů a počet kroků fixní, aby izolovala změnu vstupu. Náklady na build a testy předpokládáme stejné. Pokud se změní, musíme připočítat rozdíl. Náklad na lidskou práci se objeví v návratnosti.



---

## 20. Model: méně tokenů není celá úspora




| Varianta | Vstup mil. | Paměť USD | Celkem USD | Úspora |
|---|---|---|---|---|
| Bez paměti | 1,50 | 0,00 | 4,95 | — |
| SQL + symboly | 0,75 | 0,10 | 2,80 | 43 % |
| Vektory + filtry | 0,45 | 0,20 | 2,00 | 60 % |
| Typovaný graf | 0,30 | 0,35 | 1,70 | 66 % |
| Hybrid | 0,24 | 0,45 | 1,62 | 67 % |

Modelové předpoklady. Paměť zahrnuje retrieval a aktualizace. Fixní náklady zvlášť.

### Poznámky pro přednášejícího (1.5 min)

Výpočet je vstup v milionech krát 3 plus 0,03 krát 15 plus paměť. Například hybrid: 0,24×3 + 0,45 + 0,45 = 1,62 USD. Úspora je 1 minus náklad dělený 4,95. Pořadí není benchmark produktů ani záruka, že graf vždy porazí vektory. Pro jednoduchou opravu může být indexace dražší než grep. Částky nezahrnují jednorázové nasazení ani fixní hosting, které doplní další snímek.



---

## 21. Cache a objem práce mění návratnost




| Scénář | Výsledek modelu |
|---|---|
| Bez cache, baseline / hybrid | 4,95 / 1,62 USD za úkol |
| 80 % vstupu z cache u obou variant | 1,71 / 1,10 USD za úkol |
| Vstupní investice 300 USD + fixní 60 USD | Návratnost bez cache: 109 úkolů v 1. měsíci |
| Stejná investice při 80% cache | Návratnost: 592 úkolů v 1. měsíci |

Cache sazba 0,30 USD / mil. tokenů je modelová. Investice musí zahrnout i práci lidí.

### Poznámky pro přednášejícího (1.5 min)

Při 80 procent cache je efektivní sazba 0,2×3 + 0,8×0,3 = 0,84 USD za milion vstupních tokenů. Baseline 1,5×0,84+0,45=1,71. Hybrid 0,24×0,84+0,45+0,45=1,1016. Úspora 0,6084. Bez cache je úspora 3,33. Body zvratu jsou ceil(360/3,33)=109 a ceil(360/0,6084)=592. Jde o první měsíc. Obecně N>(počáteční investice + fixní náklad období)/(baseline−varianta). Pokud jmenovatel není kladný, návratnost neexistuje. Reálná implementace může stát násobně více než modelových 300 USD.



---

## 22. Ověření na implementačních úlohách




- 30–50 reprezentativních úkolů
- Stejný commit, model a pravidla
- Studený i aktualizovaný index
- Více opakování a zaslepené review

Hlavní metrika:
celková cena za přijatou změnu

Navíc: úspěšnost, čas, opravy, retrieval recall a podíl zastaralých důkazů.

### Poznámky pro přednášejícího (1.5 min)

Úlohy rozdělme na lokální opravy, změny přes moduly, DB změny a rozhodování podle dokumentace. Měřme A bez paměti, B SQL a symboly, C s vektory a D s grafem. Cost per accepted change počítejme jako celkové náklady všech pokusů dělené počtem přijatých změn, včetně neúspěšných běhů a ceny indexace. Hlásíme medián, p95 i variabilitu a změnu úspěšnosti. Kritérium pilotu může být úspora alespoň 20 procent bez významného zhoršení kvality, ale je to navržená brána, nikoli výsledek.



---

## 23. Doporučený postup pro tým




- 1  Symboly, metadata a měření baseline
- 2  Fulltext + vektory pro ADR a dokumenty
- 3  Typované hrany pro dopady změn
- 4  Časová paměť pro dlouhé workflow

Přidat další vrstvu až tehdy,
když řeší konkrétní měřenou ztrátu.

Výklad 28 minut. Diskuse 2 minuty: kde dnes agent opakovaně objevuje stejné informace?

### Poznámky pro přednášejícího (1 min)

Pro Kotlin a Spring má vysokou hodnotu kvalitní build model, source sety, symbol resolution a transparentní nevyřešené hrany. Graphify lze pilotovat pro navigaci, GraphRAG pro rozsáhlé dokumenty a Graphiti nebo Mem0 pro časovou či epizodickou paměť. Nemusíme nasadit všechny. Ptejte se publika, zda největší ztráta vzniká při hledání kódu, při dopadech změn nebo při zapomínání rozhodnutí. Diskuse má rezervované dvě minuty navíc.



---

## 24. Příloha: návrh minimálního záznamu




| Pole | Příklad |
|---|---|
| identity | repo + commit + symbol_id |
| classification | production / test / config / generated |
| evidence | path + řádky + content_hash + extractor |
| relation | calls / maps_to / alters / supersedes |
| validity | valid_from + valid_to + resolution_status |

Návrh schématu. Nejde o existující API konkrétního nástroje.

### Poznámky pro přednášejícího (0 min)

Společná identita propojí SQL, embedding a graf. U patchů kontrolujme commit i hash zdroje. Inkrementální aktualizace musí odstranit zaniklé symboly a odvozené vztahy. Pro multirepo doplňme vazbu mezi verzemi závislostí. Runtime důkaz přidejme s prostředím a časem pozorování.



---

## 25. Příloha: zdroje a metodika




- Graphify-Labs/graphify · README
- Aider · Repository map
- Microsoft GraphRAG · Query overview
- getzep/graphiti · README

pgvector · README
Qdrant · Hybrid queries
LangChain · Memory overview
Mem0 · arXiv:2504.19413

Zdroje ověřeny 13. 10. 2026. Přímé odkazy jsou v poznámkách příslušných snímků.

### Poznámky pro přednášejícího (0 min)

Veškeré porovnání nástrojů vychází z jejich primární dokumentace, nikoli ze spuštění na vlastním repozitáři. Nákladový model, SQL/grafové schéma a backendové scénáře jsou autorské ilustrace. Čísla úspor Mem0 a Graphify jsou tvrzení autorů či dodavatele a mají rozdílný rozsah. Odkazy: https://github.com/Graphify-Labs/graphify ; https://aider.chat/docs/repomap.html ; https://microsoft.github.io/graphrag/query/overview/ ; https://github.com/getzep/graphiti ; https://github.com/pgvector/pgvector ; https://qdrant.tech/documentation/search/hybrid-queries/ ; https://docs.langchain.com/oss/python/concepts/memory ; https://arxiv.org/abs/2504.19413

