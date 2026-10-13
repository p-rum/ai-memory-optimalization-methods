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
