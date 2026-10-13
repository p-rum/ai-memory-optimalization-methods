# Modelová podpůrná platforma pro obchodníky na burze

Tyto příklady odpovídají tématům vašeho týmu, ale **nepoužívají vaše bankovní data, zdrojový kód ani skutečné scoringové pravidlo**. Kód v bank_demo je spustitelný výukový model. Diagramy ukazují jeho reálné závislosti; výpočty a retrieval byly skutečně spuštěny.

## 1. Odkud se berou data pro týdenní report?

Začněte funkcí `generate_weekly_report` v [report.py](bank_demo/report.py). Report má dva výstupy: demonstrační PnL a finanční zdraví klienta.

| Část | Zdroje | Cesta v kódu |
|---|---|---|
| PnL | portfolio_positions, market_closing_prices, reference_fx_rates | report → calculate_weekly_pnl → load_* |
| Finanční zdraví | client_cashflows, margin_snapshots, portfolio_positions | report → calculate_financial_health → load_* |
| Identita a měna reportu | client_profiles | report → load_client_profile |
| Váhy mechanismu | nasazená health-v2 | report → deployed_mechanism → mechanisms.json |

Lineage je původ a cesta dat. U pozice 100 kusů, změny ceny 150 → 155 USD a FX 0,92 USD/EUR vyjde `(155−150) × 100 × 0,92 = 460 EUR`. Je to zjednodušená změna hodnoty jedné nezměněné pozice: nezahrnuje obchody v průběhu týdne, poplatky ani úplné FX PnL. Pro produkční report by bylo potřeba doložit také čas snapshotů, kalendář, korekce a reconciliation.

**Proč graf pomáhá:** uživatelský popis reportu nevyjmenuje všechny zdroje. Průchod volání a deklarací datových zdrojů je propojí. Diagram záměrně vynechává loader funkce pro čitelnost; jejich úplné vazby a souborové odkazy jsou v bank-results.json.

## 2. Které části kódu ovlivní přidání feature?

Modelová feature **what-if margin** má umožnit obchodníkovi zkoumat dopad změny maržového požadavku. Bod změny je `calculate_margin_buffer`.

```text
calculate_margin_buffer —používá ji→ calculate_financial_health
                                        ├─→ generate_weekly_report
                                        └─→ get_trader_dashboard
```

V AST grafu jsou původní hrany CALLS vedené od volajícího k volanému. Analýza dopadů je prochází **opačně**, od místa změny k jeho uživatelům. To je důvod, proč je důležité znát směr vztahu.

V modelu jsou přímo/nepřímo dotčené tři funkce. Kód není automaticky bezpečný k nasazení jen proto, že graf našel volající. U skutečné feature ověřte také testy, API kontrakty, dynamická volání, config, cache, oprávnění a rollout. Výukový příklad analyzuje dopad; samotnou feature neimplementuje.

## 3. Jaký je současný mechanismus výpočtu finančního zdraví klienta?

Odpověď má doložit **nasazenou verzi + datum platnosti + konfiguraci + implementaci + zdroje vstupů**. Nestačí dokument s podobným názvem.

| Verze v modelu | Stav | Platnost | Váhy likvidita / marže / diverzifikace |
|---|---|---|---|
| health-v1 | dříve nasazená | do 1. 10. 2026, konec nezahrnut | 60 % / 40 % / 0 % |
| health-v2 | nasazená | od 1. 10. 2026 | 50 % / 30 % / 20 % |
| health-v3-draft | návrh | žádná produkční platnost | 20 % / 60 % / 20 % |

Pro modelové datum 13. 10. 2026 se v [registry.py](bank_demo/registry.py) filtruje `status == deployed` a interval `valid_from ≤ datum < valid_to`. Návrh v3 se nevybere ani po jeho plánovaném datu, dokud nemá stav deployed.

### Výpočet pro modelového klienta DEMO-001

Vzorec a vstupy jsou pouze pedagogická volba, nikoli vaše bankovní metodika.

| Komponenta | Normalizace v kódu | Vstupy | Výsledek |
|---|---|---|---:|
| L: likvidita | clamp(cash / next_week_outflows / 2, 0, 1) | 20 000 / 30 000 | 0,3333 |
| M: maržová rezerva | clamp(((equity−initial_margin)/equity)/0,5, 0, 1) | 100 000 a 50 000 | 1,0 |
| D: diverzifikace | 1−largest_position_share | 0,60 | 0,4 |

`clamp` omezí číslo do daného intervalu. Pro v2:

```text
score = 100 × (0,5 × L + 0,3 × M + 0,2 × D)
      = 100 × (0,5 × 0,3333… + 0,3 × 1 + 0,2 × 0,4)
      = 54,67
```

Kód kontroluje kladné odtoky a equity a interval podílu největší pozice. Zjednodušený model nemá produkční prahy pro rozhodování, řízení úvěru ani bonitu.

## Předvedení bez instalace

Otevřete [bank-visual.html](bank-visual.html), vyberte otázku a postupně klikněte **Uložení → Otázka → Hledání → Důkazy**. Zelená znamená potřebný důkaz, oranžová dokument nebo pravidlo, které pro tuto otázku nestačí. U dopadů je modré místo změny. `top-k` mění počet textových výsledků, nikoli graf.

Pro kontrolu původních výsledků použijte bank-results.json / CSV. Grafický panel je výukový zjednodušený pohled; raw výstup obsahuje celý nalezený kontext a vazby.

## Reprodukce

```bash
cd workshop
pip install -r requirements.txt
python run_bank_demo.py
python bank_benchmark.py
python build_bank_visuals.py
python build_materials.py
```

První příkaz s Pythonem spustí report a ověří PnL, skóre, shodu s dashboardem, hranici platnosti verzí, vyřazení draftu a chování při neplatné equity. Benchmark přepočítá vyhledání a časy. Grafické podklady používají offline Pillow renderer (`pip install Pillow`), bez prohlížeče.

Po novém měření aktualizujte číselné poznámky ve workshop-content.json a bank-experiment.md; časy a případné pořadí textů se mohou změnit. Parametry a výstupy tohoto referenčního běhu jsou uložené.

## Jak nahradit model vašimi skutečnými podklady

Pro A vyberte jeden konkrétní report a commit jeho generátoru, datový katalog, pipeline a snapshoty. Pro B vyberte skutečný bod změny, call graph a testy kontraktů. Pro C použijte schválený deployment/config registry, aktuální implementaci a několik anonymizovaných vstupů s ověřeným výsledkem. Zachovejte gold důkazy, oprávnění a časovou platnost. Teprve potom má smysl rozhodovat o konkrétním nástroji podle vlastního benchmarku.
