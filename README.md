# AI memory optimization methods

Český **30minutový interaktivní meeting** o paměti LLM agenta pro tým podpůrné platformy burzovních obchodníků.

Začněte [návodem](workshop/README.md) a [scénářem moderátora](workshop/facilitator.md). Scénář obsahuje slovníček, text k přednesu, přesná kliknutí a očekávané výsledky i pro méně zkušeného prezentujícího.

- [Prezentace HTML](workshop/presentation.html), [PowerPoint](workshop/presentation.pptx), [PDF](workshop/presentation.pdf).
- [Grafické srovnání vektorů a grafů](workshop/bank-visual.html): původ dat týdenního reportu, dopady feature what-if margin, platná verze mechanismu finančního zdraví.
- [Příklady a výpočet podrobně](workshop/bank-guide.md), [vlastní měření](workshop/bank-experiment.md), [spustitelný modelový kód](workshop/bank_demo).
- [Graphify a další nástroje](workshop/tools-comparison.md), [interaktivní porovnání dvojice](workshop/tools-comparison.html).

Stáhněte **Code → Download ZIP**, rozbalte a otevřete `workshop/presentation.html`. Není potřeba API klíč ani instalace. Ukázky odhalují uložené výsledky skutečného běhu.

Používáme modelovou platformu a ilustrativní vzorec, nikoli skutečná data či bankovní metodiku. TF-IDF baseline, AST graf a registry mají popsaná omezení; výsledky nejsou benchmark produktů ani odpovědí LLM.

## Paměť implementačního agenta

Nová samostatná [30minutová prezentace](presentations/implementation-agent-memory/README.md) s příklady Kotlin / Spring Boot / PostgreSQL, porovnáním struktur a nástrojů a transparentním modelem nákladů včetně cache.
