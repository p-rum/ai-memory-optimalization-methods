# AI memory optimization methods

Český interaktivní workshop o strukturování paměti LLM agenta pro vývojáře. **Maximálně 30 minut**, 12 slidů, Knowledge Graph × vektorové databáze, návrhové cvičení a vlastní měření.

Začněte v **[workshop/README.md](workshop/README.md)**.

- [Prezentace HTML](workshop/presentation.html), [PowerPoint](workshop/presentation.pptx), [PDF](workshop/presentation.pdf)
- [Offline ukázka incidentů](workshop/demo.html), [ukázka nad skutečným kódem scikit-learn](workshop/source-demo.html)
- [Scénář moderátora](workshop/facilitator.md), [tahák pro účastníky](workshop/handout.md)
- [Měření modelového scénáře](workshop/experiment.md), [měření skutečného zdroje](workshop/real-source-experiment.md)

Stáhněte Code → Download ZIP a otevřete `workshop/presentation.html` v prohlížeči. HTML je samostatné a nevyžaduje API klíč. Interakce ukazují předpočítané výsledky skutečného běhu; Python kód pro opakování je přiložen.

Vektorový baseline používá TF‑IDF, nikoli neuronové embeddingy. Graf modelového scénáře a routing jsou připravené ručně; skutečný zdrojový příklad extrahuje explicitní importy z AST. Výsledky měří retrieval důkazů a bajty kontextu, ne kvalitu odpovědí LLM ani výkon produkčních databází. Metodická omezení jsou součástí podkladů.
