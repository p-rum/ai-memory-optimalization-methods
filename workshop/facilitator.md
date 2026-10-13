# Průvodce moderátora — lze odprezentovat bez znalosti grafových databází

Tento dokument je pracovní scénář. Odstavce **Co říct nahlas** můžete přečíst nebo převyprávět. Ostatní části jsou pokyny pro vás. U ukázek postupujte podle klikacích kroků; odpovědi jsou uvedené, nemusíte je sami odvozovat.

## Příprava za 15 minut

1. Stáhněte celý repozitář: GitHub → **Code → Download ZIP**. Rozbalte jej. Otevřete složku `workshop`.
2. Otevřete `presentation.html` v běžném prohlížeči. Na GitHubu se HTML zobrazuje jako zdrojový kód, proto jej musíte stáhnout. K předvedení nepotřebujete Python, síť ani API klíč.
3. V další kartě otevřete tento návod (`facilitator.md` v editoru / GitHubu). Máte-li dvě obrazovky, prezentaci promítejte a návod ponechte na vlastní obrazovce. U PowerPointu použijte **Zobrazení prezentujícího**; stejný scénář je v poznámkách každého slidu. PDF poznámky neobsahuje.
4. Projděte slovníček níže. Zapamatujte si především rozdíl: podobný text versus přesná hodnota versus konkrétní vztah.
5. Nacvičte ukázku na slidu 6 a ověřte očekávané výsledky. V otevřené prezentaci lze použít šipky ←/→ nebo tlačítka. „Poznámky moderátora“ rozbalujte pouze na vlastní obrazovce; publikum by vidělo i řešení.
6. Připravte `presentation.pdf` jako zálohu. Nastavte časovač na 30 minut. Během meetingu nic neinstalujte a nepřepočítávejte benchmark.

## Hlavní myšlenka v jedné větě

Agentovi nechceme vždy poslat celý archiv: chceme najít správné důkazy a jejich platnost pomocí struktury odpovídající otázce.

## Slovníček v běžné řeči

| Pojem | Jak jej vysvětlit publiku |
|---|---|
| Paměť agenta | Data, která aplikace ukládá a později vybírá jako podklady pro model. |
| Kontext / prompt | Aktuální zadání a podklady, které model skutečně dostane. |
| Token | Jednotka textu pro model, často část slova; není to stejné jako bajt. |
| Retrieval / vybavení | Nalezení a výběr podkladů před odpovědí. |
| Index | Pomocná struktura, která usnadňuje hledání v uložených datech. |
| Vektor / embedding | Číselný popis textu, podle kterého lze porovnávat podobnost. |
| TF-IDF | Jednoduchý číselný popis založený na výskytu a vzácnosti slov; náš offline baseline. |
| Top-k | Počet nejlépe hodnocených vrácených výsledků, například dva. |
| Knowledge Graph | Objekty propojené pojmenovanými vztahy. |
| Entita / uzel | Konkrétní objekt: služba, databáze, tým nebo člověk. |
| Hrana / vztah | Vazba mezi objekty, například „závisí na“ nebo „vlastní“. |
| Traversal / průchod | Přecházení po vztazích, například služba → databáze → tým. |
| Provenience | Informace, odkud tvrzení pochází; zdrojový ticket, dokument nebo řádek kódu. |
| Časová platnost | Od kdy a do kdy je fakt pravdivý; důležitá při změně vlastníka. |
| Hybrid / router | Kombinace metod a pravidlo, které vybírá vhodnou metodu pro otázku. |
| Gold | Předem určené správné důkazy pro danou otázku. |
| Recall | Kolik potřebných důkazů se našlo. |
| Precision | Kolik z vrácených výsledků je opravdu užitečných. |
| Úplnost | Zda jsou nalezené všechny důkazy potřebné pro odpověď. |
| AST | Strom struktury programu, který čte parser; například pozná import a definici funkce. |
| Import / reexport | Převzetí jména z jiného modulu / jeho další zpřístupnění přes veřejný modul. |
| MCP | Rozhraní, přes které může agent volat nástroje, například vyhledávání v grafu. |
| OSS / hosted | Otevřená varianta softwaru / služba provozovaná poskytovatelem. |
| Latence / p95 | Doba čekání / hodnota, pod kterou leží 95 % měřených časů. |

## Bankovní příklady: co je důležité vysvětlit

Tři modelové otázky jsou původ dat týdenního reportu, dopady feature what-if margin a současný mechanismus finančního zdraví klienta. Skutečně spouštíme kód bank_demo; nepracujeme s produkčním kódem nebo pravidly vaší banky. Diagram zkracuje některé loader funkce pro čitelnost, úplné vazby jsou v bank-results.json.

| Pojem | Výklad pro tento meeting |
|---|---|
| PnL | Profit and loss; výsledek reportu je zde zjednodušená změna hodnoty jedné pozice. |
| Lineage | Odkud data pocházejí a jakými výpočty projdou do reportu. |
| What-if margin | Návrh feature pro zkoumání dopadů změny maržového požadavku. |
| Equity / initial margin | Hodnota modelového kapitálu / požadovaná počáteční marže; vstupy demonstrační rezervy. |
| Call graph | Graf, která funkce kterou další funkci volá. |
| Deployment registry | Přesný seznam verzí, jejich stavu a platnosti. |
| DRAFT | Návrh, který není nasazený; název dokumentu neznamená platnou verzi. |

V bank-visual.html jsou čtyři kroky. Nejdřív vyberte otázku, potom klikněte Uložení, Otázka, Hledání, Důkazy. top-k určuje počet textových výsledků. Zelená označuje potřebný důkaz, oranžová podobný dokument, který pro danou odpověď nestačí, modrá místo změny. Grafické skóre podobnosti není pravděpodobnost správnosti.

Výsledky jsou uložené výstupy skutečného běhu, ne živá odpověď LLM. K předvedení nic neinstalujte. Podrobná formule, vstupy a odkazy na zdroje jsou v bank-guide.md.

## Časový plán a hranice

| Slide | Čas | Co musí zaznít |
|---|---|---|
| 1 | 0–2 | Paměť aplikace vybírá důkazy pro model. |
| 2 | 2–4 | Kontext, úložiště a RAM jsou různé rozpočty. |
| 3 | 4–6 | Text, přesný stav a vztahy mají různé použití. |
| 4 | 6–8 | Nechte publikum tipnout tři otázky. |
| 5 | 8–10 | Pro report potřebujeme propojené zdroje. |
| 6 | 10–15 | Dopady feature a platná verze mechanismu. |
| 7 | 15–17 | Měříme důkazy, nikoli odpovědi LLM. |
| 8 | 17–19 | Graf s registrem měl úplné důkazy; start byl známý předem. |
| 9 | 19–21 | Nástroje jsou kandidáti podle úlohy, ne pořadí kvality. |
| 10 | 21–24 | Vysvětlit mechanismus v2 a původ modelového skóre. |
| 11 | 24–27 | Dvě minuty návrhu + dvě krátké odpovědi. |
| 12 | 27–30 | Dvě minuty dotazů, poslední minuta závěr. |

Doplňující podrobnosti ve slovníčku a FAQ jsou pro přípravu, ne k přečtení celé během meetingu.

---
## Slide 1: Paměť agenta pro podporu obchodníků

Čas: 0–2 min

Cíl slidu
Vysvětlit princip paměti na modelové platformě podpory burzovních obchodníků.

Co říct nahlas (lze přečíst)
„Dnes použijeme příklady blízké naší podpůrné platformě pro obchodníky na burze. Agent má vysvětlit, odkud report čerpá data, co se změní při nové funkci a jak se dnes počítá finanční zdraví klienta. U každé otázky si ukážeme, proč nestačí najít text se správnými slovy. Potřebujeme dohledat skutečné zdroje a vazby a rozlišit platnou verzi od starého dokumentu. Nepracujeme s naším produkčním kódem ani skutečným klientem. Je to malá spustitelná modelová platforma, na které lze princip ověřit.“

Co udělat
Zeptejte se: „Která z těchto tří otázek nám dnes zabere nejvíc času?“ Vyžádejte jednu odpověď, nejvýše 30 sekund.

Očekávaná odpověď / výsledek
Libovolná z trojice je v pořádku. Připomeňte, že cílem je vysvětlit postup vybavení důkazů, ne zavádět nový produkt.

Přechod na další slide
Pojďme stejný princip ověřit v dalším kroku.

Na co si dát pozor
Nikdy neříkejte, že modelová formule je skutečný bankovní scoring nebo že graf zachycuje vaši produkci.

## Slide 2: Co vlastně šetříme?

Čas: 2–4 min

Cíl slidu
Zabránit záměně menšího promptu, menší databáze a menší RAM.

Co říct nahlas (lze přečíst)
„Představte si knihovnu. V regálech může být tisíc knih, ale pro jednu odpověď otevřeme jen několik stránek. Regály odpovídají úložišti a vybrané stránky kontextu modelu. Vytvořit index nám pomůže stránky najít, ale index sám zabere další místo. Proto graf ani vektorová databáze automaticky nezmenšují celou paměť systému. Často šetří hlavně to, co předáváme modelu. Token je jednotka textu používaná modelem, přibližně část slova. My zde počítáme bajty textu: snadno je změříme, ale nejsou totéž co tokeny.“

Co udělat
Ukažte postup „uložené zdroje → vyhledání → několik důkazů → model“. Zeptejte se: „Když přidáme index, musí se zmenšit databáze?“

Očekávaná odpověď / výsledek
Ne. Index může úložiště i RAM zvětšit, přesto zmenšit vrácený kontext.

Přechod na další slide
„Teď se podíváme na několik způsobů, jak ty regály a kartotéku uspořádat.“

Na co si dát pozor
Úspora bajtů v našich výsledcích není změřená úspora RAM, tokenů ani finančních nákladů.

## Slide 3: Pět způsobů uložení

Čas: 4–6 min

Cíl slidu
Ukázat, že graf a vektory nejsou jediné možnosti.

Co říct nahlas (lze přečíst)
„Historie je nejjednodušší: uchováme, co se stalo. Čím je delší, tím obtížněji ji celou předáváme modelu. Souhrn pomůže, ale třeba vypustí větu, že určitý postup neplatí pro produkci. Přesné nastavení, jako měna reportu, je obvykle lepší uložit do pojmenovaného pole nebo tabulky. Incident je naproti tomu příběh s příznaky a řešením, takže se hodí text. A pokud potřebujeme vědět, které služby závisejí na které databázi, pomůže explicitní síť vztahů. Nemusíme vybrat jedinou strukturu pro všechno. Jedna událost může mít textový originál i strukturované údaje.“

Co udělat
Požádejte jednoho účastníka, aby zařadil informaci „report klienta je v EUR“. Potom informaci „timeout jsme vyřešili omezením souběžných požadavků“.

Očekávaná odpověď / výsledek
Jazyk: přesný stav v JSON/SQL. Postup řešení incidentu: textová zkušenost, případně ověřený návod.

Přechod na další slide
„Na stejných datech si ukážeme tři otázky, které potřebují různé druhy paměti.“

Na co si dát pozor
Souhrn, SQL a graf mohou být stejně užitečné. Nevytvářejte dojem, že graf je automaticky nejpokročilejší správné řešení.

## Slide 4: Tři otázky z podpory tradingu

Čas: 6–8 min

Cíl slidu
Vysvětlit princip paměti na modelové platformě podpory burzovních obchodníků.

Co říct nahlas (lze přečíst)
„První otázka začíná výsledkem, tedy reportem, a jde zpět ke zdrojům. Druhá začíná změnou funkce a jde opačně k místům, která funkci používají. Třetí potřebuje zjistit nejen vzorec v kódu, ale i to, která verze a váhy jsou skutečně nasazené. Dokument s názvem současný výpočet může být jen návrh. Tyto otázky jsou záměrně o vazbách a platnosti. Výsledky nám proto neřeknou, jak dobře bychom našli podobný incident nebo parafrázi v dokumentech.“

Co udělat
Dejte dvojicím 30 sekund. Potom vysvětlete: report má lineage; feature má call graph; mechanismus má deployment registry a kód. Call graph znamená graf, kdo kterou funkci volá.

Očekávaná odpověď / výsledek
A: nestačí uživatelský popis reportu. B: nestačí návrh nové feature. C: nestačí staré pravidlo ani nenasazený draft.

Přechod na další slide
Pojďme stejný princip ověřit v dalším kroku.

Na co si dát pozor
Tři otázky nejsou reprezentativní test všech možností paměti. Záměrně odpovídají potřebám podpůrné platformy.

## Slide 5: Vektory versus grafy: odkud jsou data?

Čas: 8–10 min

Cíl slidu
Vysvětlit princip paměti na modelové platformě podpory burzovních obchodníků.

Co říct nahlas (lze přečíst)
„Vlevo je textový vyhledávač. Najde například popis reportu, protože se velmi podobá otázce. To nám pomůže se zorientovat, ale ještě z toho nevíme, odkud přichází každé číslo. Vpravo je graf vytvořený ze skutečných volání v našem modelovém kódu a deklarací datových zdrojů. Z reportu přejdeme k PnL a finančnímu zdraví a dál ke zdrojům. Skóre podobnosti je číslo, ne pravděpodobnost pravdivosti. Oranžový dokument není nutně chybný: prostě neposkytuje potřebný důkaz. V ukázce známe počáteční funkci předem, což je důležitá výhoda grafového postupu.“

Co udělat
V HTML nechte otázku A (report) a top-k 4. Klikněte Uložení, Otázka, Hledání, Důkazy. Na každý krok 15–20 sekund. Ukažte vlevo doc-weekly-report, vpravo návaznost k datovým zdrojům. V PDF/PPTX je zobrazený konečný stav.

Očekávaná odpověď / výsledek
Vektor@4 má 0/9 definovaných důkazů lineage; strukturovaný průchod 9/9. Popis reportu se neshoduje se seznamem kódu a zdrojů, který potřebujeme.

Přechod na další slide
„Teď začneme naopak od místa, které chceme změnit, a potom se podíváme na platnou verzi výpočtu.“

Na co si dát pozor
Vektorový baseline je TF-IDF nad českými otázkami a převážně anglickým kódem. Nejde o test neuronových embeddingů. S devíti potřebnými důkazy nemůže top-4 vytvořit úplnou sadu; tento fakt vyslovte.

## Slide 6: Feature a aktuální mechanismus

Čas: 10–15 min

Cíl slidu
Vysvětlit princip paměti na modelové platformě podpory burzovních obchodníků.

Co říct nahlas (lze přečíst)
„Při feature what-if margin chceme změnit výpočet maržové rezervy. Nestačí najít návrh této feature. Potřebujeme vědět, že funkci volá výpočet finančního zdraví a ten dále používá report i dashboard obchodníka. U mechanismu skóre zase vybíráme nejprve nasazenou verzi z registru. Historická v1 a budoucí návrh v3 jsou v paměti, ale nepředstavují současný stav. Nasazená v2 kombinuje likviditu, maržovou rezervu a diverzifikaci. Výsledné číslo je pouze modelová ukázka: neznáme skutečné pravidlo naší banky.“

Co udělat
10:00–12:00 — Otevřete bank-visual.html. Vyberte B (what-if margin), top-k 4. Nechte tipnout dvě dotčená místa. Klikněte na Hledání a Důkazy. Ukažte šipky od calculate_margin_buffer přes calculate_financial_health do reportu a dashboardu.
12:00–14:00 — Vyberte C (současný mechanismus). Klikněte Otázka, Hledání, Důkazy. Vlevo ukažte historický dokument a draft. Vpravo porovnejte stav v1, nasazené v2 a nenasazené v3.
14:00–15:00 — Přečtěte skóre 54,67. Řekněte, že kód byl skutečně spuštěn, ne že odpověděl LLM. Vraťte se na prezentaci. Python není potřeba spouštět během meetingu.

Očekávaná odpověď / výsledek
B/vector@4: 1/3 důkazů dopadu; graf: 3/3. C/vector@4: 0/6 potřebných důkazů mechanismu; registr + graf: 6/6. generate_weekly_report má PnL 460 EUR a skóre 54,67, verzi health-v2.

Přechod na další slide
Pojďme stejný princip ověřit v dalším kroku.

Na co si dát pozor
Šipky u dopadů jsou směr analýzy od změny k volajícím, opačný než původní CALLS. Stará verze i draft mohou být užitečné pro jiné otázky; pro dnešní mechanismus ale nestačí.

## Slide 7: Co jsme opravdu měřili?

Čas: 15–17 min

Cíl slidu
Vysvětlit princip paměti na modelové platformě podpory burzovních obchodníků.

Co říct nahlas (lze přečíst)
„Máme tři konkrétní otázky. Pro každou jsme určili, které zdroje musí odpověď doložit. U reportu je to devět důkazů lineage, u feature tři dotčená místa a u mechanismu šest zdrojů pravidla. Gold je název tohoto očekávaného seznamu. Sledujeme, zda se podařilo najít vše, a kolik textu vracíme. Strukturovaný postup prochází skutečný AST graf modelového kódu. AST je struktura programu přečtená parserem. U současného mechanismu navíc přesně filtruje registr verzí. Výběr počátečního symbolu a typu otázky máme zadaný předem.“

Co udělat
Ukažte příklad 1/3 u feature. Zeptejte se: „Stačí to pro seznam všech dopadů?“ Pak vysvětlete, že čas hledání se opakoval 50krát a nezahrnuje ingest ani rozpoznání otázky.

Očekávaná odpověď / výsledek
Nestačí. Chybí dvě používaná místa. Nalezené dokumenty ani úplná sada samy nedokazují správnou odpověď LLM.

Přechod na další slide
Pojďme stejný princip ověřit v dalším kroku.

Na co si dát pozor
Budget není stejný: top-4 versus plný průchod. Český dotaz/anglický kód znevýhodňuje slovní baseline. Výsledky nelze přenést na neural RAG, Graphify nebo produkční banku.

## Slide 8: Výsledky bankovní ukázky

Čas: 17–19 min

Cíl slidu
Přečíst skutečné výsledky a jejich omezení.

Co říct nahlas (lze přečíst)
„Celý archiv obsahuje všechny podklady, takže má úplnost tři ze tří, ale posílá 5 885 bajtů textu. Vektorový top-4 vrací průměrně 1 089 bajtů a pro naše tři strukturované otázky nemá úplnou sadu. Graf s registrem má úplné sady pro tři otázky a vrací průměrně 2 650 bajtů. Tedy není nejmenší: vrací i zdroje, které potřebujeme. Oproti celému archivu omezí text asi o 55 procent. To podporuje názornou myšlenku vybavení podle vazeb, ale není to obecný důkaz vítězství grafů. Úlohy jsme zvolili podle potřeb platformy a rozpočty strategií nejsou stejné.“

Co udělat
Ukažte vlevo úplnost, vpravo velikost textu. Porovnejte nejprve full/structure, potom vector/structure. Nečtěte drobné časy.

Očekávaná odpověď / výsledek
full 3/3; vector 0/3; structure 3/3. Context 5 885, 1 089 a 2 650 B. Méně textu není výhra, pokud chybí důkaz.

Přechod na další slide
„Které nástroje takové vazby umějí zprostředkovat agentovi?“

Na co si dát pozor
Důvody omezení: tři otázky, modelová data, TF-IDF, české dotazy a anglický kód, známý router/symbol, různý budget. Chyby extrakce a skutečné LLM odpovědi je potřeba měřit zvlášť.

## Slide 9: Jak se v nástrojích orientovat?

Čas: 19–21 min

Cíl slidu
Představit výběr nástrojů bez potřeby znát jejich instalaci či architekturu.

Co říct nahlas (lze přečíst)
„Názvy nástrojů berte jako kandidáty pro různé úlohy. Graphify a GitNexus jsou nejbližší naší ukázce dopadů what-if margin: pomáhají agentovi orientovat se ve struktuře repozitáře. Graphify zde označuje Graphify-Labs a používá grafové vybavení; GitNexus nabízí i kombinaci textových signálů. Graphiti se zaměřuje na fakta s časovou platností. Cognee a Mem0 jsou kandidáti pro paměť znalostí a interakcí, ale záleží na konkrétní verzi a nasazení. LightRAG a GraphRAG míří na otázky nad dokumenty. Jejich vlastnosti jsme ověřili v dokumentaci, tyto produkty jsme však v našem měření nespouštěli.“

Co udělat
Volitelně otevřete tools-comparison.html, první nástroj Graphify, druhý GitNexus. Ukažte řádky „Vhodné použití“ a „Co ověřit“. Nečtěte všech sedm nástrojů ani neinstalujte software. Při nedostatku času zůstaňte na slidu.

Očekávaná odpověď / výsledek
Pro dopady funkce se nejprve nabízí Graphify/GitNexus; pro časovou historii Graphiti a SQL baseline. Volba není pořadí kvality.

Přechod na další slide
„Ať vybereme kterýkoli nástroj, musíme navrhnout, co se při změně informace stane.“

Na co si dát pozor
Graphify není Graphiti. OSS je otevřená varianta softwaru; hosted Platform je spravovaná služba, jejíž vlastnosti mohou být jiné. Aktuální primární zdroje a rozdíly jsou v tools-comparison.md.

## Slide 10: Jak ověřit současný mechanismus?

Čas: 21–24 min

Cíl slidu
Vysvětlit princip paměti na modelové platformě podpory burzovních obchodníků.

Co říct nahlas (lze přečíst)
„Na otázku současný mechanismus nestačí odpovědět vzorcem nalezeným v dokumentaci. Musíme doložit verzi, která je nasazená k danému datu, její váhy a kód, který je používá. V modelové v2 je likvidita dostupná hotovost dělená očekávaným odtokem a potom dvěma, omezená na nula až jedna. Maržová komponenta je rezerva nad initial margin v poměru k equity, dělená půlkou, také omezená. Diverzifikace je jedna minus podíl největší pozice. Vážené komponenty vynásobíme stem. Výpočet zde slouží pro ilustraci vysvětlení původu čísla; nehodnotíme bonitu ani nepředstavujeme pravidlo naší banky.“

Co udělat
Ukažte registry verze v1/v2/v3, pak tři komponenty a výsledek. Pokud je formule příliš detailní, stačí číst váhy a říct, že způsob normalizace je ve zdrojovém kódu. Zeptejte se: „Co by chybělo v odpovědi, kdybychom neuvedli verzi?“

Očekávaná odpověď / výsledek
Nevíme, zda jsou pravidlo a váhy aktuální. 13. 10. 2026 vybere modelový registry health-v2; v3-draft není nasazený ani po svém navrženém datu.

Přechod na další slide
Pojďme stejný princip ověřit v dalším kroku.

Na co si dát pozor
Žádné produkční prahy nebo schvalovací rozhodnutí nejsou součástí modelu. Při historické otázce se mění váhy podle datové platnosti, ne podle názvu dokumentu.

## Slide 11: Cvičení: agent pro trading platformu

Čas: 24–27 min

Cíl slidu
Vysvětlit princip paměti na modelové platformě podpory burzovních obchodníků.

Co říct nahlas (lze přečíst)
„Ve dvojicích navrhněte paměť pro asistenta podpory obchodníků. Má odpovídat na tři dnešní otázky a vejít podklady do tisíce tokenů. Nevybírejte hned značku databáze. Řekněte, které důkazy potřebujete, jak se k nim dostanete a jak poznáte platnou verzi. Přidejte test, který by chybný návrh odhalil. Například nový draft nesmí změnit odpověď na současný mechanismus. Máte dvě minuty, potom uslyšíme dvě třicetisekundové odpovědi.“

Co udělat
24:00–26:00 práce dvojic, 26:00–27:00 dvě odpovědi. Při tichu nabídněte rozdělení text / graf / registry a zeptejte se na draft.

Očekávaná odpověď / výsledek
Lineage přes datové vazby, dopady přes volající funkce, mechanismus přes platnou verzi a kód. Text pomáhá s popisy a zkušenostmi. Přijměte SQL joiny jako strukturovanou alternativu.

Přechod na další slide
Pojďme stejný princip ověřit v dalším kroku.

Na co si dát pozor
Graf musí zachytit čerstvý commit; pro dynamické volání mohou být nutné testy. Nejde jen o výběr úložiště.

## Slide 12: Co si odnést do dalšího návrhu?

Čas: 27–30 min

Cíl slidu
Uzavřít bez tvrzení, že jedna struktura řeší všechny paměťové problémy.

Co říct nahlas (lze přečíst)
„Dnes jsme viděli, že podobnost textu, přesná hodnota a vztah mezi objekty jsou různé potřeby. U podobného incidentu může stačit textové hledání. U verze mechanismu potřebujeme platný stav a u lineage reportu konkrétní návaznost. Kombinace může zmenšit kontext, ale přináší také práci s extrakcí, aktualizacemi a výběrem správné cesty. Proto bych jako další krok nevolil okamžitě migraci na nový nástroj. Vybral bych skutečný report, jednu feature a několik časových otázek našeho týmu, určil potřebné důkazy a na nich porovnal jednoduchou variantu s kandidáty. Při výběru se ptejme nejen, zda systém něco našel, ale zda našel to, co odpověď potřebuje.“

Co udělat
27:00–29:00: dvě otázky z publika, případně z připraveného FAQ. 29:00–30:00: přečtěte závěrečný odstavec a ukažte odkaz na podklady. Ve 30:00 skončete.

Očekávaná odpověď / výsledek
Účastníci by měli umět rozlišit tři úlohy, popsat přínos struktury a vědět, že naše výsledky mají omezený rozsah.

Přechod na další slide
„Podklady, zdrojový kód a měření jsou v repozitáři; detailní otázky můžeme rozebrat po meetingu.“

Na co si dát pozor
Na otázku, kterou neumíte zodpovědět, použijte: „Tohle jsme v ukázce neměřili; ověřme konkrétní verzi a přidejme test.“ Neimprovizujte produktové sliby.

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
